from create_db import create_db
from order_generator import order_generator
from transactions import customer_purchase, bake_batch, purchase_ingredients, pay_bill, deposite_revenue
from operations import expired_batch, finished_bread, bread_check, ingredient_check, ingredient_delivery, purchase_ingredient_check, credit_expense, bread_sold
import os
import sqlite3

#################
# user inputs
db_name = 'test1'
monthly_marketing_spend = 500.0 #dollars
bread_price = 2.50 #dollars
bread_cost = 1.50 #dollars
ingredient_buy_setpoint = 5 #available batches of ingredients
ingredient_buy_qty = 20 #batches of ingredients
bake_batch_setpoint = 10 #available loaves
#################

file_path = f'{os.path.dirname(os.path.abspath(__file__))}/database'

connection_sale = sqlite3.connect(f'{file_path}/{db_name}/sale.db')
connection_purchase = sqlite3.connect(f'{file_path}/{db_name}/purchase.db')
connection_ingredients = sqlite3.connect(f'{file_path}/{db_name}/ingredients.db')
connection_bread = sqlite3.connect(f'{file_path}/{db_name}/bread.db')
connection_bank = sqlite3.connect(f'{file_path}/{db_name}/bank.db')

cursor_sale = connection_sale.cursor()
cursor_purchase = connection_purchase.cursor()
cursor_ingredients = connection_ingredients.cursor()
cursor_bread = connection_bread.cursor()
cursor_bank = connection_bank.cursor()

create_db(file_path, db_name, connection_sale, connection_purchase,
            connection_ingredients, connection_bread, connection_bank, cursor_sale,
            cursor_purchase, cursor_ingredients, cursor_bread, cursor_bank)

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

for day in range(1,366):
    purchase_time = 0
    daily_orders = order_generator(monthly_marketing_spend, bread_price)
    ingredient_delivery(connection_ingredients, cursor_ingredients,day)
    expired_batch(connection_bread, cursor_bread, day, purchase_time)
    if bread_check(cursor_bread) <= bake_batch_setpoint and ingredient_check(cursor_ingredients) > 0 and purchase_time <= 540:
        bake_batch(connection_bread, cursor_bread, connection_ingredients, cursor_ingredients, transaction_number, day, purchase_time)
        transaction_number += 1
    for i in range(len(daily_orders)):
        purchase_time = daily_orders[i,0]
        purchase_qty = daily_orders[i,1]
        expired_batch(connection_bread, cursor_bread, day, purchase_time)
        finished_bread(connection_bread, cursor_bread, day, purchase_time)
        customer_purchase(connection_bread, cursor_bread, connection_sale, cursor_sale, transaction_number, day, purchase_time, purchase_qty)
        transaction_number += 1
        if bread_check(cursor_bread) <= bake_batch_setpoint and ingredient_check(cursor_ingredients) > 0 and purchase_time <= 540:
            bake_batch(connection_bread, cursor_bread, connection_ingredients, cursor_ingredients, transaction_number, day, purchase_time)
            transaction_number += 1
    if purchase_ingredient_check <= ingredient_buy_setpoint:
       purchase_ingredients(connection_ingredients, cursor_ingredients, connection_bank, cursor_bank, transaction_number, day, ingredient_buy_qty, bread_cost)
       transaction_number += 1
    deposite_revenue(connection_bank, cursor_bank, transaction_number, day, (bread_sold(cursor_sale, day)*bread_price))
    transaction_number += 1






connection_sale.close()
connection_purchase.close()
connection_ingredients.close()
connection_bread.close()
connection_bank.close()