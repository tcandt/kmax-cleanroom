@echo off
echo ===================================================
echo [ADB LAN] Scanning and Connecting Android Devices
echo ===================================================

setlocal enabledelayedexpansion

set "DEVICES=192.168.1.48 192.168.1.54 192.168.1.66 192.168.1.73 192.168.1.96 192.168.1.97 192.168.1.134 192.168.1.153 192.168.1.167 192.168.1.178 192.168.1.180 192.168.1.182 192.168.1.238"

for %%I in (%DEVICES%) do (
    echo [*] Connecting to %%I:5555...
    adb connect %%I:5555
)

echo.
echo ===================================================
echo [ADB LAN] Current Attached Devices:
echo ===================================================
adb devices -l
echo.
pause
