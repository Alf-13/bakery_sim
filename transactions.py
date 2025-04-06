import sqlite3

oven_capacity = 25 #loaves

def customer_purchase(connection_bread, cursor_bread, connection_sale, cursor_sale, transaction_number, day, time, demand):
    missed_sale = 0
    for i in range(demand):
        cursor_bread.execute('''
        SELECT batch, loaf FROM bread
        WHERE status = 'available'
        ORDER BY batch, loaf
        LIMIT 1
        ''')
        loaf_check = cursor_bread.fetchone()
        if loaf_check:
            cursor_bread.execute('''
            UPDATE bread
            SET status = ?
            WHERE batch = ? AND loaf = ?
            ''',(f's{transaction_number}', loaf_check[0], loaf_check[1]))
        else:
            missed_sale += 1
    if missed_sale == 0:
        sale_status = 'filled'
    elif missed_sale == demand:
        sale_status = 'missed'
    else:
        sale_status = 'partial'
    cursor_sale.execute('''
    INSERT INTO sale (transaction_id, transaction_number, day, time, status, demand, purchased)
    VALUES (?,?,?,?,?,?,?)
    ''',('s', transaction_number, day, time, sale_status, demand, (demand-missed_sale)))
    connection_bread.commit()
    connection_sale.commit()
    

def bake_batch(connection_bread, cursor_bread, connection_ingredients, cursor_ingredients, transaction_number, day, time):
    cursor_bread.execute('''
    SELECT status FROM bread
    WHERE status = 'baking'
    ''')
    bake_check = cursor_bread.fetchone()
    if bake_check is None:
        cursor_ingredients.execute('''
        SELECT batch FROM ingredients
        WHERE status = 'available'
        ''')
        if cursor_ingredients.fetchone() != None:
            cursor_bread.execute('''
            SELECT MAX(batch) FROM bread
            ''')
            max_batch = cursor_bread.fetchone()[0]
            if max_batch != None:
                batch = max_batch+1
            else:
                batch = 1
            for i in range(1,(oven_capacity+1)):
                cursor_bread.execute('''
                INSERT INTO bread (transaction_id, transaction_number, day, time, batch, loaf, status)
                VALUES (?,?,?,?,?,?,?)
                ''',('b', transaction_number, day, time, batch, i, 'baking'))
            cursor_ingredients.execute('''
            UPDATE ingredients
            SET status = ?
            WHERE batch = (SELECT MIN(batch) FROM ingredients
                            WHERE status = 'available')
            ''',(f'b{transaction_number}',))
    connection_bread.commit()
    connection_ingredients.commit()


def purchase_ingredients(connection_ingredients, cursor_ingredients, connection_bank, cursor_bank, transaction_number, day, batch_qty, bread_cost):
    total_cost = batch_qty*oven_capacity*bread_cost
    cursor_ingredients.execute('''
    SELECT MAX(batch) FROM ingredients
    ''')
    max_batch = cursor_ingredients.fetchone()[0]
    if max_batch != None:
        batch = max_batch+1
    else:
        batch = 1
    for i in range(batch_qty):
        cursor_ingredients.execute('''
        INSERT INTO ingredients (transaction_id, transaction_number, day, time, status, batch)
        VALUES (?,?,?,?,?,?)
        ''',('i', transaction_number, day, 600, 'ordered', batch))
        batch += 1
    cursor_bank.execute('''
    SELECT balance FROM bank
    WHERE transaction_number = (SELECT MAX(transaction_number) FROM bank)
    ''')
    balance = cursor_bank.fetchone()[0]
    cursor_bank.execute('''
    INSERT INTO bank (transaction_id, transaction_number, day, description, amount, balance)
    VALUES (?,?,?,?,?,?)
    ''',('x', transaction_number, day, 'purchased ingredients', (-total_cost), (balance-total_cost)))
    connection_bank.commit()
    connection_ingredients.commit()    


def pay_bill(connection_bank, cursor_bank, transaction_number, day, description, amount):
    cursor_bank.execute('''
    SELECT balance FROM bank
    WHERE transaction_number = (SELECT MAX(transaction_number) FROM bank)
    ''')
    balance = cursor_bank.fetchone()[0]
    cursor_bank.execute('''
    INSERT INTO bank (transaction_id, transaction_number, day, description, amount, balance)
    VALUES (?,?,?,?,?,?)
    ''',('x', transaction_number, day, description, -amount, (balance-amount)))
    connection_bank.commit()


def deposit_revenue(connection_bank, cursor_bank, transaction_number, day, amount):
    cursor_bank.execute('''
    SELECT balance FROM bank
    WHERE transaction_number = (SELECT MAX(transaction_number) FROM bank)
    ''')
    balance = cursor_bank.fetchone()[0]
    cursor_bank.execute('''
    INSERT INTO bank (transaction_id, transaction_number, day, description, amount, balance)
    VALUES (?,?,?,?,?,?)
    ''',('x', transaction_number, day, 'deposit revenue', amount, (balance+amount)))
    connection_bank.commit()