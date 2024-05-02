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

REM Start the Flask server
echo Starting the Flask server...
call python run.py

REM Keep the window open to see the output from the Flask server
pause
