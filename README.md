Debt Optimization Tool (DO1)
Overview
The Debt Optimization Tool (DO1) is designed to help users manage their debts effectively using two widely recognized methods: the Avalanche and Snowball repayment strategies. The tool allows users to input details of up to four different types of loans and provides visualizations to analyze repayment timelines, interest savings, and monthly payment breakdowns.

This project is implemented using Python with Dash for the UI and interactive visualizations.

Features
1. Loan Types
The tool supports the following 4 types of loans:
Credit Card Debt
Auto Loan
Student Loan
Personal Loan
2. Repayment Methods
Avalanche Method:
Focuses on repaying the loan with the highest interest rate first, minimizing the total interest paid.
Snowball Method:
Focuses on repaying the smallest loan amount first, providing quick wins and psychological motivation.
3. Visualizations
The tool generates the following visualizations to assist users in analyzing their debt repayment plans:

Debt Repayment Timeline:
A line graph showing how long it will take to repay all debts under both the Avalanche and Snowball methods.
Interest Savings:
A bar chart comparing the total interest saved using the Avalanche vs. Snowball methods.
Monthly Payment Breakdown:
A stacked bar chart showing how much of each monthly payment goes toward each debt.
Setup Instructions
Step 1: Run the Batch File
To set up the project environment, follow these steps:

Navigate to the project directory where setup_DO1.bat is located.
Double-click the setup_DO1.bat file. It will:
Create a virtual environment.
Install all necessary dependencies, including Dash.
Step 2: Run the Application
Once the setup is complete:

Open a terminal (Command Prompt or VS Code terminal).

Activate the virtual environment:

cmd
Copy code
env\Scripts\activate
Run the UI file to launch the application:

cmd
Copy code
python user_interface.py
Open the URL provided in the terminal (e.g., http://127.0.0.1:8050) in your web browser.

Troubleshooting
If the setup_DO1.bat file does not work:

Manually install the required packages by running:
cmd
Copy code
pip install dash
Then run:
cmd
Copy code
pip install -r requirements.txt
Ensure you are using the correct Python interpreter (the one inside the env virtual environment).

Folder Structure
The project folder contains the following files:

bash
Copy code
project_fixed/
│
├── env/                  # Virtual environment (auto-created by setup_DO1.bat)
├── repayment_logic.py    # Core logic for debt optimization
├── user_interface.py     # Dash-based user interface
├── setup_DO1.bat         # Batch file to set up the environment
├── requirements.txt      # List of dependencies
└── README.md             # This file
How It Works
Input Loans:
Enter the details of your debts, including the type, balance, interest rate, and extra payment amounts.
Select a Method:
Choose between the Avalanche and Snowball methods.
View Results:
Analyze repayment timelines, total interest paid, and monthly payment breakdown using the interactive visualizations.
Contact Information
If you have any issues or questions about using DO1, feel free to reach out!
