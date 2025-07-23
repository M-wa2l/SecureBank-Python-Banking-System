# 💼 SecureBank - Python Banking System

**SecureBank** is a comprehensive desktop-based banking management system written in Python using Tkinter. It provides a secure and modern interface for both customers and bank employees to perform and manage typical banking operations efficiently.

SecureBank simulates the core functionalities of a banking institution with an intuitive and interactive GUI. From account creation to real-time transactions and administrative tools for bank employees, this system is built for demonstration, education, and small-scale deployment scenarios.

This application focuses on usability, performance, and secure operations by implementing industry-standard practices such as password hashing and input validation. It uses a local SQLite database for storage, making it simple to deploy without external dependencies.

The project is modular and extensible, designed to help learners and developers understand how a banking system can be architected using Python's built-in libraries. It can also serve as a foundational base for further enhancements like adding interest calculations, integrating OTP-based login, or connecting to an actual web backend.

---

## 🛠️ Features

### 👤 Customer Interface

* User registration and login
* Account balance overview
* Money deposit and withdrawal
* Transfer between accounts
* Full transaction history
* Account details update
* Create or close accounts
* Apply for loans
* Generate downloadable account statements (PDF)

### 🧑‍💼 Employee Interface

* Login as admin/employee
* View all customers and accounts
* Monitor and manage transactions
* Review, approve, or reject loan applications
* Create new employee accounts
* Search customer profiles and view details
* Freeze or unfreeze accounts
* View real-time bank statistics

---

## 📚 Technologies Used

* **Python 3**
* **Tkinter** for GUI
* **SQLite** for local database management
* **hashlib** for password security (SHA-256 hashing)
* **ttk** for styled widgets
* *(Optional)* `fpdf` for generating account statements

---

## 📁 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/SecureBank.git
cd SecureBank
```

### 2. Install optional PDF library

```bash
pip install fpdf
```

### 3. Run the application

```bash
python test.py
```

This will open the SecureBank GUI. You can log in as an admin or register a new customer account. All operations are handled locally.

---

## 🔑 Default Admin Credentials

| Username | Password   |
| -------- | ---------- |
| `admin`  | `admin123` |

---

## 📚 Project Structure

```
SecureBank/
├── test.py              # Main source file
├── banking_system.db    # SQLite DB file (auto-generated)
├── README.md            # Project documentation
```

---

## 🖼️ Screenshots

*Coming soon...*

You can capture and include screenshots of the login screen, dashboard, transaction history view, or loan application interface for a more visual README.

---

## 📝 License

This project is open source under the **MIT License**. You are free to use, modify, and distribute it for any purpose.

---

## ✨ Contributions

Feel free to fork the repo, make improvements, or suggest new features via pull requests. All contributions are welcome!

If you're a beginner, this project can be a great way to learn GUI development, database handling, and user authentication in Python.

---

## 🙏 Acknowledgements

Thanks to the Python and Tkinter communities for their incredible support and documentation.

Special thanks to open-source developers who inspired features such as PDF generation, modular class design, and themed widgets in Tkinter.
