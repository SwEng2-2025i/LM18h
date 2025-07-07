@echo off
echo ========================================
echo Lab 2 - Quick Test Runner
echo ========================================
echo.

echo Checking if services are running...
echo.

echo Testing Backend Integration...
python Test\BackEnd-Test.py
echo.

echo Waiting 5 seconds before frontend test...
timeout /t 5

echo Testing Frontend E2E...
python Test\FrontEnd-Test.py
echo.

echo ========================================
echo Tests completed!
echo Check Test\reports folder for PDF reports
echo ========================================
pause
