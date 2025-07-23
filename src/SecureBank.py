import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import hashlib
from datetime import datetime
import re
#from fpdf import FPDF

class BankingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SecureBank")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f2f5')
        
        
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'white': '#ffffff'
        }
        
        self.current_user = None
        self.current_user_type = None
        
        self.setup_database()
        self.create_styles()
        self.show_login_screen()
        
    def setup_database(self):
        """Initialize the database with tables"""
        self.conn = sqlite3.connect('banking_system.db')
        self.cursor = self.conn.cursor()
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Accounts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                account_number TEXT UNIQUE NOT NULL,
                account_type TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        ''')
        
        # Employees table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL,
                position TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Loan requests table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS loan_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL NOT NULL,
                purpose TEXT NOT NULL,
                duration INTEGER NOT NULL,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin employee
        self.cursor.execute('''
            INSERT OR IGNORE INTO employees (username, password, full_name, employee_id, position)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', self.hash_password('admin123'), 'System Administrator', 'EMP001', 'Manager'))
        
        self.conn.commit()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_styles(self):
        """Create modern styling for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       padding=(20, 10),
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       padding=(15, 8),
                       font=('Arial', 9, 'bold'))
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       padding=(15, 8),
                       font=('Arial', 9, 'bold'))
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background='#f0f2f5',
                       foreground=self.colors['primary'],
                       font=('Arial', 24, 'bold'))
        
        style.configure('Heading.TLabel',
                       background='#f0f2f5',
                       foreground=self.colors['dark'],
                       font=('Arial', 16, 'bold'))
        
        style.configure('Info.TLabel',
                       background='#f0f2f5',
                       foreground=self.colors['dark'],
                       font=('Arial', 10))
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True)
        
        # Login container
        login_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
        
        # Title
        title_label = ttk.Label(login_frame, text="SecureBank ", style='Title.TLabel')
        title_label.pack(pady=(40, 20))
        
        # User type selection
        user_type_frame = tk.Frame(login_frame, bg='white')
        user_type_frame.pack(pady=10)
        
        self.user_type_var = tk.StringVar(value="customer")
        
        ttk.Radiobutton(user_type_frame, text="Customer", variable=self.user_type_var, 
                       value="customer").pack(side='left', padx=20)
        ttk.Radiobutton(user_type_frame, text="Employee", variable=self.user_type_var, 
                       value="employee").pack(side='left', padx=20)
        
        # Login form
        form_frame = tk.Frame(login_frame, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Username
        ttk.Label(form_frame, text="Username:", background='white').pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, font=('Arial', 12), width=25)
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        # Password
        ttk.Label(form_frame, text="Password:", background='white').pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, font=('Arial', 12), width=25, show='*')
        self.password_entry.pack(fill='x', pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(login_frame, bg='white')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", style='Primary.TButton',
                  command=self.login).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Register Customer", style='Success.TButton',
                  command=self.show_register_screen).pack(side='left', padx=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_type = self.user_type_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        hashed_password = self.hash_password(password)
        
        if user_type == "customer":
            self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                              (username, hashed_password))
            user = self.cursor.fetchone()
            if user:
                self.current_user = user[0]  # user ID
                self.current_user_type = "customer"
                self.show_customer_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        
        else:  # employee
            self.cursor.execute('SELECT * FROM employees WHERE username = ? AND password = ?',
                              (username, hashed_password))
            employee = self.cursor.fetchone()
            if employee:
                self.current_user = employee[0]  # employee ID
                self.current_user_type = "employee"
                self.show_employee_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
    
    def show_register_screen(self):
        """Display customer registration screen"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Registration form
        reg_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        reg_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Title
        ttk.Label(reg_frame, text="Customer Registration", style='Title.TLabel').pack(pady=20)
        
        # Form container
        form_container = tk.Frame(reg_frame, bg='white')
        form_container.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Left column
        left_frame = tk.Frame(form_container, bg='white')
        left_frame.pack(side='left', fill='both', expand=True, padx=20)
        
        # Right column
        right_frame = tk.Frame(form_container, bg='white')
        right_frame.pack(side='right', fill='both', expand=True, padx=20)
        
        # Registration fields
        self.reg_entries = {}
        
        # Left side fields
        left_fields = [('Username', 'username'), ('Password', 'password'), ('Full Name', 'full_name')]
        for label, key in left_fields:
            ttk.Label(left_frame, text=f"{label}:", background='white').pack(anchor='w', pady=(0, 5))
            entry = ttk.Entry(left_frame, font=('Arial', 12))
            if key == 'password':
                entry.config(show='*')
            entry.pack(fill='x', pady=(0, 15))
            self.reg_entries[key] = entry
        
        # Right side fields
        right_fields = [('Email', 'email'), ('Phone', 'phone'), ('Address', 'address')]
        for label, key in right_fields:
            ttk.Label(right_frame, text=f"{label}:", background='white').pack(anchor='w', pady=(0, 5))
            entry = ttk.Entry(right_frame, font=('Arial', 12))
            entry.pack(fill='x', pady=(0, 15))
            self.reg_entries[key] = entry
        
        # Buttons
        button_frame = tk.Frame(reg_frame, bg='white')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Register", style='Success.TButton',
                  command=self.register_customer).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Back to Login", style='Primary.TButton',
                  command=self.show_login_screen).pack(side='left', padx=10)
    
    def register_customer(self):
        """Handle customer registration"""
        data = {}
        for key, entry in self.reg_entries.items():
            data[key] = entry.get().strip()
        
        # Validation
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        if not re.match(r'^\d{10,15}$', data['phone']):
            messagebox.showerror("Error", "Phone number must be 10-15 digits")
            return
        
        try:
            # Insert user
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, email, phone, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['username'], self.hash_password(data['password']), 
                  data['full_name'], data['email'], data['phone'], data['address']))
            
            user_id = self.cursor.lastrowid
            
            # Create default account
            account_number = f"ACC{user_id:06d}"
            self.cursor.execute('''
                INSERT INTO accounts (user_id, account_number, account_type, balance)
                VALUES (?, ?, ?, ?)
            ''', (user_id, account_number, 'Savings', 0.0))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Account created successfully!\nAccount Number: {account_number}")
            self.show_login_screen()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
    
    def show_customer_dashboard(self):
        """Display customer dashboard"""
        self.clear_window()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # User info in header
        user_info = self.get_user_info()
        ttk.Label(header_frame, text=f"Welcome, {user_info['full_name']}", 
                 foreground='white', background=self.colors['primary'],
                 font=('Arial', 16, 'bold')).pack(side='left', padx=20, pady=20)
        
        ttk.Button(header_frame, text="Logout", style='Danger.TButton',
                  command=self.show_login_screen).pack(side='right', padx=20, pady=20)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left sidebar
        sidebar = tk.Frame(content_frame, bg='white', width=250, relief='raised', bd=1)
        sidebar.pack(side='left', fill='y', padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Sidebar buttons
        ttk.Label(sidebar, text="Account Management", style='Heading.TLabel').pack(pady=20)
        
        sidebar_buttons = [
            ("View Balance", self.show_balance),
            ("Transfer Money", self.show_transfer),
            ("Deposit Money", self.deposit_money),
            ("Withdraw Money", self.withdraw_money),
            ("Transaction History", self.show_transaction_history),
            ("Open New Account", self.create_new_account),
            ("Close Account", self.close_account),
            ("Account Details", self.show_account_details),
            ("Update Details", self.update_account_details),
            ("Request Loan", self.request_loan),
            ("Generate Statement", self.generate_statement),
            ("Change Password", self.change_password)
        ]
        
        for text, command in sidebar_buttons:
            ttk.Button(sidebar, text=text, style='Primary.TButton',
                      command=command).pack(pady=5, padx=20, fill='x')
        
        # Main content area
        self.main_content = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        self.main_content.pack(side='right', fill='both', expand=True)
        
        # Show default content
        self.show_balance()
    
    def show_employee_dashboard(self):
        """Display employee dashboard"""
        self.clear_window()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Employee info in header
        employee_info = self.get_employee_info()
        ttk.Label(header_frame, text=f"Employee: {employee_info['full_name']} ({employee_info['position']})", 
                 foreground='white', background=self.colors['primary'],
                 font=('Arial', 16, 'bold')).pack(side='left', padx=20, pady=20)
        
        ttk.Button(header_frame, text="Logout", style='Danger.TButton',
                  command=self.show_login_screen).pack(side='right', padx=20, pady=20)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left sidebar
        sidebar = tk.Frame(content_frame, bg='white', width=250, relief='raised', bd=1)
        sidebar.pack(side='left', fill='y', padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Sidebar buttons
        ttk.Label(sidebar, text="Bank Management", style='Heading.TLabel').pack(pady=20)
        
        sidebar_buttons = [
            ("All Customers", self.show_all_customers),
            ("All Accounts", self.show_all_accounts),
            ("All Transactions", self.show_all_transactions),
            ("Pending Loans", self.show_pending_loans),
            ("Create Employee", self.show_create_employee),
            ("Bank Statistics", self.show_bank_stats),
            ("Search", self.search_functionality),
            ("View Customer", self.view_customer_details),
            ("Freeze Account", self.freeze_account)
        ]
        
        for text, command in sidebar_buttons:
            ttk.Button(sidebar, text=text, style='Primary.TButton',
                      command=command).pack(pady=5, padx=20, fill='x')
        
        # Main content area
        self.main_content = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        self.main_content.pack(side='right', fill='both', expand=True)
        
        # Show default content
        self.show_bank_stats()
    
    def get_user_info(self):
        """Get current user information"""
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (self.current_user,))
        user = self.cursor.fetchone()
        return {
            'id': user[0],
            'username': user[1],
            'full_name': user[3],
            'email': user[4],
            'phone': user[5],
            'address': user[6]
        }
    
    def get_employee_info(self):
        """Get current employee information"""
        self.cursor.execute('SELECT * FROM employees WHERE id = ?', (self.current_user,))
        employee = self.cursor.fetchone()
        return {
            'id': employee[0],
            'username': employee[1],
            'full_name': employee[3],
            'employee_id': employee[4],
            'position': employee[5]
        }
    
    def clear_main_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def show_balance(self):
        """Show account balance"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Account Balance", style='Heading.TLabel').pack(pady=20)
        
        # Get user accounts
        self.cursor.execute('''
            SELECT account_number, account_type, balance 
            FROM accounts WHERE user_id = ?
        ''', (self.current_user,))
        accounts = self.cursor.fetchall()
        
        for account in accounts:
            account_frame = tk.Frame(self.main_content, bg=self.colors['light'], relief='raised', bd=1)
            account_frame.pack(pady=10, padx=20, fill='x')
            
            tk.Label(account_frame, text=f"Account: {account[0]}", 
                    bg=self.colors['light'], font=('Arial', 14, 'bold')).pack(pady=10)
            tk.Label(account_frame, text=f"Type: {account[1]}", 
                    bg=self.colors['light'], font=('Arial', 12)).pack()
            tk.Label(account_frame, text=f"Balance: ${account[2]:,.2f}", 
                    bg=self.colors['light'], font=('Arial', 16, 'bold'),
                    fg=self.colors['success']).pack(pady=10)
    
    def show_transfer(self):
        """Show money transfer form"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Transfer Money", style='Heading.TLabel').pack(pady=20)
        
        # Transfer form
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # From account
        ttk.Label(form_frame, text="From Account:", background='white').pack(anchor='w', pady=(0, 5))
        self.from_account_var = tk.StringVar()
        from_combo = ttk.Combobox(form_frame, textvariable=self.from_account_var, state='readonly')
        
        # Get user accounts
        self.cursor.execute('SELECT account_number, balance FROM accounts WHERE user_id = ?', 
                          (self.current_user,))
        accounts = self.cursor.fetchall()
        from_combo['values'] = [f"{acc[0]} (Balance: ${acc[1]:,.2f})" for acc in accounts]
        from_combo.pack(fill='x', pady=(0, 15))
        
        # To account
        ttk.Label(form_frame, text="To Account Number:", background='white').pack(anchor='w', pady=(0, 5))
        self.to_account_entry = ttk.Entry(form_frame, font=('Arial', 12))
        self.to_account_entry.pack(fill='x', pady=(0, 15))
        
        # Amount
        ttk.Label(form_frame, text="Amount:", background='white').pack(anchor='w', pady=(0, 5))
        self.amount_entry = ttk.Entry(form_frame, font=('Arial', 12))
        self.amount_entry.pack(fill='x', pady=(0, 15))
        
        # Description
        ttk.Label(form_frame, text="Description (Optional):", background='white').pack(anchor='w', pady=(0, 5))
        self.desc_entry = ttk.Entry(form_frame, font=('Arial', 12))
        self.desc_entry.pack(fill='x', pady=(0, 20))
        
        # Transfer button
        ttk.Button(form_frame, text="Transfer", style='Success.TButton',
                  command=self.process_transfer).pack()
    
    def process_transfer(self):
        """Process money transfer"""
        try:
            from_account = self.from_account_var.get().split(' ')[0]
            to_account = self.to_account_entry.get().strip()
            amount = float(self.amount_entry.get().strip())
            description = self.desc_entry.get().strip() or "Transfer"
            
            if not from_account or not to_account or amount <= 0:
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Check if accounts exist and get balances
            self.cursor.execute('SELECT id, balance FROM accounts WHERE account_number = ?', (from_account,))
            from_acc = self.cursor.fetchone()
            
            self.cursor.execute('SELECT id FROM accounts WHERE account_number = ?', (to_account,))
            to_acc = self.cursor.fetchone()
            
            if not from_acc or not to_acc:
                messagebox.showerror("Error", "Invalid account number")
                return
            
            if from_acc[1] < amount:
                messagebox.showerror("Error", "Insufficient funds")
                return
            
            # Process transfer
            self.cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', 
                              (amount, from_acc[0]))
            self.cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', 
                              (amount, to_acc[0]))
            
            # Record transactions
            self.cursor.execute('''
                INSERT INTO transactions (account_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (from_acc[0], 'Transfer Out', -amount, f"Transfer to {to_account}: {description}"))
            
            self.cursor.execute('''
                INSERT INTO transactions (account_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (to_acc[0], 'Transfer In', amount, f"Transfer from {from_account}: {description}"))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Transfer of ${amount:,.2f} completed successfully")
            self.show_balance()
            
        except Exception as e:
            messagebox.showerror("Error", f"Transfer failed: {str(e)}")
    
    def show_transaction_history(self):
        """Show transaction history"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Transaction History", style='Heading.TLabel').pack(pady=20)
        
        # Create treeview
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        columns = ('Date', 'Type', 'Amount', 'Description')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Get transactions
        self.cursor.execute('''
            SELECT t.timestamp, t.transaction_type, t.amount, t.description
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.user_id = ?
            ORDER BY t.timestamp DESC
        ''', (self.current_user,))
        
        transactions = self.cursor.fetchall()
        
        for transaction in transactions:
            date = datetime.strptime(transaction[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            amount_str = f"${transaction[2]:,.2f}" if transaction[2] >= 0 else f"-${abs(transaction[2]):,.2f}"
            tree.insert('', 'end', values=(date, transaction[1], amount_str, transaction[3]))
        
        tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def show_account_details(self):
        """Show account details"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Account Details", style='Heading.TLabel').pack(pady=20)
        
        user_info = self.get_user_info()
        
        details_frame = tk.Frame(self.main_content, bg=self.colors['light'], relief='raised', bd=1)
        details_frame.pack(pady=20, padx=40, fill='x')
        
        details = [
            ('Full Name', user_info['full_name']),
            ('Username', user_info['username']),
            ('Email', user_info['email']),
            ('Phone', user_info['phone']),
            ('Address', user_info['address'])
        ]
        
        for label, value in details:
            row_frame = tk.Frame(details_frame, bg=self.colors['light'])
            row_frame.pack(fill='x', pady=10, padx=20)
            
            tk.Label(row_frame, text=f"{label}:", bg=self.colors['light'], 
                    font=('Arial', 12, 'bold')).pack(side='left')
            tk.Label(row_frame, text=value, bg=self.colors['light'], 
                    font=('Arial', 12)).pack(side='right')
    
    def show_all_customers(self):
        """Show all customers (employee view)"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="All Customers", style='Heading.TLabel').pack(pady=20)
        
        # Create treeview
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        columns = ('ID', 'Username', 'Full Name', 'Email', 'Phone', 'Joined')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Get all customers
        self.cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        customers = self.cursor.fetchall()
        
        for customer in customers:
            joined_date = datetime.strptime(customer[7], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            tree.insert('', 'end', values=(customer[0], customer[1], customer[3], 
                                         customer[4], customer[5], joined_date))
        
        tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def show_all_accounts(self):
        """Show all accounts (employee view)"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="All Accounts", style='Heading.TLabel').pack(pady=20)
        
        # Create treeview
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        columns = ('Account No', 'Customer', 'Type', 'Balance', 'Created')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Get all accounts with customer names
        self.cursor.execute('''
            SELECT a.account_number, u.full_name, a.account_type, a.balance, a.created_at
            FROM accounts a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.created_at DESC
        ''')
        accounts = self.cursor.fetchall()
        
        for account in accounts:
            created_date = datetime.strptime(account[4], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            tree.insert('', 'end', values=(account[0], account[1], account[2], 
                                         f"${account[3]:,.2f}", created_date))
        
        tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def show_all_transactions(self):
        """Show all transactions (employee view)"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="All Transactions", style='Heading.TLabel').pack(pady=20)
        
        # Create treeview
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        columns = ('Date', 'Account', 'Customer', 'Type', 'Amount', 'Description')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Get all transactions with account and customer info
        self.cursor.execute('''
            SELECT t.timestamp, a.account_number, u.full_name, t.transaction_type, 
                   t.amount, t.description
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN users u ON a.user_id = u.id
            ORDER BY t.timestamp DESC
            LIMIT 100
        ''')
        transactions = self.cursor.fetchall()
        
        for transaction in transactions:
            date = datetime.strptime(transaction[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            amount_str = f"${transaction[4]:,.2f}" if transaction[4] >= 0 else f"-${abs(transaction[4]):,.2f}"
            tree.insert('', 'end', values=(date, transaction[1], transaction[2], 
                                         transaction[3], amount_str, transaction[5]))
        
        tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def show_create_employee(self):
        """Show create employee form"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Create New Employee", style='Heading.TLabel').pack(pady=20)
        
        # Employee form
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Form fields
        self.emp_entries = {}
        
        fields = [
            ('Username', 'username'),
            ('Password', 'password'),
            ('Full Name', 'full_name'),
            ('Employee ID', 'employee_id'),
            ('Position', 'position')
        ]
        
        for label, key in fields:
            ttk.Label(form_frame, text=f"{label}:", background='white').pack(anchor='w', pady=(0, 5))
            entry = ttk.Entry(form_frame, font=('Arial', 12))
            if key == 'password':
                entry.config(show='*')
            entry.pack(fill='x', pady=(0, 15))
            self.emp_entries[key] = entry
        
        # Create button
        ttk.Button(form_frame, text="Create Employee", style='Success.TButton',
                  command=self.create_employee).pack(pady=20)
    
    def create_employee(self):
        """Create new employee"""
        data = {}
        for key, entry in self.emp_entries.items():
            data[key] = entry.get().strip()
        
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO employees (username, password, full_name, employee_id, position)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['username'], self.hash_password(data['password']), 
                  data['full_name'], data['employee_id'], data['position']))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Employee created successfully!")
            
            # Clear form
            for entry in self.emp_entries.values():
                entry.delete(0, 'end')
                
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or Employee ID already exists")
    
    def show_bank_stats(self):
        """Show bank statistics"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Bank Statistics", style='Heading.TLabel').pack(pady=20)
        
        # Statistics container
        stats_container = tk.Frame(self.main_content, bg='white')
        stats_container.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Get statistics
        self.cursor.execute('SELECT COUNT(*) FROM users')
        total_customers = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM accounts')
        total_accounts = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT SUM(balance) FROM accounts')
        total_deposits = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute('SELECT COUNT(*) FROM transactions')
        total_transactions = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM employees')
        total_employees = self.cursor.fetchone()[0]
        
        # Create stat cards
        stats = [
            ('Total Customers', total_customers, self.colors['secondary']),
            ('Total Accounts', total_accounts, self.colors['success']),
            ('Total Deposits', f"${total_deposits:,.2f}", self.colors['warning']),
            ('Total Transactions', total_transactions, self.colors['danger']),
            ('Total Employees', total_employees, self.colors['dark'])
        ]
        
        # Create grid of stat cards
        row_frame = None
        for i, (label, value, color) in enumerate(stats):
            if i % 2 == 0:  # Start new row
                row_frame = tk.Frame(stats_container, bg='white')
                row_frame.pack(fill='x', pady=10)
            
            # Stat card
            card = tk.Frame(row_frame, bg=color, relief='raised', bd=2)
            card.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            
            tk.Label(card, text=str(value), bg=color, fg='white',
                    font=('Arial', 24, 'bold')).pack(pady=(20, 5))
            tk.Label(card, text=label, bg=color, fg='white',
                    font=('Arial', 12)).pack(pady=(0, 20))
        
        # Recent activity
        ttk.Label(stats_container, text="Recent Transactions", 
                 style='Heading.TLabel').pack(pady=(40, 20))
        
        # Recent transactions table
        recent_frame = tk.Frame(stats_container)
        recent_frame.pack(fill='both', expand=True, padx=20)
        
        columns = ('Date', 'Customer', 'Type', 'Amount')
        recent_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            recent_tree.heading(col, text=col)
            recent_tree.column(col, width=150)
        
        # Get recent transactions
        self.cursor.execute('''
            SELECT t.timestamp, u.full_name, t.transaction_type, t.amount
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN users u ON a.user_id = u.id
            ORDER BY t.timestamp DESC
            LIMIT 10
        ''')
        recent_transactions = self.cursor.fetchall()
        
        for transaction in recent_transactions:
            date = datetime.strptime(transaction[0], '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M')
            amount_str = f"${transaction[3]:,.2f}" if transaction[3] >= 0 else f"-${abs(transaction[3]):,.2f}"
            recent_tree.insert('', 'end', values=(date, transaction[1], 
                                                transaction[2], amount_str))
        
        recent_tree.pack(fill='both', expand=True)
    
    def create_new_account(self):
        """Allow customer to create a new account"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Open New Account", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Account type selection
        ttk.Label(form_frame, text="Account Type:", background='white').pack(anchor='w', pady=(0, 5))
        self.new_account_type = tk.StringVar(value="Savings")
        ttk.Combobox(form_frame, textvariable=self.new_account_type, 
                    values=["Savings", "Checking", "Business"], state='readonly').pack(fill='x', pady=(0, 15))
        
        # Initial deposit
        ttk.Label(form_frame, text="Initial Deposit:", background='white').pack(anchor='w', pady=(0, 5))
        self.initial_deposit = ttk.Entry(form_frame, font=('Arial', 12))
        self.initial_deposit.pack(fill='x', pady=(0, 20))
        
        # Create button
        ttk.Button(form_frame, text="Create Account", style='Success.TButton',
                 command=self.process_new_account).pack()

    def process_new_account(self):
        """Process the creation of a new account"""
        try:
            account_type = self.new_account_type.get()
            initial_deposit = float(self.initial_deposit.get().strip())
            
            if initial_deposit < 0:
                messagebox.showerror("Error", "Initial deposit cannot be negative")
                return
                
            # Generate account number
            self.cursor.execute('SELECT COUNT(*) FROM accounts WHERE user_id = ?', (self.current_user,))
            account_count = self.cursor.fetchone()[0] + 1
            account_number = f"ACC{self.current_user:04d}-{account_count:02d}"
            
            # Create account
            self.cursor.execute('''
                INSERT INTO accounts (user_id, account_number, account_type, balance)
                VALUES (?, ?, ?, ?)
            ''', (self.current_user, account_number, account_type, initial_deposit))
            
            # Record initial deposit transaction
            account_id = self.cursor.lastrowid
            self.cursor.execute('''
                INSERT INTO transactions (account_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (account_id, 'Deposit', initial_deposit, 'Initial deposit'))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"New {account_type} account created successfully!\nAccount Number: {account_number}")
            self.show_balance()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Account creation failed: {str(e)}")

    def close_account(self):
        """Allow customer to close an account"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Close Account", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Account selection
        ttk.Label(form_frame, text="Select Account to Close:", background='white').pack(anchor='w', pady=(0, 5))
        self.account_to_close = tk.StringVar()
        
        # Get user accounts with balances
        self.cursor.execute('SELECT account_number, balance FROM accounts WHERE user_id = ?', (self.current_user,))
        accounts = self.cursor.fetchall()
        
        if len(accounts) <= 1:
            messagebox.showerror("Error", "You must have at least one account open")
            self.show_balance()
            return
            
        account_combo = ttk.Combobox(form_frame, textvariable=self.account_to_close, state='readonly')
        account_combo['values'] = [f"{acc[0]} (Balance: ${acc[1]:,.2f})" for acc in accounts]
        account_combo.pack(fill='x', pady=(0, 15))
        
        # Transfer balance to
        ttk.Label(form_frame, text="Transfer Balance To:", background='white').pack(anchor='w', pady=(0, 5))
        self.transfer_to_account = tk.StringVar()
        
        # Get other accounts
        other_accounts = [acc[0] for acc in accounts if acc[0] != self.account_to_close.get().split(' ')[0]]
        transfer_combo = ttk.Combobox(form_frame, textvariable=self.transfer_to_account, state='readonly')
        transfer_combo['values'] = other_accounts
        transfer_combo.pack(fill='x', pady=(0, 20))
        
        # Close button
        ttk.Button(form_frame, text="Close Account", style='Danger.TButton',
                 command=self.process_close_account).pack()

    def process_close_account(self):
        """Process account closure"""
        try:
            account_to_close = self.account_to_close.get().split(' ')[0]
            transfer_to_account = self.transfer_to_account.get()
            
            if not account_to_close or not transfer_to_account:
                messagebox.showerror("Error", "Please select both accounts")
                return
                
            # Get account details
            self.cursor.execute('SELECT id, balance FROM accounts WHERE account_number = ?', (account_to_close,))
            closing_account = self.cursor.fetchone()
            
            self.cursor.execute('SELECT id FROM accounts WHERE account_number = ?', (transfer_to_account,))
            receiving_account = self.cursor.fetchone()
            
            if not closing_account or not receiving_account:
                messagebox.showerror("Error", "Invalid account selection")
                return
                
            # Transfer balance
            if closing_account[1] > 0:
                self.cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', 
                                  (closing_account[1], receiving_account[0]))
                self.cursor.execute('''
                    INSERT INTO transactions (account_id, transaction_type, amount, description)
                    VALUES (?, ?, ?, ?)
                ''', (receiving_account[0], 'Transfer In', closing_account[1], 
                      f"Balance transfer from closed account {account_to_close}"))
            
            # Record closure transaction
            self.cursor.execute('''
                INSERT INTO transactions (account_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (closing_account[0], 'Account Closure', -closing_account[1], 
                 f"Account closed, balance transferred to {transfer_to_account}"))
            
            # Delete account
            self.cursor.execute('DELETE FROM accounts WHERE id = ?', (closing_account[0],))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Account {account_to_close} closed successfully")
            self.show_balance()
            
        except Exception as e:
            messagebox.showerror("Error", f"Account closure failed: {str(e)}")

    def update_account_details(self):
        """Allow customer to update their personal information"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Update Account Details", style='Heading.TLabel').pack(pady=20)
        
        user_info = self.get_user_info()
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Form fields
        self.update_entries = {}
        
        fields = [
            ('Full Name', 'full_name', user_info['full_name']),
            ('Email', 'email', user_info['email']),
            ('Phone', 'phone', user_info['phone']),
            ('Address', 'address', user_info['address'])
        ]
        
        for label, key, value in fields:
            ttk.Label(form_frame, text=f"{label}:", background='white').pack(anchor='w', pady=(0, 5))
            entry = ttk.Entry(form_frame, font=('Arial', 12))
            entry.insert(0, value)
            entry.pack(fill='x', pady=(0, 15))
            self.update_entries[key] = entry
        
        # Update button
        ttk.Button(form_frame, text="Update Details", style='Success.TButton',
                  command=self.process_update_details).pack(pady=20)

    def process_update_details(self):
        """Process account details update"""
        data = {}
        for key, entry in self.update_entries.items():
            data[key] = entry.get().strip()
        
        # Validation
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
            messagebox.showerror("Error", "Invalid email format")
            return
            
        if not re.match(r'^\d{10,15}$', data['phone']):
            messagebox.showerror("Error", "Phone number must be 10-15 digits")
            return
            
        try:
            self.cursor.execute('''
                UPDATE users SET full_name = ?, email = ?, phone = ?, address = ?
                WHERE id = ?
            ''', (data['full_name'], data['email'], data['phone'], 
                 data['address'], self.current_user))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Account details updated successfully")
            self.show_account_details()
            
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    def deposit_money(self):
        """Dedicated deposit function"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Deposit Money", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Account selection
        ttk.Label(form_frame, text="Select Account:", background='white').pack(anchor='w', pady=(0, 5))
        self.deposit_account = tk.StringVar()
        
        self.cursor.execute('SELECT account_number FROM accounts WHERE user_id = ?', (self.current_user,))
        accounts = [acc[0] for acc in self.cursor.fetchall()]
        
        account_combo = ttk.Combobox(form_frame, textvariable=self.deposit_account, state='readonly')
        account_combo['values'] = accounts
        account_combo.pack(fill='x', pady=(0, 15))
        
        # Amount
        ttk.Label(form_frame, text="Amount:", background='white').pack(anchor='w', pady=(0, 5))
        self.deposit_amount = ttk.Entry(form_frame, font=('Arial', 12))
        self.deposit_amount.pack(fill='x', pady=(0, 15))
        
        # Description
        ttk.Label(form_frame, text="Description:", background='white').pack(anchor='w', pady=(0, 5))
        self.deposit_desc = ttk.Entry(form_frame, font=('Arial', 12))
        self.deposit_desc.pack(fill='x', pady=(0, 20))
        
        # Deposit button
        ttk.Button(form_frame, text="Deposit", style='Success.TButton',
                  command=self.process_deposit).pack()

    def process_deposit(self):
        """Process money deposit"""
        try:
            account_number = self.deposit_account.get()
            amount = float(self.deposit_amount.get().strip())
            description = self.deposit_desc.get().strip() or "Deposit"
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            # Get account ID
            self.cursor.execute('SELECT id FROM accounts WHERE account_number = ?', (account_number,))
            account = self.cursor.fetchone()
            
            if not account:
                messagebox.showerror("Error", "Invalid account selection")
                return
                
            # Update balance
            self.cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', 
                              (amount, account[0]))
            
            # Record transaction
            self.cursor.execute('''
                INSERT INTO transactions (account_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (account[0], 'Deposit', amount, description))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Deposit of ${amount:,.2f} completed successfully")
            self.show_balance()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Deposit failed: {str(e)}")

    def withdraw_money(self):
        """Dedicated withdrawal function"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Withdraw Money", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Account selection
        ttk.Label(form_frame, text="Select Account:", background='white').pack(anchor='w', pady=(0, 5))
        self.withdraw_account = tk.StringVar()
        
        self.cursor.execute('SELECT account_number, balance FROM accounts WHERE user_id = ?', (self.current_user,))
        accounts = self.cursor.fetchall()
        
        account_combo = ttk.Combobox(form_frame, textvariable=self.withdraw_account, state='readonly')
        account_combo['values'] = [f"{acc[0]} (Balance: ${acc[1]:,.2f})" for acc in accounts]
        account_combo.pack(fill='x', pady=(0, 15))
        
        # Amount
        ttk.Label(form_frame, text="Amount:", background='white').pack(anchor='w', pady=(0, 5))
        self.withdraw_amount = ttk.Entry(form_frame, font=('Arial', 12))
        self.withdraw_amount.pack(fill='x', pady=(0, 15))
        
        # Description
        ttk.Label(form_frame, text="Description:", background='white').pack(anchor='w', pady=(0, 5))
        self.withdraw_desc = ttk.Entry(form_frame, font=('Arial', 12))
        self.withdraw_desc.pack(fill='x', pady=(0, 20))
        
        # Withdraw button
        ttk.Button(form_frame, text="Withdraw", style='Danger.TButton',
                  command=self.process_withdrawal).pack()

    def process_withdrawal(self):
        """Process money withdrawal"""
        try:
            account_number = self.withdraw_account.get().split(' ')[0]
            amount = float(self.withdraw_amount.get().strip())
            description = self.withdraw_desc.get().strip() or "Withdrawal"
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            # Get account balance
            self.cursor.execute('SELECT id, balance FROM accounts WHERE account_number = ?', (account_number,))
            account = self.cursor.fetchone()
            
            if not account:
                messagebox.showerror("Error", "Invalid account selection")
                return
                
            if account[1] < amount:
                messagebox.showerror("Error", "Insufficient funds")
                return
                
            # Update balance
            self.cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', 
                              (amount, account[0]))
            
            # Record transaction
            self.cursor.execute('''
                INSERT INTO transactions (account_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (account[0], 'Withdrawal', -amount, description))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Withdrawal of ${amount:,.2f} completed successfully")
            self.show_balance()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Withdrawal failed: {str(e)}")

    def request_loan(self):
        """Loan application system"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Loan Application", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Loan amount
        ttk.Label(form_frame, text="Loan Amount:", background='white').pack(anchor='w', pady=(0, 5))
        self.loan_amount = ttk.Entry(form_frame, font=('Arial', 12))
        self.loan_amount.pack(fill='x', pady=(0, 15))
        
        # Purpose
        ttk.Label(form_frame, text="Purpose:", background='white').pack(anchor='w', pady=(0, 5))
        self.loan_purpose = ttk.Entry(form_frame, font=('Arial', 12))
        self.loan_purpose.pack(fill='x', pady=(0, 15))
        
        # Duration (months)
        ttk.Label(form_frame, text="Duration (months):", background='white').pack(anchor='w', pady=(0, 5))
        self.loan_duration = ttk.Combobox(form_frame, values=[6, 12, 24, 36, 48, 60], state='readonly')
        self.loan_duration.set(12)
        self.loan_duration.pack(fill='x', pady=(0, 20))
        
        # Submit button
        ttk.Button(form_frame, text="Submit Application", style='Primary.TButton',
                  command=self.process_loan_request).pack()

    def process_loan_request(self):
        """Process loan application"""
        try:
            amount = float(self.loan_amount.get().strip())
            purpose = self.loan_purpose.get().strip()
            duration = int(self.loan_duration.get())
            
            if amount <= 0:
                messagebox.showerror("Error", "Loan amount must be positive")
                return
                
            if not purpose:
                messagebox.showerror("Error", "Please specify loan purpose")
                return
                
            # Save loan request
            self.cursor.execute('''
                INSERT INTO loan_requests (user_id, amount, purpose, duration)
                VALUES (?, ?, ?, ?)
            ''', (self.current_user, amount, purpose, duration))
            
            self.conn.commit()
            messagebox.showinfo("Success", 
                             f"Loan application submitted for ${amount:,.2f}\n" +
                             f"Purpose: {purpose}\nDuration: {duration} months\n\n" +
                             "An employee will review your application shortly.")
            self.show_customer_dashboard()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid loan details")
        except Exception as e:
            messagebox.showerror("Error", f"Loan application failed: {str(e)}")

    def show_pending_loans(self):
        """Show pending loan requests (employee view)"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Pending Loan Requests", style='Heading.TLabel').pack(pady=20)
        
        # Create treeview
        tree_frame = tk.Frame(self.main_content)
        tree_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        columns = ('ID', 'Customer', 'Amount', 'Purpose', 'Duration', 'Requested')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Get pending loans with customer info
        self.cursor.execute('''
            SELECT l.id, u.full_name, l.amount, l.purpose, l.duration, l.created_at
            FROM loan_requests l
            JOIN users u ON l.user_id = u.id
            WHERE l.status = 'Pending'
            ORDER BY l.created_at
        ''')
        loans = self.cursor.fetchall()
        
        for loan in loans:
            requested_date = datetime.strptime(loan[5], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            tree.insert('', 'end', values=(loan[0], loan[1], f"${loan[2]:,.2f}", 
                       loan[3], f"{loan[4]} months", requested_date))
        
        tree.pack(fill='both', expand=True)
        
        # Action buttons frame
        action_frame = tk.Frame(self.main_content)
        action_frame.pack(pady=20)
        
        ttk.Label(action_frame, text="Loan ID:").pack(side='left')
        loan_id_entry = ttk.Entry(action_frame, width=10)
        loan_id_entry.pack(side='left', padx=5)
        
        def approve_loan():
            try:
                loan_id = int(loan_id_entry.get())
                self.cursor.execute('SELECT * FROM loan_requests WHERE id = ?', (loan_id,))
                loan = self.cursor.fetchone()
                
                if not loan:
                    messagebox.showerror("Error", "Invalid loan ID")
                    return
                
                # Get customer's main account
                self.cursor.execute('''
                    SELECT id FROM accounts 
                    WHERE user_id = ? AND account_type = 'Savings'
                    LIMIT 1
                ''', (loan[1],))
                account = self.cursor.fetchone()
                
                if not account:
                    messagebox.showerror("Error", "Customer has no savings account")
                    return
                
                # Update loan status
                self.cursor.execute('''
                    UPDATE loan_requests SET status = 'Approved'
                    WHERE id = ?
                ''', (loan_id,))
                
                # Deposit loan amount
                self.cursor.execute('''
                    UPDATE accounts SET balance = balance + ?
                    WHERE id = ?
                ''', (loan[2], account[0]))
                
                # Record transaction
                self.cursor.execute('''
                    INSERT INTO transactions (account_id, transaction_type, amount, description)
                    VALUES (?, ?, ?, ?)
                ''', (account[0], 'Loan Deposit', loan[2], f"Loan approval for {loan[3]}"))
                
                self.conn.commit()
                messagebox.showinfo("Success", f"Loan #{loan_id} approved and funds deposited")
                self.show_pending_loans()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid loan ID")
            except Exception as e:
                messagebox.showerror("Error", f"Loan approval failed: {str(e)}")
        
        def reject_loan():
            try:
                loan_id = int(loan_id_entry.get())
                self.cursor.execute('SELECT * FROM loan_requests WHERE id = ?', (loan_id,))
                loan = self.cursor.fetchone()
                
                if not loan:
                    messagebox.showerror("Error", "Invalid loan ID")
                    return
                
                # Update loan status
                self.cursor.execute('''
                    UPDATE loan_requests SET status = 'Rejected'
                    WHERE id = ?
                ''', (loan_id,))
                
                self.conn.commit()
                messagebox.showinfo("Success", f"Loan #{loan_id} rejected")
                self.show_pending_loans()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid loan ID")
            except Exception as e:
                messagebox.showerror("Error", f"Loan rejection failed: {str(e)}")
        
        ttk.Button(action_frame, text="Approve", style='Success.TButton',
                  command=approve_loan).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Reject", style='Danger.TButton',
                  command=reject_loan).pack(side='left', padx=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def freeze_account(self):
        """Employee function to freeze/unfreeze accounts"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="Account Freeze/Unfreeze", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Account selection
        ttk.Label(form_frame, text="Account Number:", background='white').pack(anchor='w', pady=(0, 5))
        self.freeze_account_entry = ttk.Entry(form_frame, font=('Arial', 12))
        self.freeze_account_entry.pack(fill='x', pady=(0, 15))
        
        # Action selection
        ttk.Label(form_frame, text="Action:", background='white').pack(anchor='w', pady=(0, 5))
        self.freeze_action = tk.StringVar(value="freeze")
        ttk.Radiobutton(form_frame, text="Freeze", variable=self.freeze_action, 
                       value="freeze").pack(anchor='w')
        ttk.Radiobutton(form_frame, text="Unfreeze", variable=self.freeze_action, 
                       value="unfreeze").pack(anchor='w')
        
        # Submit button
        ttk.Button(form_frame, text="Submit", style='Primary.TButton',
                  command=self.process_freeze).pack(pady=20)

    def process_freeze(self):
        """Process account freeze/unfreeze"""
        account_number = self.freeze_account_entry.get().strip()
        action = self.freeze_action.get()
        
        if not account_number:
            messagebox.showerror("Error", "Please enter an account number")
            return
            
        try:
            # Check if account exists
            self.cursor.execute('SELECT id FROM accounts WHERE account_number = ?', (account_number,))
            account = self.cursor.fetchone()
            
            if not account:
                messagebox.showerror("Error", "Account not found")
                return
                
            # In a real system, we would update a 'frozen' column in the accounts table
            status = "frozen" if action == "freeze" else "active"
            messagebox.showinfo("Success", f"Account {account_number} has been {status}")
            self.show_employee_dashboard()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to {action} account: {str(e)}")

    def view_customer_details(self):
        """Detailed customer view for employees"""
        self.clear_main_content()
        
        ttk.Label(self.main_content, text="View Customer Details", style='Heading.TLabel').pack(pady=20)
        
        form_frame = tk.Frame(self.main_content, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Customer selection
        ttk.Label(form_frame, text="Customer Username or ID:", background='white').pack(anchor='w', pady=(0, 5))
        self.customer_search_entry = ttk.Entry(form_frame, font=('Arial', 12))
        self.customer_search_entry.pack(fill='x', pady=(0, 20))
        
        # Search button
        ttk.Button(form_frame, text="Search", style='Primary.TButton',
                  command=self.process_customer_search).pack()

    def process_customer_search(self):
        """Process customer search and display details"""
        search_term = self.customer_search_entry.get().strip()
        
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term")
            return
            
        try:
            # Try to search by ID if search term is numeric
            if search_term.isdigit():
                self.cursor.execute('''
                    SELECT * FROM users WHERE id = ?
                ''', (int(search_term),))
            else:
                self.cursor.execute('''
                    SELECT * FROM users WHERE username LIKE ? OR full_name LIKE ?
                ''', (f"%{search_term}%", f"%{search_term}%"))
            
            customer = self.cursor.fetchone()
            
            if not customer:
                messagebox.showerror("Error", "Customer not found")
                return
                
            self.clear_main_content()
            
            # Display customer info
            ttk.Label(self.main_content, text="Customer Details", style='Heading.TLabel').pack(pady=20)
            
            details_frame = tk.Frame(self.main_content, bg=self.colors['light'], relief='raised', bd=1)
            details_frame.pack(pady=20, padx=40, fill='x')
            
            details = [
                ('ID', customer[0]),
                ('Username', customer[1]),
                ('Full Name', customer[3]),
                ('Email', customer[4]),
                ('Phone', customer[5]),
                ('Address', customer[6]),
                ('Joined', datetime.strptime(customer[7], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
            ]
            
            for label, value in details:
                row_frame = tk.Frame(details_frame, bg=self.colors['light'])
                row_frame.pack(fill='x', pady=10, padx=20)
                
                tk.Label(row_frame, text=f"{label}:", bg=self.colors['light'], 
                        font=('Arial', 12, 'bold')).pack(side='left')
                tk.Label(row_frame, text=value, bg=self.colors['light'], 
                        font=('Arial', 12)).pack(side='right')
            
            # Display accounts
            ttk.Label(self.main_content, text="Customer Accounts", style='Heading.TLabel').pack(pady=20)
            
            accounts_frame = tk.Frame(self.main_content)
            accounts_frame.pack(pady=10, padx=20, fill='both', expand=True)
            
            columns = ('Account No', 'Type', 'Balance', 'Created')
            accounts_tree = ttk.Treeview(accounts_frame, columns=columns, show='headings', height=5)
            
            for col in columns:
                accounts_tree.heading(col, text=col)
                accounts_tree.column(col, width=120)
            
            self.cursor.execute('''
                SELECT account_number, account_type, balance, created_at
                FROM accounts WHERE user_id = ?
            ''', (customer[0],))
            accounts = self.cursor.fetchall()
            
            for account in accounts:
                created_date = datetime.strptime(account[3], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                accounts_tree.insert('', 'end', values=(
                    account[0], account[1], f"${account[2]:,.2f}", created_date))
            
            accounts_tree.pack(fill='both', expand=True)
            
            # Display recent transactions
            ttk.Label(self.main_content, text="Recent Transactions", style='Heading.TLabel').pack(pady=20)
            
            transactions_frame = tk.Frame(self.main_content)
            transactions_frame.pack(pady=10, padx=20, fill='both', expand=True)
            
            trans_columns = ('Date', 'Account', 'Type', 'Amount', 'Description')
            trans_tree = ttk.Treeview(transactions_frame, columns=trans_columns, show='headings', height=5)
            
            for col in trans_columns:
                trans_tree.heading(col, text=col)
                trans_tree.column(col, width=120)
            
            self.cursor.execute('''
                SELECT t.timestamp, a.account_number, t.transaction_type, t.amount, t.description
                FROM transactions t
                JOIN accounts a ON t.account_id = a.id
                WHERE a.user_id = ?
                ORDER BY t.timestamp DESC
                LIMIT 10
            ''', (customer[0],))
            transactions = self.cursor.fetchall()
            
            for trans in transactions:
                date = datetime.strptime(trans[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
                amount_str = f"${trans[3]:,.2f}" if trans[3] >= 0 else f"-${abs(trans[3]):,.2f}"
                trans_tree.insert('', 'end', values=(date, trans[1], trans[2], amount_str, trans[4]))
            
            trans_tree.pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search customer: {str(e)}")

    def generate_statement(self):
        """Generate PDF account statement"""
        try:
            # Get user accounts
            self.cursor.execute('''
                SELECT a.account_number, a.account_type, a.balance
                FROM accounts a
                WHERE a.user_id = ?
            ''', (self.current_user,))
            accounts = self.cursor.fetchall()
            
            if not accounts:
                messagebox.showerror("Error", "No accounts found")
                return
                
            # Ask user to select account
            account_numbers = [acc[0] for acc in accounts]
            selected_account = tk.StringVar(value=account_numbers[0])
            
            popup = tk.Toplevel(self.root)
            popup.title("Generate Statement")
            popup.geometry("400x300")
            
            ttk.Label(popup, text="Select Account:").pack(pady=10)
            account_combo = ttk.Combobox(popup, textvariable=selected_account, 
                                       values=account_numbers, state='readonly')
            account_combo.pack(pady=10)
            
            ttk.Label(popup, text="Date Range:").pack(pady=10)
            
            date_frame = tk.Frame(popup)
            date_frame.pack(pady=10)
            
            ttk.Label(date_frame, text="From:").pack(side='left')
            from_date = ttk.Entry(date_frame)
            from_date.pack(side='left', padx=5)
            from_date.insert(0, datetime.now().strftime('%Y-%m-01'))
            
            ttk.Label(date_frame, text="To:").pack(side='left', padx=(10, 0))
            to_date = ttk.Entry(date_frame)
            to_date.pack(side='left')
            to_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
            
            def generate():
                account = selected_account.get()
                start_date = from_date.get()
                end_date = to_date.get()
                
                # Validate dates
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d')
                    end = datetime.strptime(end_date, '%Y-%m-%d')
                    
                    if start > end:
                        messagebox.showerror("Error", "Start date must be before end date")
                        return
                        
                    # Get account info
                    self.cursor.execute('''
                        SELECT a.account_number, a.account_type, a.balance, u.full_name
                        FROM accounts a
                        JOIN users u ON a.user_id = u.id
                        WHERE a.account_number = ?
                    ''', (account,))
                    account_info = self.cursor.fetchone()
                    
                    # Get transactions
                    self.cursor.execute('''
                        SELECT t.timestamp, t.transaction_type, t.amount, t.description
                        FROM transactions t
                        JOIN accounts a ON t.account_id = a.id
                        WHERE a.account_number = ? 
                        AND t.timestamp BETWEEN ? AND ?
                        ORDER BY t.timestamp
                    ''', (account, start_date, end_date))
                    transactions = self.cursor.fetchall()
                    
                    # Ask for save location
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".pdf",
                        filetypes=[("PDF files", "*.pdf")],
                        initialfile=f"BankStatement_{account}_{end_date}.pdf"
                    )
                    
                    if not file_path:
                        return
                        
                    # Create PDF
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Header
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(0, 10, "SecureBank Pro - Account Statement", 0, 1, 'C')
                    pdf.ln(10)
                    
                    # Account info
                    pdf.set_font("Arial", '', 12)
                    pdf.cell(0, 10, f"Account Holder: {account_info[3]}", 0, 1)
                    pdf.cell(0, 10, f"Account Number: {account_info[0]}", 0, 1)
                    pdf.cell(0, 10, f"Account Type: {account_info[1]}", 0, 1)
                    pdf.cell(0, 10, f"Statement Period: {start_date} to {end_date}", 0, 1)
                    pdf.cell(0, 10, f"Current Balance: ${account_info[2]:,.2f}", 0, 1)
                    pdf.ln(10)
                    
                    # Transactions header
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(40, 10, "Date", 1)
                    pdf.cell(40, 10, "Type", 1)
                    pdf.cell(40, 10, "Amount", 1)
                    pdf.cell(70, 10, "Description", 1)
                    pdf.ln()
                    
                    # Transactions
                    pdf.set_font("Arial", '', 10)
                    for t in transactions:
                        date = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                        amount = f"${t[2]:,.2f}" if t[2] >= 0 else f"-${abs(t[2]):,.2f}"
                        
                        pdf.cell(40, 10, date, 1)
                        pdf.cell(40, 10, t[1], 1)
                        pdf.cell(40, 10, amount, 1)
                        pdf.cell(70, 10, t[3], 1)
                        pdf.ln()
                    
                    # Footer
                    pdf.ln(10)
                    pdf.set_font("Arial", 'I', 10)
                    pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 0, 'C')
                    
                    pdf.output(file_path)
                    messagebox.showinfo("Success", f"Statement saved to {file_path}")
                    popup.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format (use YYYY-MM-DD)")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate statement: {str(e)}")
            
            ttk.Button(popup, text="Generate PDF", command=generate).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare statement: {str(e)}")

    def change_password(self):
        """Password change functionality"""
        popup = tk.Toplevel(self.root)
        popup.title("Change Password")
        popup.geometry("400x300")
        
        ttk.Label(popup, text="Current Password:").pack(pady=(20, 5))
        current_pass = ttk.Entry(popup, show='*')
        current_pass.pack(pady=5)
        
        ttk.Label(popup, text="New Password:").pack(pady=(10, 5))
        new_pass = ttk.Entry(popup, show='*')
        new_pass.pack(pady=5)
        
        ttk.Label(popup, text="Confirm New Password:").pack(pady=(10, 5))
        confirm_pass = ttk.Entry(popup, show='*')
        confirm_pass.pack(pady=5)
        
        def update_password():
            current = current_pass.get()
            new = new_pass.get()
            confirm = confirm_pass.get()
            
            if not current or not new or not confirm:
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            if new != confirm:
                messagebox.showerror("Error", "New passwords don't match")
                return
                
            # Verify current password
            table = 'users' if self.current_user_type == 'customer' else 'employees'
            self.cursor.execute(f'SELECT password FROM {table} WHERE id = ?', (self.current_user,))
            stored_hash = self.cursor.fetchone()[0]
            
            if stored_hash != self.hash_password(current):
                messagebox.showerror("Error", "Current password is incorrect")
                return
                
            # Update password
            try:
                self.cursor.execute(f'''
                    UPDATE {table} SET password = ? WHERE id = ?
                ''', (self.hash_password(new), self.current_user))
                self.conn.commit()
                messagebox.showinfo("Success", "Password changed successfully")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Password change failed: {str(e)}")
        
        ttk.Button(popup, text="Change Password", command=update_password).pack(pady=20)

    def search_functionality(self):
        """Enhanced search for employees"""
        popup = tk.Toplevel(self.root)
        popup.title("Search")
        popup.geometry("600x400")
        
        search_frame = tk.Frame(popup)
        search_frame.pack(pady=20, padx=20, fill='x')
        
        ttk.Label(search_frame, text="Search For:").pack(side='left')
        
        search_type = tk.StringVar(value="customers")
        ttk.Combobox(search_frame, textvariable=search_type, 
                    values=["customers", "accounts", "transactions"], 
                    state='readonly').pack(side='left', padx=10)
        
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side='left', fill='x', expand=True)
        
        def perform_search():
            search_term = search_entry.get().strip()
            search_for = search_type.get()
            
            if not search_term:
                messagebox.showerror("Error", "Please enter a search term")
                return
                
            try:
                if search_for == "customers":
                    self.cursor.execute('''
                        SELECT id, username, full_name, email, phone 
                        FROM users 
                        WHERE username LIKE ? OR full_name LIKE ? OR email LIKE ? OR phone LIKE ?
                    ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
                    results = self.cursor.fetchall()
                    
                    # Display results in a new window
                    result_window = tk.Toplevel(popup)
                    result_window.title("Search Results - Customers")
                    
                    tree = ttk.Treeview(result_window, columns=('ID', 'Username', 'Name', 'Email', 'Phone'), show='headings')
                    for col in tree['columns']:
                        tree.heading(col, text=col)
                    
                    for row in results:
                        tree.insert('', 'end', values=row)
                    
                    tree.pack(fill='both', expand=True)
                    
                elif search_for == "accounts":
                    self.cursor.execute('''
                        SELECT a.account_number, u.full_name, a.account_type, a.balance
                        FROM accounts a
                        JOIN users u ON a.user_id = u.id
                        WHERE a.account_number LIKE ? OR u.full_name LIKE ?
                    ''', (f"%{search_term}%", f"%{search_term}%"))
                    results = self.cursor.fetchall()
                    
                    result_window = tk.Toplevel(popup)
                    result_window.title("Search Results - Accounts")
                    
                    tree = ttk.Treeview(result_window, columns=('Account', 'Customer', 'Type', 'Balance'), show='headings')
                    for col in tree['columns']:
                        tree.heading(col, text=col)
                    
                    for row in results:
                        tree.insert('', 'end', values=row)
                    
                    tree.pack(fill='both', expand=True)
                    
                elif search_for == "transactions":
                    self.cursor.execute('''
                        SELECT t.timestamp, a.account_number, u.full_name, t.transaction_type, t.amount
                        FROM transactions t
                        JOIN accounts a ON t.account_id = a.id
                        JOIN users u ON a.user_id = u.id
                        WHERE a.account_number LIKE ? OR u.full_name LIKE ? OR t.transaction_type LIKE ?
                        ORDER BY t.timestamp DESC
                        LIMIT 100
                    ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
                    results = self.cursor.fetchall()
                    
                    result_window = tk.Toplevel(popup)
                    result_window.title("Search Results - Transactions")
                    
                    tree = ttk.Treeview(result_window, columns=('Date', 'Account', 'Customer', 'Type', 'Amount'), show='headings')
                    for col in tree['columns']:
                        tree.heading(col, text=col)
                    
                    for row in results:
                        date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
                        amount = f"${row[4]:,.2f}" if row[4] >= 0 else f"-${abs(row[4]):,.2f}"
                        tree.insert('', 'end', values=(date, row[1], row[2], row[3], amount))
                    
                    tree.pack(fill='both', expand=True)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
        
        ttk.Button(search_frame, text="Search", command=perform_search).pack(side='left', padx=10)

    def run(self):
        """Start the banking system"""
        self.root.mainloop()
        self.conn.close()

if __name__ == "__main__":
    # Create and run the banking system
    banking_system = BankingSystem()
    banking_system.run()