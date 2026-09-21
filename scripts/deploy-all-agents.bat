@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo [CloudPhone] Deploying Agents to All LAN Devices
echo ===================================================

set "HOST_IP=192.168.1.163"
set "SIGNALING=ws://%HOST_IP%:8111/register_agent"
set "BASE_DIR=%~dp0..\deploy_agent"

set "DEVICES=48 54 66 73 96 97 134 153 167 178 180 182 238"

for %%O in (%DEVICES%) do (
    set "IP=192.168.1.%%O"
    set "SERIAL=!IP!:5555"
    if "%%O"=="167" (
        set "DEV_ID=Samsung_S7"
    ) else (
        set "DEV_ID=Samsung_S7_%%O"
    )
    
    echo [*] Checking connection to !SERIAL!...
    adb connect !SERIAL! >nul 2>&1
    
    echo [*] Deploying agent to !DEV_ID! (!SERIAL!)...
    call "!BASE_DIR!\run.bat" !SERIAL! -id !DEV_ID! -signaling !SIGNALING!
    echo ---------------------------------------------------
)

echo.
echo ===================================================
echo [CloudPhone] Deployment Completed.
echo Querying registered devices on signaling server:
echo ===================================================
curl -s http://127.0.0.1:8111/devices
echo.
pause
