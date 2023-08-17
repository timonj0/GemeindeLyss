@echo off
title Steuerregisterabgleich Setup
echo Steuerregisterabgleich Setup
echo Updating pip
python -m pip install --upgrade pip
echo Installing Packages
pip install pandas
pip install openpyxl
pip install configparser
echo Packages installed successfully
echo Setup complete!
pause