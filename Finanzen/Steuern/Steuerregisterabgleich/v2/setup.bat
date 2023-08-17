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

echo Creating folders
cd %~dp0
md register
cd register
md reg_cit
md reg_tax
md reg_qst
echo Folders created

echo Setup complete!
pause