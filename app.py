from flask import Flask, render_template, request
import sqlite3

from database import create_database


app = Flask(__name__)

create_database()


# Fixed prices controlled by the system
PASS_PRICES = {
    "Daily": 50,
    "Weekly": 250,
    "Monthly": 800
}


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    pass_id = ""

    if request.method == "POST":

        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        source = request.form["source"].strip()
        destination = request.form["destination"].strip()
        pass_type = request.form["pass_type"]

        # Validate input
        if not name or not phone or not source or not destination:
            message = "Please fill all fields."

            return render_template(
                "index.html",
                message=message
            )

        # Check valid pass type
        if pass_type not in PASS_PRICES:

            message = "Invalid pass type."

            return render_template(
                "index.html",
                message=message
            )

        # Automatically determine price
        price = PASS_PRICES[pass_type]

        connection = sqlite3.connect("bus_pass.db")

        cursor = connection.cursor()

        # Store booking
        cursor.execute("""
            INSERT INTO bus_passes
            (
                passenger_name,
                phone,
                source,
                destination,
                pass_type,
                price
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            source,
            destination,
            pass_type,
            price
        ))

        connection.commit()

        # Generate unique ID
        pass_id = cursor.lastrowid

        connection.close()

        message = "Bus pass booked successfully!"

    return render_template(
        "index.html",
        message=message,
        pass_id=pass_id
    )


if __name__ == "__main__":
    app.run(debug=True)