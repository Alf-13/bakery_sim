import sqlite3

def expired_batch(connection_bread, cursor_bread, day, time):
    expiration_day = day-2
    cursor_bread.execute('''
    UPDATE bread
    SET "status" = "expired"
    WHERE "status" = "ready" AND ("day" < ? OR ("day" = ? AND "time" <= ?))
    ''',(expiration_day, expiration_day, time+60))
    connection_bread.commit()

def finished_bread(connection_bread, cursor_bread, day, time):
    cursor_bread.execute('''
    UPDATE bread
    SET "status" = "available"
    WHERE "status" = "baking" AND ("time" <= ? OR "day" < ?)
    ''',(time-60, day))
    connection_bread.commit()

def bread_check(cursor_bread):
    cursor_bread.execute('''
    SELECT COUNT(*) FROM bread
    WHERE "status" = "baking" OR "available"
    ''')
    bread_count = cursor_bread.fetchone()[0]
    return bread_count

def ingredient_check(cursor_ingredients):
    cursor_ingredients.execute('''
    SELECT COUNT(*) FROM ingredients
    WHERE "status" = "available"
    ''')
    ingredient_count = cursor_ingredients.fetchone()[0]
    return ingredient_count

def ingredient_delivery(connection_ingredients, cursor_ingredients, day):
    cursor_ingredients.execute('''
    UPDATE ingredients
    SET "status" = "available"
    WHERE "status" = "ordered" AND "day" <= ?
    ''',(day-2))
    connection_ingredients.commit()

def purchase_ingredient_check(cursor_ingredients):
    cursor_ingredients.execute('''
    SELECT COUNT(*) FROM ingredients
    WHERE "status" = "available" OR "ordered"
    ''')
    purchase_ingredient_count = cursor_ingredients.fetchone()[0]
    return purchase_ingredient_count

def credit_expense(cursor_bank):
    cursor_bank.execute('''
    SELECT balance FROM bank
    WHERE "transaction_number" = (SELECT MAX(transaction_number) FROM bank)
    ''')
    balance = cursor_bank.fetchone()[0]
    if balance < 0:
        expense = balance*(-0.02)
    else:
        expense = 0.0
    return expense

def bread_sold(cursor_sale, day):
    cursor_sale.execute('''
    SELECT SUM(purchased) FROM sale
    WHERE "day" = ?
    ''',(day))
    bread_sold_qty = cursor_sale.fetchone()[0]
    return bread_sold_qty