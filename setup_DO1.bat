@echo off
echo Setting up the DO1 environment...

REM Step 1: Create a virtual environment
python -m venv env
echo Virtual environment created.

REM Step 2: Activate the virtual environment
call env\Scripts\activate
echo Virtual environment activated.

REM Step 3: Install required packages
pip install -r requirements.txt
echo Packages installed.

REM Step 4: Run the DO1 script (optional, if you want to run the script after setup)
python your_DO1_script.py

echo Setup complete.
pause
