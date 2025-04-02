import sqlite3
import os
import shutil

file_path = f'{os.path.dirname(os.path.abspath(__file__))}/database'

def create_db(db_name):
    
    try:
        os.makedirs(f'{file_path}/{db_name}', exist_ok=True)

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

        connection_sale.close()
        connection_purchase.close()
        connection_ingredients.close()
        connection_bread.close()
        connection_bank.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def delete_db(db_name):
    try:
        directory_path = f"{file_path}/{db_name}"
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

    except Exception as e:
        print(f"An error occurred while deleting the directory: {e}")
