import sqlite3
import os
import shutil

file_path = f'{os.path.dirname(os.path.abspath(__file__))}/database'

def create_db(db_name):
    
    try:
        os.makedirs(f'{file_path}/{db_name}', exist_ok=True)

        conection_sale = sqlite3.connect(f'{file_path}/{db_name}/{db_name}_sale.db')
        conection_purchase = sqlite3.connect(f'{file_path}/{db_name}/{db_name}_purchase.db')
        conection_production = sqlite3.connect(f'{file_path}/{db_name}/{db_name}_production.db')
        conection_inventory = sqlite3.connect(f'{file_path}/{db_name}/{db_name}_inventory.db')
        conection_bank = sqlite3.connect(f'{file_path}/{db_name}/{db_name}_bank.db')

        cursor_sale = conection_sale.cursor()
        cursor_purchase = conection_purchase.cursor()
        cursor_production = conection_production.cursor()
        cursor_inventory = conection_inventory.cursor()
        cursor_bank = conection_bank.cursor()

        cursor_sale.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_number INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL
            )
            ''')
        
        cursor_purchase.execute('''
            CREATE TABLE IF NOT EXISTS purchase (
                purchase_number INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL
            )
            ''')
        cursor_production.execute('''
            CREATE TABLE IF NOT EXISTS production (
                production_number INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
            ''')
        
        cursor_inventory.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_number INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
            ''')
        
        cursor_bank.execute('''
            CREATE TABLE IF NOT EXISTS bank (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount DECIMAL(18, 2) NOT NULL,
                balance DECIMAL(18, 2) NOT NULL
            )
            ''')

        conection_sale.commit()
        conection_purchase.commit()
        conection_production.commit()
        conection_inventory.commit()
        conection_bank.commit()

        conection_sale.close()
        conection_purchase.close()
        conection_production.close()
        conection_inventory.close()
        conection_bank.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def delete_db(db_name):
    try:
        directory_path = f"{file_path}/{db_name}"
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

    except Exception as e:
        print(f"An error occurred while deleting the directory: {e}")
