import sqlite3
import os

def create_db(file_path, db_name, connection_sale, connection_ingredients, connection_bread,
          connection_bank, cursor_sale,cursor_ingredients, cursor_bread, cursor_bank):
    
    cursor_sale.execute('''
        CREATE TABLE IF NOT EXISTS sale (
            transaction_id TEXT NOT NULL,
            transaction_number INTEGER NOT NULL,
            day INTEGER NOT NULL,
            time INTEGER NOT NULL,
            status TEXT NOT NULL,
            demand INTEGER NOT NULL,
            purchased INTEGER NOT NULL
        )
        ''')
    
    cursor_ingredients.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            transaction_id TEXT NOT NULL,
            transaction_number INTEGER NOT NULL,
            day INTEGER NOT NULL,
            time INTEGER NOT NULL,
            status TEXT NOT NULL,
            batch INTEGER NOT NULL
        )
        ''')
    
    cursor_bread.execute('''
        CREATE TABLE IF NOT EXISTS bread (
            transaction_id TEXT NOT NULL,
            transaction_number INTEGER NOT NULL,
            day INTEGER NOT NULL,
            time INTEGER NOT NULL,
            batch INTEGER NOT NULL,
            loaf INTEGER NOT NULL,
            status TEXT NOT NULL
        )
        ''')
    
    cursor_bank.execute('''
        CREATE TABLE IF NOT EXISTS bank (
            transaction_id TEXT NOT NULL,
            transaction_number INTEGER NOT NULL,
            day INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount FLOAT NOT NULL,
            balance FLOAT NOT NULL
        )
        ''')

    connection_sale.commit()
    connection_ingredients.commit()
    connection_bread.commit()
    connection_bank.commit()
