@echo off
title Unternehmensregisterassistent Setup
echo Unternehmensregisterassistent Setup

echo Updating pip
python -m pip install --upgrade pip

echo Installing Packages
pip install pandas
pip install openpyxl
pip install configparser
pip install requests
echo Packages installed successfully

echo Creating folders
cd %~dp0
md data
md results
echo Folders created

echo Setup complete!
pause