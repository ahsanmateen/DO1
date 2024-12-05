import copy
def get_avalanche_order(debts):
    '''
    This function takes a list of debts and returns them
    sorted from highest to lowest order of interest rate
    '''
    sorted_debts = sorted(debts, key=lambda x: x['interest_rate'], reverse=True)
    repayment_order = []
    for debt in sorted_debts:
    
        if debt["amount"] > 0:
            repayment_order.append(debt)
    return repayment_order

def get_snowball_order(debts):
    '''
    This function takes a list of debts and returns them
    sorted from lowest to highest order of interest rate
    '''
    sorted_debts = sorted(debts, key=lambda x: x['interest_rate'], reverse=False)
    repayment_order = []
    for debt in sorted_debts:
        
        if debt["amount"] > 0:
            repayment_order.append(debt)
    return repayment_order

def get_minimum_income_to_payoff(debts):
    '''
    This function takes a list of debts and determines the
    minimum monthly payment that will allow for them to be 
    paid off by maturity
    '''
    #--------------------------------------------------------------------
    #   TODO - At the moment the minimum payment is being hardcoded below
    #--------------------------------------------------------------------
    payment = 1000
    return payment


def get_snowball_interests(debts, user_income = 0):
    '''
    returns the interests for the snowball method
    '''
    debts = get_snowball_order(debts)
    #get monthly income
    monthly_income = max(user_income, get_minimum_income_to_payoff(debts))
    #add extra payments to monthly income
    monthly_income += sum(debt1['extra_payment'] for debt1 in debts if debt1['amount'] > 0)
    
    snowball_interests = []
    current_month = 0
    while any(debt['amount'] > 0 for debt in debts):
        month_data = []
        interest_data = []
        remaining_income = monthly_income
        for debt in debts:
            if debt['amount'] > 0 and (debt['months_to_maturity'] is None or debt['months_to_maturity'] > 0):
                # Calculate monthly interest & payment
                monthly_interest = debt['amount'] * (debt['interest_rate'] / 100 / 12)
                payment = min(remaining_income, debt['amount'] + monthly_interest)
                debt['amount'] -= (payment - monthly_interest)
                remaining_income -= payment

                # Decrement months to maturity
                if debt['months_to_maturity'] is not None:
                    debt['months_to_maturity'] -= 1
 
                # Prevent negative balances
                if debt['amount'] < 0:
                    debt['amount'] = 0

                # Add data to month
                month_data.append({
                    'debt_type': debt['debt_type'],
                    'remaining_balance': debt['amount'],
                    'months_to_maturity': debt.get('months_to_maturity', None)           
                })
                interest_data.append({
                    'debt_type': debt['debt_type'],
                    'interest': monthly_interest
                })
        snowball_interests.append({
            'month': current_month,
            'interests': interest_data
        })

        # Stop if no progress is being made
        if not any(d['remaining_balance'] > 0 for d in month_data):
            break

        current_month += 1
        if current_month > 60:
            break
    return snowball_interests


def get_avalanche_interests(debts, user_income = 0):
    '''
    returns the interests for the avalanche method
    '''
    debts = get_avalanche_order(debts)
    #get monthly income
    monthly_income = max(user_income, get_minimum_income_to_payoff(debts))
    #add extra payments to monthly income
    monthly_income += sum(debt1['extra_payment'] for debt1 in debts if debt1['amount'] > 0)
    
    avalanche_interests = []
    current_month = 0
    while any(debt['amount'] > 0 for debt in debts):
        month_data = []
        interest_data = []
        remaining_income = monthly_income
        for debt in debts:
            if debt['amount'] > 0 and (debt['months_to_maturity'] is None or debt['months_to_maturity'] > 0):
                # Calculate monthly interest & payment
                monthly_interest = debt['amount'] * (debt['interest_rate'] / 100 / 12)
                payment = min(remaining_income, debt['amount'] + monthly_interest)
                debt['amount'] -= (payment - monthly_interest)
                remaining_income -= payment

                # Decrement months to maturity
                if debt['months_to_maturity'] is not None:
                    debt['months_to_maturity'] -= 1
 
                # Prevent negative balances
                if debt['amount'] < 0:
                    debt['amount'] = 0

                # Add data to month
                month_data.append({
                    'debt_type': debt['debt_type'],
                    'remaining_balance': debt['amount'],
                    'months_to_maturity': debt.get('months_to_maturity', None)           
                })
                interest_data.append({
                    'debt_type': debt['debt_type'],
                    'interest': monthly_interest
                })
        avalanche_interests.append({
            'month': current_month,
            'interests': interest_data
        })

        # Stop if no progress is being made
        if not any(d['remaining_balance'] > 0 for d in month_data):
            break

        current_month += 1
        if current_month > 60:
            break
    return avalanche_interests

def get_repayment_timeline(debts, type = "avalanche", user_income = 0):
    '''
    This function creates a monthly repayment timeline that
    includes the relevant information about remaining debts
    over the months until all are paid off
    '''
    #Sort debts according to type
    if type == "avalanche":
        debts = get_avalanche_order(debts)
    elif type == "snowball":
        debts = get_snowball_order(debts)

    #get monthly income
    monthly_income = max(user_income, get_minimum_income_to_payoff(debts))
    #add extra payments to monthly income
    monthly_income += sum(debt1['extra_payment'] for debt1 in debts if debt1['amount'] > 0)
    
    timeline = []
    payment_timeline = []
    current_month = 0
    while any(debt['amount'] > 0 for debt in debts):
        month_data = []
        payment_data = []
        interest_data = []
        remaining_income = monthly_income
        for debt in debts:
            if debt['amount'] > 0 and (debt['months_to_maturity'] is None or debt['months_to_maturity'] > 0):
                # Calculate monthly interest & payment
                monthly_interest = debt['amount'] * (debt['interest_rate'] / 100 / 12)
                payment = min(remaining_income, debt['amount'] + monthly_interest)
                debt['amount'] -= (payment - monthly_interest)
                remaining_income -= payment

                # Decrement months to maturity
                if debt['months_to_maturity'] is not None:
                    debt['months_to_maturity'] -= 1
 
                # Prevent negative balances
                if debt['amount'] < 0:
                    debt['amount'] = 0

                # Add data to month
                month_data.append({
                    'debt_type': debt['debt_type'],
                    'remaining_balance': debt['amount'],
                    'months_to_maturity': debt.get('months_to_maturity', None)           
                })
                payment_data.append({
                    'debt_type': debt['debt_type'],
                    'payment_made': payment
                })
        timeline.append({
            'month': current_month,
            'debts': month_data
        })
        payment_timeline.append({
            'month': current_month,
            'payments': payment_data
        })

        # Stop if no progress is being made
        if not any(d['remaining_balance'] > 0 for d in month_data):
            break

        current_month += 1
        if current_month > 60:
            break
    return timeline, payment_timeline

def cumulate(key, data):
    '''
    This function takes in a dictionary of data and cumulates
    each value correlating to the key. It returns the updated
    dictionary.
    '''
    cumulative_sum = 0
    for item in data:
        if key in item:
            cumulative_sum += item[key]
            item[key] = cumulative_sum
    return data

def sum_interests(interests):
    '''
    This function takes in a dictionary including data on interests and
    sums the amount of interest generated each month. It returns a dictionary
    that includes "month" and "total interest"
    '''
    result = []
    for month_data in interests:
        month = month_data['month']
        total_interest = sum(debt['interest'] for debt in month_data['interests'])
        result.append({'month': month, 'total_interest': total_interest})
    return result


'''
GETTER FUNCTION <- this is the only thing user_interface needs from this program
'''

def get_timeline_payments_interests(debts, type = "avalanche", income = 0):
    '''
    This function returns timeline, payments, and interests in that order
    '''
    tmp_debts = []
    for val in debts:
        # Create a deep copy of val and append it to tmp_debts
        tmp_debts.append(copy.deepcopy(val))
    tmp_debts2 = []
    for val in debts:
        tmp_debts2.append(copy.deepcopy(val))
    timeline, payment_timeline = get_repayment_timeline(debts, type, income)
    
    interest_avalanche = get_avalanche_interests(tmp_debts, income)
    interest_snowball = get_snowball_interests(tmp_debts2, income)
    interest_avalanche = sum_interests(interest_avalanche)
    interest_avalanche = cumulate("total_interest", interest_avalanche)
    interest_snowball = sum_interests(interest_snowball)
    interest_snowball = cumulate("total_interest", interest_snowball)
    #--------------------------------------------------------------------
    #   TODO - subtract default interest from each month to get difference saved
    #--------------------------------------------------------------------
    return timeline, payment_timeline, interest_avalanche, interest_snowball

'''
TEST
'''

'''
print("-------------------------------------")
print("\n\n\n TESTING REPAYMENT LOGIC \n\n\n")
print("-------------------------------------")
debts = [
    {'debt_type': 'Credit Card', 'amount': 5000, 'interest_rate': 19.99, "extra_payment": 400, "months_to_maturity": None},
    {'debt_type': 'Auto Loan', 'amount': 12000, 'interest_rate': 4.99, "extra_payment": 400, "months_to_maturity": 60},
    {'debt_type': 'Student Loan', 'amount': 15000, 'interest_rate': 6.99, "extra_payment": 400, "months_to_maturity": 36},
    {"debt_type": "Personal Loan", "amount": 5000, "interest_rate": 8.99, "extra_payment": 400, "months_to_maturity": 24}
]
timeline = get_timeline_payments_interests(debts)
print(timeline)
'''
