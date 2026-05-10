@echo off
setlocal

set "NODE_EXE=%~1"
set "SCRIPT=%~2"
if "%SCRIPT%"=="" (
  if "%NODE_EXE%"=="" (
    set "SCRIPT=%~dp0publish-stop.js"
  ) else (
    set "SCRIPT=%~1"
    set "NODE_EXE="
  )
)
if "%SCRIPT%"=="" (
  echo Missing publish-stop script path. 1>&2
  exit /b 2
)

set "NODE_OPTIONS_CURRENT=%NODE_OPTIONS%"
echo %NODE_OPTIONS_CURRENT% | findstr /C:"--use-system-ca" >nul
if errorlevel 1 (
  if "%NODE_OPTIONS%"=="" (
    set "NODE_OPTIONS=--use-system-ca"
  ) else (
    set "NODE_OPTIONS=%NODE_OPTIONS% --use-system-ca"
  )
)

if not "%NODE_EXE%"=="" (
  set "OUT=%TEMP%\imessage-handoff-stop-%RANDOM%-%RANDOM%.json"
  set "ERR=%TEMP%\imessage-handoff-stop-%RANDOM%-%RANDOM%.err"
  "%NODE_EXE%" "%SCRIPT%" > "%OUT%" 2> "%ERR%"
  set "CODE=%ERRORLEVEL%"
  if not "%CODE%"=="0" (
    type "%ERR%" 1>&2
    del "%OUT%" >nul 2>nul
    del "%ERR%" >nul 2>nul
    exit /b %CODE%
  )
  for %%A in ("%OUT%") do set "SIZE=%%~zA"
  if "%SIZE%"=="0" (
    echo {"continue":true}
  ) else (
    type "%OUT%"
  )
  del "%OUT%" >nul 2>nul
  del "%ERR%" >nul 2>nul
  exit /b 0
)

set "OUT=%TEMP%\imessage-handoff-stop-%RANDOM%-%RANDOM%.json"
set "ERR=%TEMP%\imessage-handoff-stop-%RANDOM%-%RANDOM%.err"
node "%SCRIPT%" > "%OUT%" 2> "%ERR%"
set "CODE=%ERRORLEVEL%"
if not "%CODE%"=="0" (
  type "%ERR%" 1>&2
  del "%OUT%" >nul 2>nul
  del "%ERR%" >nul 2>nul
  exit /b %CODE%
)
for %%A in ("%OUT%") do set "SIZE=%%~zA"
if "%SIZE%"=="0" (
  echo {"continue":true}
) else (
  type "%OUT%"
)
del "%OUT%" >nul 2>nul
del "%ERR%" >nul 2>nul
exit /b 0
