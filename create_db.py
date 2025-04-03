import sqlite3
import os
import shutil

def create_db(file_path, db_name, connection_sale, connection_purchase,
              connection_ingredients, connection_bread, connection_bank, cursor_sale,
              cursor_purchase, cursor_ingredients, cursor_bread, cursor_bank):
    
    try:
        os.makedirs(f'{file_path}/{db_name}', exist_ok=True)

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
        
        cursor_purchase.execute('''
            CREATE TABLE IF NOT EXISTS purchase (
                transaction_id TEXT NOT NULL,
                transaction_number INTEGER NOT NULL,
                day INTEGER NOT NULL,
                purchased_qty INTEGER NOT NULL,
                price FLOAT NOT NULL
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
        connection_purchase.commit()
        connection_ingredients.commit()
        connection_bread.commit()
        connection_bank.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def delete_db(file_path, db_name):
    try:
        directory_path = f"{file_path}/{db_name}"
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

    except Exception as e:
        print(f"An error occurred while deleting the directory: {e}")
