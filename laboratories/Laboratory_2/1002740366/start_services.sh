#!/bin/bash

echo "========================================"
echo "Starting Lab 2 Integration Test Services"
echo "========================================"
echo

echo "Installing dependencies..."
pip install -r requirements.txt
echo

echo "Starting services..."
echo

echo "Starting Users Service (Port 5001)..."
gnome-terminal --title="Users Service" -- bash -c "python3 Users_Service/main.py; exec bash" &
sleep 3

echo "Starting Task Service (Port 5002)..."
gnome-terminal --title="Task Service" -- bash -c "python3 Task_Service/main.py; exec bash" &
sleep 3

echo "Starting Frontend Service (Port 5003)..."
gnome-terminal --title="Frontend Service" -- bash -c "python3 Front-End/main.py; exec bash" &
sleep 3

echo
echo "========================================"
echo "All services started!"
echo "========================================"
echo "Users Service:    http://localhost:5001"
echo "Task Service:     http://localhost:5002"
echo "Frontend:         http://localhost:5003"
echo "========================================"
echo

echo "Press Enter to run the Backend Test..."
read
python3 Test/BackEnd-Test.py

echo
echo "Press Enter to run the Frontend Test..."
read
python3 Test/FrontEnd-Test.py

echo
echo "Tests completed! Check the Test/reports folder for PDF reports."
