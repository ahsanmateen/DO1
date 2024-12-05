
import repayment_logic
import dash
from dash import dcc, html
import plotly.graph_objs as go


def get_debts():
    return [
        {'debt_type': 'Credit Card', 'amount': 5000, 'interest_rate': 19.99, "extra_payment": 400, "months_to_maturity": None},
        {'debt_type': 'Auto Loan', 'amount': 12000, 'interest_rate': 4.99, "extra_payment": 400, "months_to_maturity": 60},
        {'debt_type': 'Student Loan', 'amount': 15000, 'interest_rate': 6.99, "extra_payment": 400, "months_to_maturity": 36},
        {'debt_type': 'Personal Loan', 'amount': 5000, 'interest_rate': 8.99, "extra_payment": 400, "months_to_maturity": 24}
    ]


def create_dash_app():
    # Define initial Dash layout for user input
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Debt Repayment Dashboard"),
        html.Div([
            html.Label("Select Repayment Type:"),
            dcc.Dropdown(
                id='repayment-type',
                options=[
                    {'label': 'Avalanche', 'value': 'avalanche'},
                    {'label': 'Snowball', 'value': 'snowball'}
                ],
                value='avalanche',  # Default value
                clearable=False
            )
        ], style={'margin-bottom': '20px'}),
        html.Div([
            html.Label("Enter Monthly Income:"),
            dcc.Input(
                id='monthly-income',
                type='number',
                value=1000  # Default value
            )
        ], style={'margin-bottom': '20px'}),
        #--------------------------------------------------------------------
        # 
        #--------------------------------------------------------------------
        # Add inputs for debt amounts and interest rates
        html.Div([
            html.H2("Debt Details"),
            html.Div([
                html.H3("Credit Card"),
                html.Label("Amount:"),
                dcc.Input(id='Credit Card-amount', type='number', value=5000),
                html.Label("Interest Rate (%):"),
                dcc.Input(id='Credit Card-interest_rate', type='number', value=19.99)
            ], style={'margin-bottom': '20px'}),
            html.Div([
                html.H3("Auto Loan"),
                html.Label("Amount:"),
                dcc.Input(id='Auto Loan-amount', type='number', value=12000),
                html.Label("Interest Rate (%):"),
                dcc.Input(id='Auto Loan-interest_rate', type='number', value=4.99)
            ], style={'margin-bottom': '20px'}),
            html.Div([
                html.H3("Student Loan"),
                html.Label("Amount:"),
                dcc.Input(id='Student Loan-amount', type='number', value=15000),
                html.Label("Interest Rate (%):"),
                dcc.Input(id='Student Loan-interest_rate', type='number', value=6.99)
            ], style={'margin-bottom': '20px'}),
            html.Div([
                html.H3("Personal Loan"),
                html.Label("Amount:"),
                dcc.Input(id='Personal Loan-amount', type='number', value=5000),
                html.Label("Interest Rate (%):"),
                dcc.Input(id='Personal Loan-interest_rate', type='number', value=8.99)
            ], style={'margin-bottom': '20px'})
        ]),
        html.Button("Submit", id="submit-button", n_clicks=0),
        html.Div(id='output-dashboard')
    ])

    @app.callback(
        dash.dependencies.Output('output-dashboard', 'children'),
        [dash.dependencies.Input('submit-button', 'n_clicks')],
        [dash.dependencies.State('repayment-type', 'value'),
         dash.dependencies.State('monthly-income', 'value'),
         dash.dependencies.State('Credit Card-amount', 'value'),
         dash.dependencies.State('Credit Card-interest_rate', 'value'),
         dash.dependencies.State('Auto Loan-amount', 'value'),
         dash.dependencies.State('Auto Loan-interest_rate', 'value'),
         dash.dependencies.State('Student Loan-amount', 'value'),
         dash.dependencies.State('Student Loan-interest_rate', 'value'),
         dash.dependencies.State('Personal Loan-amount', 'value'),
         dash.dependencies.State('Personal Loan-interest_rate', 'value')]
    )
    def update_dashboard(n_clicks, repayment_type, monthly_income, cc_amount, cc_interest,
                         auto_amount, auto_interest, student_amount, student_interest,
                         personal_amount, personal_interest):
        if n_clicks > 0:
            # Construct debts based on user inputs
            debts = [
                {'debt_type': 'Credit Card', 'amount': cc_amount or 0, 'interest_rate': cc_interest or 0,
                 "extra_payment": 400, "months_to_maturity": None},
                {'debt_type': 'Auto Loan', 'amount': auto_amount or 0, 'interest_rate': auto_interest or 0,
                 "extra_payment": 400, "months_to_maturity": 60},
                {'debt_type': 'Student Loan', 'amount': student_amount or 0, 'interest_rate': student_interest or 0,
                 "extra_payment": 400, "months_to_maturity": 36},
                {'debt_type': 'Personal Loan', 'amount': personal_amount or 0, 'interest_rate': personal_interest or 0,
                 "extra_payment": 400, "months_to_maturity": 24}
            ]

            # Fetch data for each strategy independently
            # Copy debts explicitly to ensure isolation
            
            avalanche_debts = debts.copy()
            snowball_debts = debts.copy()
            timeline = []
            payments = []
            if repayment_type == "avalanche":
                avalanche_timeline, avalanche_payments, avalanche_interest, snowball_interests = repayment_logic.get_timeline_payments_interests(
                    avalanche_debts, "avalanche", monthly_income)
                timeline = avalanche_timeline
                payments = avalanche_payments
            else:
                snowball_timeline, snowball_payments, avalanche_interest, snowball_interests = repayment_logic.get_timeline_payments_interests(
                    snowball_debts, "snowball", monthly_income)
                timeline = snowball_timeline
                payments = snowball_payments
            
            #--------------------------------------------------------------------
            #   
            #--------------------------------------------------------------------
            # Repayment Timeline
            debt_types = set()
            balances = {}
            month_to_debts = {entry['month']: entry['debts'] for entry in timeline}
            for month, debts in month_to_debts.items():
                for debt in debts:
                    debt_type = debt['debt_type']
                    debt_types.add(debt_type)
                    if debt_type not in balances:
                        balances[debt_type] = []
                    while len(balances[debt_type]) < month:
                        balances[debt_type].append(None)
                    balances[debt_type].append(debt['remaining_balance'])

            repayment_timeline_graph = dcc.Graph(
                figure={
                    'data': [
                        go.Scatter(
                            x=list(range(len(balances[debt_type]))),
                            y=balances[debt_type],
                            mode='lines+markers',
                            name=debt_type
                        ) for debt_type in debt_types
                    ],
                    'layout': go.Layout(
                        title="Debt Repayment Timeline",
                        xaxis={'title': 'Months'},
                        yaxis={'title': 'Remaining Balance'},
                        legend={'title': 'Debt Type'}
                    )
                }
            )

            # Payment Breakdown
            months = [entry['month'] for entry in payments]
            payment_data = {}
            for entry in payments:
                for payment in entry['payments']:
                    debt_type = payment['debt_type']
                    if debt_type not in payment_data:
                        payment_data[debt_type] = []
                    payment_data[debt_type].append(payment['payment_made'])

            payment_breakdown_graph = dcc.Graph(
                figure={
                    'data': [
                        go.Bar(
                            x=months,
                            y=payment_data[debt_type],
                            name=debt_type
                        ) for debt_type in payment_data
                    ],
                    'layout': go.Layout(
                        title="Payment Breakdown by Debt Type",
                        xaxis={'title': 'Months'},
                        yaxis={'title': 'Payment Amount'},
                        barmode='group',
                        legend={'title': 'Debt Type'}
                    )
                }
            )

            # Interest Timeline Comparison
            avalanche_months = [entry['month'] for entry in avalanche_interest]
            avalanche_totals = [entry['total_interest'] for entry in avalanche_interest]
            snowball_months = [entry['month'] for entry in snowball_interests]
            snowball_totals = [entry['total_interest'] for entry in snowball_interests]
            interest_timeline_graph = dcc.Graph(
                figure={
                    'data': [
                        go.Scatter(
                            x=avalanche_months,
                            y=avalanche_totals,
                            mode='lines+markers',
                            name='Avalanche Strategy'
                        ),
                        go.Scatter(
                            x=snowball_months,
                            y=snowball_totals,
                            mode='lines+markers',
                            name='Snowball Strategy'
                        )
                    ],
                    'layout': go.Layout(
                        title="Interest Timeline: Avalanche vs Snowball Strategies",
                        xaxis={'title': 'Months'},
                        yaxis={'title': 'Total Interest'},
                        legend={'title': 'Strategy'}
                    )
                }
            )

            # Combine all plots
            return html.Div([
                html.H2("Repayment Timeline"),
                repayment_timeline_graph,
                html.H2("Payment Breakdown"),
                payment_breakdown_graph,
                html.H2("Interest Timeline"),
                interest_timeline_graph
            ])

        return "Submit your preferences to view the dashboard."

    return app


if __name__ == "__main__":
    app = create_dash_app()
    app.run_server(debug=True)

#--------------------------------------------------------------------
#  
#--------------------------------------------------------------------