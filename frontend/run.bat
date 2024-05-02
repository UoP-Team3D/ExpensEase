@echo off
setlocal

REM Change to the directory where the batch file is located
cd /d %~dp0

REM Build the React project
echo Building the React app...
call npm run build

REM Check if build was successful
if not exist build\index.html (
    echo Build failed, index.html not found.
    exit /b
)

REM Copy the build directory to the Flask static folder
echo Copying build to the Flask app...
xcopy /E /I /Y build ..\backend\build

REM Navigate to the backend directory
cd ..\backend

REM Activate the virtual environment and start the Flask server in a single command
echo Starting the Flask server...
cmd /c "env\Scripts\activate && python run.py"

REM Keep the window open to see the output from the Flask server
pause
