from create_db import create_db
from order_generator import order_generator
from transactions import customer_purchase, bake_batch, purchase_ingredients, pay_bill, deposite_revenue
from operations import expired_batch, finished_bread, bread_check, ingredient_check, ingredient_delivery, purchase_ingredient_check, credit_expense, bread_sold, account_balance
import os
import sqlite3
import pandas as pd
import shutil

#################
# user inputs
db_name = 'test3'
sim_days = 31
monthly_marketing_spend = 1000.0 #dollars
bread_price = 2.50 #dollars
bread_cost = 1.50 #dollars
ingredient_buy_setpoint = 5 #available batches of ingredients
ingredient_buy_qty = 20 #batches of ingredients
bake_batch_setpoint = 10 #available loaves
#################

file_path = f'{os.path.dirname(os.path.abspath(__file__))}/database'
directory_path = f"{file_path}/{db_name}"
if os.path.exists(directory_path):
    shutil.rmtree(directory_path)
os.makedirs(directory_path, exist_ok=True)

connection_sale = sqlite3.connect(f'{directory_path}/sale.db')
connection_ingredients = sqlite3.connect(f'{directory_path}/ingredients.db')
connection_bread = sqlite3.connect(f'{directory_path}/bread.db')
connection_bank = sqlite3.connect(f'{directory_path}/bank.db')

cursor_sale = connection_sale.cursor()
cursor_ingredients = connection_ingredients.cursor()
cursor_bread = connection_bread.cursor()
cursor_bank = connection_bank.cursor()

create_db(file_path, db_name, connection_sale, connection_ingredients, connection_bread,
          connection_bank, cursor_sale,cursor_ingredients, cursor_bread, cursor_bank)

#add money to bank account
cursor_bank.execute('''
INSERT INTO bank (transaction_id, transaction_number, day, description, amount, balance)
VALUES (?,?,?,?,?,?)
''',('x',0,0,'initial deposite',10000.00,10000.00))

#pay initial bills
pay_bill(connection_bank, cursor_bank, 1, 0, 'marketing expense', monthly_marketing_spend)
pay_bill(connection_bank, cursor_bank, 2, 0, 'rent expense', 1500.00)

purchase_ingredients(connection_ingredients, cursor_ingredients, connection_bank, cursor_bank, 3, 0, ingredient_buy_qty, bread_cost)

transaction_number = 4

for day in range(1,(sim_days+1)):
    purchase_time = 0
    daily_orders = order_generator(monthly_marketing_spend, bread_price)
    ingredient_delivery(connection_ingredients, cursor_ingredients,day)
    expired_batch(connection_bread, cursor_bread, day, purchase_time)
    if bread_check(cursor_bread) <= bake_batch_setpoint and ingredient_check(cursor_ingredients) > 0 and purchase_time <= 540:
        bake_batch(connection_bread, cursor_bread, connection_ingredients, cursor_ingredients, transaction_number, day, purchase_time)
        transaction_number += 1
    for i in range(len(daily_orders)):
        purchase_time = int(daily_orders[i,0])
        purchase_qty = int(daily_orders[i,1])
        expired_batch(connection_bread, cursor_bread, day, purchase_time)
        finished_bread(connection_bread, cursor_bread, day, purchase_time)
        customer_purchase(connection_bread, cursor_bread, connection_sale, cursor_sale, transaction_number, day, purchase_time, purchase_qty)
        transaction_number += 1
        if bread_check(cursor_bread) <= bake_batch_setpoint and ingredient_check(cursor_ingredients) > 0 and purchase_time <= 540:
            bake_batch(connection_bread, cursor_bread, connection_ingredients, cursor_ingredients, transaction_number, day, purchase_time)
            transaction_number += 1
    if purchase_ingredient_check(cursor_ingredients) <= ingredient_buy_setpoint:
       purchase_ingredients(connection_ingredients, cursor_ingredients, connection_bank, cursor_bank, transaction_number, day, ingredient_buy_qty, bread_cost)
       transaction_number += 1
    deposite_revenue(connection_bank, cursor_bank, transaction_number, day, (bread_sold(cursor_sale, day)*bread_price))
    transaction_number += 1
    if (day % 7) == 0:
        pay_bill(connection_bank, cursor_bank, transaction_number, day, 'payroll expense', 700.00)
        transaction_number += 1
    if (day % 30) == 0:
        pay_bill(connection_bank, cursor_bank, transaction_number, day, 'marketing expense', monthly_marketing_spend)
        transaction_number += 1
        pay_bill(connection_bank, cursor_bank, transaction_number, day, 'rent expense', 1500.00)
        transaction_number += 1
        financing = credit_expense(cursor_bank)
        if financing != 0:
            pay_bill(connection_bank, cursor_bank, transaction_number, day, 'credit expense', financing)
            transaction_number += 1
    print(f'Day: {day}, Account Balance: ${account_balance(cursor_bank)}')

query_sale = 'SELECT * FROM sale'
query_ingredients = 'SELECT * FROM ingredients'
query_bread = 'SELECT * FROM bread'
query_bank = 'SELECT * FROM bank'

df_sale = pd.read_sql_query(query_sale, connection_sale)
df_ingredients = pd.read_sql_query(query_ingredients, connection_ingredients)
df_bread = pd.read_sql_query(query_bread, connection_bread)
df_bank = pd.read_sql_query(query_bank, connection_bank)

df_sale.to_excel(f'{directory_path}/sale.xlsx', index=False)
df_ingredients.to_excel(f'{directory_path}/ingredients.xlsx', index=False)
df_bread.to_excel(f'{directory_path}/bread.xlsx', index=False)
df_bank.to_excel(f'{directory_path}/bank.xlsx', index=False)

connection_sale.close()
connection_ingredients.close()
connection_bread.close()
connection_bank.close()

print('Program Complete')