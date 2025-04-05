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
        return 0