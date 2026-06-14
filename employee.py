from flask import Flask, jsonify, request
import mysql.connector
from datetime import date

app = Flask(__name__)

# ─────────────────────────────────────────
# 1. DATABASE CONNECTION
# ─────────────────────────────────────────
def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",  # 🔁 change to your MySQL password
        database="employee_db"
    )
    return conn


# ─────────────────────────────────────────
# 2. HOME ROUTE
# ─────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({
        "message": "👋 Welcome to Employee Management API",
        "version": "1.0",
        "author": "Thanisha M Shetty",
        "endpoints": {
            "GET    /employees":           "Get all employees",
            "GET    /employees/<id>":      "Get employee by ID",
            "GET    /employees/dept/<name>": "Get employees by department",
            "POST   /employees":           "Add new employee",
            "PUT    /employees/<id>":      "Update employee",
            "DELETE /employees/<id>":      "Delete employee"
        }
    })


# ─────────────────────────────────────────
# 3. GET ALL EMPLOYEES
# ─────────────────────────────────────────
@app.route("/employees", methods=["GET"])
def get_all_employees():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()

    # Convert date to string for JSON
    for emp in employees:
        if isinstance(emp.get("joining_date"), date):
            emp["joining_date"] = str(emp["joining_date"])

    return jsonify({
        "success": True,
        "count": len(employees),
        "employees": employees
    }), 200


# ─────────────────────────────────────────
# 4. GET EMPLOYEE BY ID
# ─────────────────────────────────────────
@app.route("/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
    emp = cursor.fetchone()
    conn.close()

    if not emp:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    if isinstance(emp.get("joining_date"), date):
        emp["joining_date"] = str(emp["joining_date"])

    return jsonify({"success": True, "employee": emp}), 200


# ─────────────────────────────────────────
# 5. GET EMPLOYEES BY DEPARTMENT
# ─────────────────────────────────────────
@app.route("/employees/dept/<string:dept_name>", methods=["GET"])
def get_by_department(dept_name):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE department = %s", (dept_name,))
    employees = cursor.fetchall()
    conn.close()

    for emp in employees:
        if isinstance(emp.get("joining_date"), date):
            emp["joining_date"] = str(emp["joining_date"])

    return jsonify({
        "success": True,
        "department": dept_name,
        "count": len(employees),
        "employees": employees
    }), 200


# ─────────────────────────────────────────
# 6. ADD NEW EMPLOYEE (POST)
# ─────────────────────────────────────────
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()

    # Validate required fields
    required = ["name", "department", "salary", "email", "joining_date"]
    for field in required:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing field: {field}"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees (name, department, salary, email, joining_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (data["name"], data["department"], data["salary"],
          data["email"], data["joining_date"]))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "success": True,
        "message": "Employee added successfully",
        "id": new_id
    }), 201


# ─────────────────────────────────────────
# 7. UPDATE EMPLOYEE (PUT)
# ─────────────────────────────────────────
@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    # Build dynamic update query
    fields = []
    values = []
    for key in ["name", "department", "salary", "email", "joining_date"]:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])

    if not fields:
        return jsonify({"success": False, "message": "No fields to update"}), 400

    values.append(emp_id)
    query = f"UPDATE employees SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    return jsonify({
        "success": True,
        "message": f"Employee {emp_id} updated successfully"
    }), 200


# ─────────────────────────────────────────
# 8. DELETE EMPLOYEE
# ─────────────────────────────────────────
@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    return jsonify({
        "success": True,
        "message": f"Employee {emp_id} deleted successfully"
    }), 200


# ─────────────────────────────────────────
# 9. RUN APP
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Employee Management API Running!")
    print("📍 Open browser: http://127.0.0.1:5000")
    print("📍 All employees: http://127.0.0.1:5000/employees")
    app.run(debug=True)
