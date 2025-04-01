import sqlite3
import os

def customer_purchase(cursor_bread, cursor_sale, transaction_number, day, time, status, demand):
    for i in range(demand):
        cursor_bread.execute('''
        SELECT MIN(batch), MIN(loaf)
        FROM bread
        WHERE "status" = "ready"
        ''')
        loaf_check = cursor_bread.fetchone()
        if loaf_check != None:
            cursor_bread.execute('''
            UPDATE bread
            SET "status" = ?
            WHERE "batch" = ? AND "loaf" = ?
            ''',(f's{transaction_number}', loaf_check[0], loaf_check[1]))
    

def bake_batch():


def purchase_ingredients():


def expired_batch():


def pay_bill():


def deposite_revenue():