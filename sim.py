import tkinter as tk
from tkinter import messagebox
import os
import sqlite3
from create_db import create_db, delete_db

script_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_dir, "database")

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.db_list = []

        # Input field
        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=10)

        # Bind the "Enter" key to the create_database function
        self.entry.bind("<Return>", lambda event: self.create_database())

        # Create Sim button
        self.create_button = tk.Button(self.root, text="Create Sim", command=self.create_database)
        self.create_button.pack()

        # Database list frame
        self.db_frame = tk.Frame(self.root)
        self.db_frame.pack(pady=20)

        self.update_db_list()

    def create_database(self):
        db_name = self.entry.get().strip()
        if db_name:
            if not os.path.exists(database_path):
                os.makedirs(database_path)
                print('Made database directory')
            create_db(db_name)  # Assumes create_db creates databases in the "database/" folder
            self.update_db_list()
            messagebox.showinfo("Success", f"Directory and databases for '{db_name}' created successfully!")
        else:
            messagebox.showerror("Error", "Please enter a valid database name.")


    def delete_database(self, db_name):
        delete_db(db_name)  # Call the updated delete function
        self.update_db_list()
        messagebox.showinfo("Success", f"Directory 'database/{db_name}' deleted successfully!")


    def update_db_list(self):
        # Clear the frame
        for widget in self.db_frame.winfo_children():
            widget.destroy()

        # Clear the current database list
        self.db_list = []

        # Check for directories inside the "database" folder
        if os.path.exists(database_path):
            print("Database path exists. Scanning for directories...")
            for folder in os.listdir(database_path):
                folder_path = os.path.join(database_path, folder)
                if os.path.isdir(folder_path):  # Ensure it's a directory
                    self.db_list.append(folder)

        # Display the updated list with delete buttons
        for db_name in self.db_list:
            frame = tk.Frame(self.db_frame)
            frame.pack(fill="x", pady=5)

            label = tk.Label(frame, text=db_name, width=30, anchor="w")
            label.pack(side="left", padx=10)

            delete_btn = tk.Button(frame, text="Delete", command=lambda name=db_name: self.delete_database(name))
            delete_btn.pack(side="right", padx=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()