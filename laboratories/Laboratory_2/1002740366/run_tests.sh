#!/bin/bash

echo "========================================"
echo "Lab 2 - Quick Test Runner"
echo "========================================"
echo

echo "Checking if services are running..."
echo

echo "Testing Backend Integration..."
python3 Test/BackEnd-Test.py
echo

echo "Waiting 5 seconds before frontend test..."
sleep 5

echo "Testing Frontend E2E..."
python3 Test/FrontEnd-Test.py
echo

echo "========================================"
echo "Tests completed!"
echo "Check Test/reports folder for PDF reports"
echo "========================================"
