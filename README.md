# Employee Management REST API

A REST API built with Python and Flask to manage employee records using MySQL database. Supports full CRUD operations.

## Tech Stack
Python | Flask | MySQL | mysql-connector-python

## Features
- Get all employees
- Get employee by ID
- Get employees by department
- Add new employee
- Update employee details
- Delete employee
- JSON responses with error handling

## Installation

Step 1 - Clone the repo
git clone https://github.com/yourusername/employee-management-api.git

Step 2 - Install dependencies
pip install flask mysql-connector-python

Step 3 - Set up MySQL
Create database employee_db and employees table (see app.py for schema)

Step 4 - Update MySQL password in app.py
password="your_mysql_password"

Step 5 - Run
python app.py

Step 6 - Open browser
http://127.0.0.1:5000

## API Endpoints
GET    /employees              - Get all employees
GET    /employees/<id>         - Get employee by ID
GET    /employees/dept/<name>  - Get by department
POST   /employees              - Add new employee
PUT    /employees/<id>         - Update employee
DELETE /employees/<id>         - Delete employee

## Author
Thanisha M Shetty
Computer Science Engineering Graduate
Bengaluru, India
thanishamshetty@gmail.com
