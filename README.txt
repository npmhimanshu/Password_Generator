🔐 PASSWORD GENERATOR
(Python + Flask + Dark Mode UI)
1️⃣ PROJECT OVERVIEW

Project Title: Password Generator
Domain: Python / Web Application
Technology Stack:

Frontend: HTML, CSS (Dark Mode)

Backend: Python (Flask)

Database: SQLite

2️⃣ PROBLEM STATEMENT

Weak and predictable passwords are a major cause of security breaches.
There is a need for a system that can generate strong, random, and customizable passwords through an easy-to-use interface.

3️⃣ OBJECTIVES

Generate strong passwords automatically

Allow user-defined password length

Provide character selection options

Store generated password history

Offer a modern dark-mode UI

4️⃣ SYSTEM REQUIREMENTS
Hardware Requirements

Minimum 4 GB RAM

Any modern processor

Software Requirements

Python 3.x

Flask Framework

Web Browser

SQLite Database

5️⃣ SYSTEM ARCHITECTURE

User → Frontend (HTML/CSS) → Flask Backend → Password Logic → SQLite Database

6️⃣ PROJECT STRUCTURE (FOLDER FORMAT)
Password_Generator/
│
├── app.py
├── passwords.db
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── README.txt

7️⃣ MODULE DESCRIPTION
7.1 Frontend Module

Dark mode UI

Input fields for password length

Checkbox options for character selection

Displays generated password

Shows password history

7.2 Backend Module (Flask)

Handles user requests

Generates password using Python logic

Stores password in database

Fetches password history

7.3 Database Module (SQLite)

Stores generated passwords

Maintains last 5 password records

8️⃣ FUNCTIONAL FEATURES

Random password generation

Uppercase / Lowercase selection

Numbers and special characters

Password history storage

Responsive dark UI

9️⃣ SECURITY FEATURES

Randomized character selection

User-controlled complexity

No personal user data stored

🔟 ALGORITHM (STEP-BY-STEP)

Take password length from user

Read selected character options

Combine selected character sets

Generate random password

Store password in database

Display password and history

1️⃣1️⃣ OUTPUT SCREEN

Dark theme web interface

Generated password display

Password history list

(Screenshots can be attached here)

1️⃣2️⃣ ADVANTAGES

Easy to use

Secure password generation

Full-stack application

Lightweight and fast

1️⃣3️⃣ LIMITATIONS

No user authentication

Passwords stored as plain text

Local database only

1️⃣4️⃣ FUTURE ENHANCEMENTS

Password encryption

User login system

Password strength meter

Clipboard auto-clear

Cloud database support

1️⃣5️⃣ CONCLUSION

The Password Generator project successfully demonstrates the use of Python and Flask in building a secure, real-world web application with a modern interface and database integration.

1️⃣6️⃣ REFERENCES

Python Documentation

Flask Official Documentation

SQLite Documentation
