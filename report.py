import sqlite3
import numpy as np

def total_revenue(cursor_bank):
    cursor_bank.execute('''
    SELECT SUM(amount) FROM bank
    WHERE description = 'deposit revenue'
    ''')
    revenue = cursor_bank.fetchone()[0]
    return revenue


def total_expense(cursor_bank):
    cursor_bank.execute('''
    SELECT SUM(amount) FROM bank
    WHERE description != 'deposit revenue' OR description != 'initial deposit'
    ''')
    expense = cursor_bank.fetchone()[0]
    return expense


def net_income(total_revenue, total_expense):
    return (total_revenue-total_expense)


def profit_margin(net_income, total_revenue):
    return (net_income/total_revenue)


def used_oven_capacity(cursor_bread, sim_days):
    cursor_bread.execute('''
    SELECT COUNT(DISTINCT batch) FROM bread
    ''')
    batches = cursor_bread.fetchone()[0]
    return np.round((batches/(10*sim_days)),2)


def customer_qty(cursor_sale):
    cursor_sale.execute('''
    SELECT COUNT(transaction_id) FROM sale
    ''')
    customers = cursor_sale.fetchone()[0]
    return customers


def order_demand(cursor_sale):
    cursor_sale.execute('''
    SELECT SUM(demand) FROM sale
    ''')
    demand = cursor_sale.fetchone()[0]
    return demand


def missed_orders(cursor_sale):
    cursor_sale.execute('''
    SELECT SUM(demand),SUM(purchased) FROM sale
    ''')
    ordered_purchased = cursor_sale.fetchone()
    return (ordered_purchased[0]-ordered_purchased[1])

def expired_loaves(cursor_bread):
    cursor_bread.execute('''
    SELECT COUNT(status) FROM bread
    WHERE status = 'expired'
    ''')
    expired = cursor_bread.fetchone()[0]
    return expired


def final_account_balance(cursor_bank):
    cursor_bank.execute('''
    SELECT balance FROM bank
    WHERE transaction_number = (SELECT MAX(transaction_number) FROM bank)
    ''')
    balance = cursor_bank.fetchone()[0]
    return balance


def total_credit_expense(cursor_bank):
    cursor_bank.execute('''
    SELECT SUM(amount) FROM bank
    WHERE description = 'credit expense'
    ''')
    credit_expense = cursor_bank.fetchone()[0]
    if credit_expense != None:
        return credit_expense
    else:
        return 0.0
    

def report_txt(cursor_sale, cursor_ingredients, cursor_bread,
               cursor_bank, sim_days, monthly_marketing_spend,
               bread_price, bread_cost, ingredient_buy_setpoint,
               ingredient_buy_qty, bake_batch_setpoint, db_name, 
               rent_expense, payroll_expense, starting_account_balance):
    revenue = total_revenue(cursor_bank)
    expense = total_expense(cursor_bank)
    income = net_income(revenue, expense)
    margin = profit_margin(income, revenue)
    text = f'''Sim Name: {db_name}\n
    Sim Days: {sim_days}\n
    Monthly Marketing Spend: ${monthly_marketing_spend:.2f}\n
    Bread Cost: ${bread_cost:.2f}\n
    Bread Price: ${bread_price:.2f}\n
    Ingredient Buy Setpoint: {ingredient_buy_setpoint}\n
    Ingredient Buy Qty: {ingredient_buy_qty}\n
    Bake Batch Setpoint: {bake_batch_setpoint}\n
    Starting Account Balance: ${starting_account_balance:.2f}\n
    Rent Expense: ${rent_expense:.2f}\n
    Payroll Expense: ${payroll_expense:.2f}\n 
    ------------------------------------------\n
    Total Revenue: ${revenue:.2f}\n
    Total Expense: ${expense:.2f}\n
    Net Income: ${income:.2f}\n
    Profit Margin: {(margin*100):.1f}%\n
    Final Account Balance: ${final_account_balance(cursor_bank):.2f}\n
    Total Credit Expense: ${total_credit_expense(cursor_bank):.2f}\n
    ------------------------------------------\n
    Average Daily Customers: {(customer_qty(cursor_sale)/sim_days):.0f}\n
    Average Order Size: {(order_demand(cursor_sale)/customer_qty(cursor_sale)):.1f}\n
    Average Missed Orders: {(missed_orders(cursor_sale)/sim_days):.1f}\n
    Used Oven Capacity: {(used_oven_capacity(cursor_bread, sim_days)*100):.1f}%\n
    Average Expired Loaves: {(expired_loaves(cursor_bread)/sim_days):.1f}
    '''
    return text