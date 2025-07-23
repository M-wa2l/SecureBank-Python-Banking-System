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


<img width="1919" height="1018" alt="Screenshot 2025-07-23 123720" src="https://github.com/user-attachments/assets/3deaaff9-cefb-4cde-968f-ff562755bc07" />


<img width="1919" height="1020" alt="Screenshot 2025-07-23 123802" src="https://github.com/user-attachments/assets/55f0800d-1dcf-456f-b6c1-076a3f564f4a" />

<img width="1918" height="1017" alt="Screenshot 2025-07-23 124109" src="https://github.com/user-attachments/assets/6f1ded94-386a-4b85-abc5-0cfe69974804" />



---

## 📝 License

This project is open source under the **MIT License**. You are free to use, modify, and distribute it for any purpose.

---


## 🙏 Acknowledgements

Thanks to the Python and Tkinter communities for their incredible support and documentation.

Special thanks to open-source developers who inspired features such as PDF generation, modular class design, and themed widgets in Tkinter.
