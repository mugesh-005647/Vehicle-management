from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Beast@005647",   # 🔴 CHANGE THIS
        database="vehicle_db"
    )


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        con = get_connection()
        cursor = con.cursor()

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()
        con.close()

        if user:
            session["admin"] = username
            return redirect("/dashboard")
        else:
            flash("Invalid Username or Password", "danger")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/")

    con = get_connection()
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM vehicle")
    total_vehicles = cursor.fetchone()[0]

    con.close()

    return render_template("dashboard.html",
                           total_vehicles=total_vehicles,
                           admin=session["admin"])


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("admin", None)
    flash("Logged out successfully", "success")

    return redirect("/")


# ---------------- ADD OWNER ----------------
@app.route("/add_owner", methods=["GET", "POST"])
def add_owner():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        owner_name = request.form["owner_name"]
        phone = request.form["phone"]
        address = request.form["address"]

        con = get_connection()
        cursor = con.cursor()

        cursor.execute("""
            INSERT INTO owner (owner_name, phone, address)
            VALUES (%s, %s, %s)
        """, (owner_name, phone, address))

        con.commit()
        con.close()

        flash("Owner Added Successfully", "success")
        return redirect("/add_owner")

    return render_template("add_owner.html")

# ---------------- VIEW OWNERS ----------------
@app.route("/view_owner")
def view_owner():

    if "admin" not in session:
        return redirect("/")

    con = get_connection()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM owner")
    owners = cursor.fetchall()

    con.close()

    return render_template("view_owner.html", owners=owners)


# ---------------- ADD VEHICLE ----------------
@app.route("/add_vehicle", methods=["GET", "POST"])
def add_vehicle():

    if "admin" not in session:
        return redirect("/")

    con = get_connection()
    cursor = con.cursor()

    # Load owners for dropdown
    cursor.execute("SELECT owner_id, owner_name FROM owner")
    owners = cursor.fetchall()

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"].upper()
        owner_id = request.form["owner_id"]
        vehicle_type = request.form["vehicle_type"]
        model = request.form["model"]
        reg_date = request.form["reg_date"]

        try:
            cursor.execute("""
                INSERT INTO vehicle
                (vehicle_no, owner_id, vehicle_type, model, reg_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (vehicle_no, owner_id, vehicle_type, model, reg_date))

            con.commit()
            flash("Vehicle Added Successfully", "success")
            return redirect("/add_vehicle")

        except Error as e:
            if "Duplicate" in str(e):
                flash("Vehicle Number Already Exists", "danger")
            else:
                flash("Error Adding Vehicle", "danger")

    con.close()

    return render_template("add_vehicle.html", owners=owners)


# ---------------- VIEW & SEARCH VEHICLE ----------------
@app.route("/view_vehicle", methods=["GET"])
def view_vehicle():

    if "admin" not in session:
        return redirect("/")

    search_query = request.args.get("search", "")

    con = get_connection()
    cursor = con.cursor()

    if search_query:
        cursor.execute("""
            SELECT vehicle.vehicle_id,
                   vehicle.vehicle_no,
                   owner.owner_name,
                   vehicle.vehicle_type,
                   vehicle.model,
                   vehicle.reg_date
            FROM vehicle
            JOIN owner ON vehicle.owner_id = owner.owner_id
            WHERE vehicle.vehicle_no LIKE %s
        """, ("%" + search_query + "%",))
    else:
        cursor.execute("""
            SELECT vehicle.vehicle_id,
                   vehicle.vehicle_no,
                   owner.owner_name,
                   vehicle.vehicle_type,
                   vehicle.model,
                   vehicle.reg_date
            FROM vehicle
            JOIN owner ON vehicle.owner_id = owner.owner_id
        """)

    vehicles = cursor.fetchall()
    con.close()

    return render_template("view_vehicle.html",
                           vehicles=vehicles,
                           search_query=search_query)


# ---------------- DELETE VEHICLE ----------------
@app.route("/delete_vehicle/<int:vehicle_id>")
def delete_vehicle(vehicle_id):

    if "admin" not in session:
        return redirect("/")

    con = get_connection()
    cursor = con.cursor()

    cursor.execute("DELETE FROM vehicle WHERE vehicle_id=%s", (vehicle_id,))
    con.commit()
    con.close()

    flash("Vehicle Deleted Successfully", "success")
    return redirect("/view_vehicle")
    
# ---------------- EDIT VEHICLE ----------------
@app.route("/edit_vehicle/<int:vehicle_id>", methods=["GET", "POST"])
def edit_vehicle(vehicle_id):

    if "admin" not in session:
        return redirect("/")

    con = get_connection()
    cursor = con.cursor()

    # Load owners for dropdown
    cursor.execute("SELECT owner_id, owner_name FROM owner")
    owners = cursor.fetchall()

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"].upper()
        owner_id = request.form["owner_id"]
        vehicle_type = request.form["vehicle_type"]
        model = request.form["model"]
        reg_date = request.form["reg_date"]

        try:
            cursor.execute("""
                UPDATE vehicle
                SET vehicle_no=%s,
                    owner_id=%s,
                    vehicle_type=%s,
                    model=%s,
                    reg_date=%s
                WHERE vehicle_id=%s
            """, (vehicle_no, owner_id, vehicle_type,
                  model, reg_date, vehicle_id))

            con.commit()
            flash("Vehicle Updated Successfully ✅", "success")
            return redirect("/view_vehicle")

        except Error as e:
            if "Duplicate" in str(e):
                flash("Vehicle Number Already Exists ❌", "danger")
            else:
                flash("Error Updating Vehicle", "danger")

    # Load current vehicle details
    cursor.execute("SELECT * FROM vehicle WHERE vehicle_id=%s", (vehicle_id,))
    vehicle = cursor.fetchone()

    con.close()

    return render_template("edit_vehicle.html",
                           vehicle=vehicle,
                           owners=owners)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)