import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 
import calendar
from datetime import datetime
from database import DatabaseApp

class DatabaseApp:
    def connect_db(self, db_name, user, password, host, port):
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            return self.conn
        except Exception as e:
            return None