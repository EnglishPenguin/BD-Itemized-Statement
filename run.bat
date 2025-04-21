echo "Running Itemized Statement File Generation
@Echo off

SETLOCAL
set FILE_PATH=C:\Users\pa_dpashayan\Desktop\PyProjects\BD-Itemized-Statement\
cd %FILE_PATH%
set SCRIPT_PATH=%FILE_PATH%main.py
set VENV_PATH=%FILE_PATH%.venv

call "%VENV_PATH%\Scripts\activate.bat"
python -u "%SCRIPT_PATH%" > logs\TS_log.txt 2>&1

IF ERRORLEVEL 1 (
    echo Python script encountered an error. The error message is: %ERRORLEVEL% %ERRORMESSAGE%
)
ENDLOCAL