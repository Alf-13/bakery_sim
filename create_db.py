import sqlite3
import os
import shutil

def create_db(db_name):

    try:
        os.makedirs(f'database/{db_name}', exist_ok=True)

        conection_sale = sqlite3.connect(f'database/{db_name}/{db_name}_sale.db')
        conection_inventory = sqlite3.connect(f'database/{db_name}/{db_name}_inventory.db')
        conection_purchase = sqlite3.connect(f'database/{db_name}/{db_name}_purchase.db')
        conection_production = sqlite3.connect(f'database/{db_name}/{db_name}_production.db')

        cursor_sale = conection_sale.cursor()
        cursor_inventory = conection_inventory.cursor()
        cursor_purchase = conection_purchase.cursor()
        cursor_production = conection_production.cursor()

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
        cursor_inventory.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                location TEXT PRIMARY KEY,
                stow_date TEXT NOT NULL,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL
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

        conection_sale.commit()
        conection_inventory.commit()
        conection_purchase.commit()
        conection_production.commit()

        conection_sale.close()
        conection_inventory.close()
        conection_purchase.close()
        conection_production.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def delete_db(db_name):
    try:
        directory_path = f"database/{db_name}"
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

    except Exception as e:
        print(f"An error occurred while deleting the directory: {e}")
