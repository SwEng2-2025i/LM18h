@echo off
echo ========================================
echo Starting Lab 2 Integration Test Services
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Starting services in separate windows...
echo.

echo Starting Users Service (Port 5001)...
start "Users Service" cmd /k "python Users_Service\main.py"
timeout /t 3

echo Starting Task Service (Port 5002)...
start "Task Service" cmd /k "python Task_Service\main.py"
timeout /t 3

echo Starting Frontend Service (Port 5003)...
start "Frontend Service" cmd /k "python Front-End\main.py"
timeout /t 3

echo.
echo ========================================
echo All services started!
echo ========================================
echo Users Service:    http://localhost:5001
echo Task Service:     http://localhost:5002
echo Frontend:         http://localhost:5003
echo ========================================
echo.
echo Press any key to run the Backend Test...
pause
python Test\BackEnd-Test.py

echo.
echo Press any key to run the Frontend Test...
pause
python Test\FrontEnd-Test.py

echo.
echo Tests completed! Check the Test\reports folder for PDF reports.
pause
