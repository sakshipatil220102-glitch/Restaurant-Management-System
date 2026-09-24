from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sakshi@22",
    database="restaurant_db"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin")
def admin():

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            customers.name,
            customers.phone,
            customers.address,
            food.food_name,
            orders.quantity,
            orders.order_date
        FROM orders
        JOIN customers
        ON orders.customer_id = customers.customer_id
        JOIN food
        ON orders.food_id = food.food_id
    """)

    orders = cursor.fetchall()

    return render_template("admin.html", orders=orders)


@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        food = request.form["food"]
        quantity = request.form["quantity"]

        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)",
            (name, phone, address)
        )

        customer_id = cursor.lastrowid

        cursor.execute(
            "SELECT food_id FROM food WHERE food_name = %s",
            (food,)
        )

        food_result = cursor.fetchone()
        food_id = food_result[0]

        cursor.execute(
            "INSERT INTO orders (customer_id, food_id, quantity) VALUES (%s, %s, %s)",
            (customer_id, food_id, quantity)
        )

        db.commit()

        print("Order saved successfully")

        return render_template(
            "order.html",
            message="Order placed successfully! 🍽️"
        )

    return render_template("order.html")


if __name__ == "__main__":
    app.run(debug=True)