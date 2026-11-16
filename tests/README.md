# macsmc ACPI power regression test

Apply the T2 kernel patch series, then point the test at the resulting driver:

```sh
python3 tests/macsmc-acpi-power-test.py /path/to/linux/drivers/power/supply/macsmc-power.c
```

The test compiles the actual driver functions in a small host harness with
mocked ACPI and SMC reads. It requires Python 3 and a C compiler. It checks
missed notifications, charging/full/idle/discharging states, firmware read
errors, the desktop and non-ACPI paths, change-only one-second polling,
immediate notification handling, and suspend/resume scheduling. It also runs
against the original 3010 driver and fails on the stale ONLINE regression.

To enable AddressSanitizer and UndefinedBehaviorSanitizer, add `--sanitize`.
If running under ptrace, disable LeakSanitizer with
`ASAN_OPTIONS=detect_leaks=0`; the harness does not allocate heap objects.

This host test complements a kernel-module build and hardware testing. It
does not exercise real ACPI firmware, workqueue concurrency, or system sleep.
