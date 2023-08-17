@echo off
echo Steuerregisterabgleich Setup
echo Updating pip
python -m pip install --upgrade pip
echo Installing Packages
pip install pandas
pip install openpyxl
pip install configparser
pip install tkinter
pip install tkinterdnd2
echo Packages installed successfully
echo Setup complete!
pause