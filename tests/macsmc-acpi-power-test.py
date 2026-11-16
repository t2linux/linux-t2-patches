#!/usr/bin/env python3
"""Compile the driver's actual ACPI functions with mocked firmware reads."""
import argparse
import pathlib
import subprocess
import tempfile

def function(source, name):
    start = source.index("static ", source.index(name) - 20)
    brace = source.index("{", start)
    depth = 1
    end = brace + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


PRELUDE = r'''
#include <assert.h>
#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
typedef int16_t s16;
typedef uint16_t u16;
typedef uint32_t u32;
typedef unsigned long acpi_status;
typedef void *acpi_handle;
#define ACPI_FAILURE(s) ((s) != 0)
#define SMC_KEY(k) 0
#define swab16(v) __builtin_bswap16(v)
#define swab32(v) __builtin_bswap32(v)
enum { POWER_SUPPLY_STATUS_CHARGING = 1, POWER_SUPPLY_STATUS_DISCHARGING,
       POWER_SUPPLY_STATUS_NOT_CHARGING, POWER_SUPPLY_STATUS_FULL };
enum power_supply_property { POWER_SUPPLY_PROP_ONLINE, POWER_SUPPLY_PROP_CURRENT_NOW,
       POWER_SUPPLY_PROP_POWER_NOW, POWER_SUPPLY_PROP_VOLTAGE_NOW,
       POWER_SUPPLY_PROP_INPUT_CURRENT_LIMIT, POWER_SUPPLY_PROP_INPUT_POWER_LIMIT };
union power_supply_propval { int intval; };
struct apple_smc { bool is_acpi; };
struct acpi_device { acpi_handle handle; };
struct power_supply { void *data; };
struct device { void *data; };
struct work_struct { int unused; };
struct delayed_work { struct work_struct work; };
#define container_of(ptr, type, member) ((type *)((char *)(ptr) - offsetof(type, member)))
#define to_delayed_work(ptr) container_of(ptr, struct delayed_work, work)
#define HZ 1000
#define system_freezable_wq ((void *)1)
struct macsmc_power {
    bool has_battery, has_pd0r;
    unsigned long long adapter_status; /* Also compile the unfixed driver. */
    struct apple_smc *smc;
    struct acpi_device *adapter;
    struct power_supply *batt, *ac;
    struct delayed_work acpi_poll_work;
    int acpi_last_online, acpi_last_status;
};
static unsigned long long psr;
static int acpi_error, current_ma, percentage, smc_error, reads, events;
static int scheduled, last_delay = -1, cancelled;
static int queue_delayed_work(void *q, struct delayed_work *w, int delay)
{ assert(q && w); scheduled++; last_delay = delay; return 1; }
static int mod_delayed_work(void *q, struct delayed_work *w, int delay)
{ return queue_delayed_work(q, w, delay); }
static void cancel_delayed_work_sync(struct delayed_work *w)
{ assert(w); cancelled++; last_delay = -1; }
static void *power_supply_get_drvdata(struct power_supply *s) { return s->data; }
static void *dev_get_drvdata(struct device *d) { return d->data; }
static void power_supply_changed(struct power_supply *s) { assert(s); events++; }
static acpi_status acpi_evaluate_integer(acpi_handle h, const char *name, void *args,
                                       unsigned long long *state)
{
    (void)args;
    assert(h && !strcmp(name, "_PSR"));
    reads++;
    if (acpi_error) return 1;
    *state = psr;
    return 0;
}
static int apple_smc_read_s16(struct apple_smc *s, int key, s16 *v)
{ (void)s; (void)key; *v = (s16)swab16((u16)current_ma); return smc_error; }
static int apple_smc_read_u16(struct apple_smc *s, int key, u16 *v)
{ (void)s; (void)key; *v = swab16((u16)percentage); return smc_error; }
static int apple_smc_read_u32(struct apple_smc *s, int key, u32 *v)
{ (void)s; (void)key; *v = (u32)psr; return smc_error; }
static int macsmc_battery_acpi_read(struct apple_smc *s, int key, int *v, int scale)
{ (void)s; (void)key; (void)v; (void)scale; return -EINVAL; }
'''

TESTS = r'''
int main(void)
{
    struct apple_smc smc = { .is_acpi = true };
    struct acpi_device adapter = { .handle = &smc };
    struct power_supply battery, ac;
    struct macsmc_power p = { .has_battery = true, .smc = &smc,
        .adapter = &adapter, .batt = &battery, .ac = &ac };
    struct device dev = { .data = &p };
    union power_supply_propval val;
    battery.data = ac.data = &p;

    /* No notification between plug/unplug: both properties must follow _PSR. */
    for (int i = 0; i < 100; i++) {
        psr = i % 2;
        current_ma = psr ? 3506 : -700;
        percentage = 7;
        assert(macsmc_ac_get_property(&ac, POWER_SUPPLY_PROP_ONLINE, &val) == 0);
        assert(val.intval == (int)psr);
        assert(macsmc_battery_acpi_get_status(&p) ==
               (psr ? POWER_SUPPLY_STATUS_CHARGING : POWER_SUPPLY_STATUS_DISCHARGING));
    }
    psr = 1;
    percentage = 100; current_ma = 0;
    assert(macsmc_battery_acpi_get_status(&p) == POWER_SUPPLY_STATUS_FULL);
    current_ma = -100;
    assert(macsmc_battery_acpi_get_status(&p) == POWER_SUPPLY_STATUS_FULL);
    percentage = 80; current_ma = 0;
    assert(macsmc_battery_acpi_get_status(&p) == POWER_SUPPLY_STATUS_NOT_CHARGING);
    acpi_error = 1;
    assert(macsmc_battery_acpi_get_status(&p) == -EIO);
    assert(macsmc_ac_get_property(&ac, POWER_SUPPLY_PROP_ONLINE, &val) == -EIO);
    acpi_error = 0; smc_error = -ENODATA;
    assert(macsmc_battery_acpi_get_status(&p) == -ENODATA);
    smc_error = 0;

    /* Desktop: always online, without dereferencing a missing adapter. */
    p.has_battery = false; p.adapter = NULL;
    int old_reads = reads;
    assert(macsmc_ac_get_property(&ac, POWER_SUPPLY_PROP_ONLINE, &val) == 0);
    assert(val.intval == 1 && reads == old_reads);
    p.has_battery = true; p.adapter = &adapter;

    /* Apple Silicon keeps the SMC CHIS path. */
    smc.is_acpi = false; psr = 1;
    assert(macsmc_ac_get_property(&ac, POWER_SUPPLY_PROP_ONLINE, &val) == 0);
    assert(val.intval == 1 && reads == old_reads);
    p.adapter = NULL;
    int old_scheduled = scheduled;
    assert(macsmc_power_resume(&dev) == 0 && scheduled == old_scheduled);
    smc.is_acpi = true;
    p.adapter = &adapter;

    /* Polling reports changes immediately, then checks again in one second. */
    p.acpi_last_online = p.acpi_last_status = -1;
    percentage = 50; current_ma = 1000;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 2 && last_delay == HZ);
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 2); /* No periodic uevent spam. */
    psr = 0; current_ma = -700;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 4 && p.acpi_last_online == 0);
    psr = 1; current_ma = 1500;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 6 && p.acpi_last_status == POWER_SUPPLY_STATUS_CHARGING);
    percentage = 100; current_ma = 0;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 8 && p.acpi_last_status == POWER_SUPPLY_STATUS_FULL);
    acpi_error = 1;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 8 && last_delay == HZ); /* Keep valid state and retry. */
    acpi_error = 0;

    /* Notifications and resume check immediately; suspend cancels polling. */
    assert(macsmc_power_suspend(&dev) == 0 && cancelled == 1 && last_delay == -1);
    assert(macsmc_power_resume(&dev) == 0 && last_delay == 0);
    old_scheduled = scheduled;
    macsmc_power_acpi_notify(NULL, 0x81, &p);
    assert(scheduled == old_scheduled);
    macsmc_power_acpi_notify(NULL, 0x80, &p);
    assert(scheduled == old_scheduled + 1 && last_delay == 0);
    p.batt = NULL;
    p.acpi_last_status = -1;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 9);
    p.ac = NULL;
    p.acpi_last_status = -1;
    macsmc_power_acpi_poll(&p.acpi_poll_work.work);
    assert(events == 9);
    puts("PASS: live reads, charge states, failures, desktops, Apple Silicon, change-only polling, suspend/resume");
    return 0;
}
'''

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=pathlib.Path, help="Patched kernel's drivers/power/supply/macsmc-power.c")
parser.add_argument("--sanitize", action="store_true", help="Enable address and undefined-behavior sanitizers")
args = parser.parse_args()
source = args.source.read_text()
names = ("macsmc_acpi_get_online", "macsmc_battery_acpi_get_status",
         "macsmc_ac_get_property", "macsmc_power_acpi_poll", "macsmc_power_acpi_notify",
         "macsmc_power_suspend", "macsmc_power_resume")
functions = "\n".join(function(source, name) for name in names if name + "(" in source)
if "macsmc_power_resume(" not in source:
    functions += "\nstatic int macsmc_power_resume(struct device *d) { (void)dev_get_drvdata(d); return 0; }\n"
if "macsmc_power_suspend(" not in source:
    functions += "\nstatic int macsmc_power_suspend(struct device *d) { (void)d; return 0; }\n"
if "macsmc_power_acpi_poll(" not in source:
    functions += "\nstatic void macsmc_power_acpi_poll(struct work_struct *w) { (void)w; }\n"
code = PRELUDE + "\n" + functions + TESTS
with tempfile.TemporaryDirectory() as temporary:
    directory = pathlib.Path(temporary)
    (directory / "test.c").write_text(code)
    sanitizers = ["-fsanitize=undefined,address"] if args.sanitize else []
    subprocess.run(["cc", "-std=gnu11", "-Wall", "-Wextra", "-Werror",
                    "-Wno-unused-parameter", "-Wno-unused-function", *sanitizers, "-g",
                    str(directory / "test.c"), "-o", str(directory / "test")], check=True)
    subprocess.run([str(directory / "test")], check=True)
