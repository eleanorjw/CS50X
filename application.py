import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create table for stocks and transaction
db.execute("CREATE TABLE IF NOT EXISTS 'stocks' (user_id TEXT NOT NULL, symbol TEXT NOT NULL, shares TEXT NOT NULL, price TEXT NOT NULL, sum NUMERIC NOT NULL GENERATED ALWAYS AS (price*shares) STORED, FOREIGN KEY(user_id) REFERENCES users(id))")
db.execute("CREATE TABLE IF NOT EXISTS 'transactions' (user_id TEXT NOT NULL, symbol TEXT NOT NULL, shares TEXT NOT NULL, price TEXT NOT NULL, sum TEXT NOT NULL, time DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    sum = 0
    # Geting stocks of user
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])
    for stock in stocks:
        if int(stock["shares"]) == 0:
            db.execute("DELETE FROM stocks WHERE symbol = ?", stock["symbol"])
            continue
        price = lookup(stock["symbol"])["price"]
        db.execute("UPDATE stocks SET price = ? WHERE symbol = ?", price, stock["symbol"])
        sum = sum + db.execute("SELECT sum FROM stocks WHERE symbol = ?", stock["symbol"])[0]["sum"]

    # Total up sum and cash
    cash = round(db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"], 2)
    sum = round(sum + cash, 2)

    # Return template
    return render_template("index.html", sum=sum, stocks=stocks, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Check valid input
        if not symbol or lookup(symbol) == None:
            return apology("invalid symbol", 403)
        elif not shares or int(ord(shares[0])) > 57 or int(ord(shares[0])) < 48 or int(shares) < 0:
            return apology("invalid shares", 403)

        # Price of shares
        price = lookup(symbol)["price"]
        sum = round(float(price) * int(shares), 2)

        # Get user data from database
        user = db.execute("SELECT * FROM users where id = ?", session["user_id"])

        # Check if enough cash
        if sum > user[0]["cash"]:
            return apology("not enough cash", 403)
        else:
            # Update cash
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", sum, session["user_id"])

            # Insert stock and transaction table
            if len(db.execute("SELECT * FROM stocks WHERE symbol = ? AND user_id = ?", symbol, session["user_id"])) == 0:
                db.execute("INSERT INTO stocks (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, shares, price)
            # Stock with existing shares
            else:
                db.execute("UPDATE stocks SET shares = shares + ? WHERE symbol = ? AND user_id = ?", shares, symbol, session["user_id"])

            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, sum) VALUES (?, ?, ?, ?, ?)", session["user_id"], symbol, shares, price, sum)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY TIME DESC", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # User search nothing
        if not request.form.get("symbol"):
            return redirect("/quote")

        # Lookup for symbol, diaplay result if exist, else error
        result = lookup(request.form.get("symbol"))
        if result == None:
            return apology("stock not exist", 403)
        else:
            return render_template("quoted.html", result=result)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear session
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        name = request.form.get("username")

        # Ensure username was submitted
        if not name:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirmed password", 400)

        # Ensure passwords are same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("different password typed", 403)

        # Invalid username
        elif len(db.execute("SELECT * FROM users WHERE username = ?", name)) != 0:
            return apology("username existed", 403)

        else:
            # Insert into database
            db.execute("INSERT INTO users (username, hash) VALUES (? ,?)", name, generate_password_hash(request.form.get("password")))

            # Remember which user has logged in
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", name)[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("no symbol selected", 403)

        shares = request.form.get("shares")
        oldshares = int(db.execute("SELECT shares FROM stocks WHERE symbol = ? AND user_id = ?", symbol, session["user_id"])[0]["shares"])

        if not shares or int(ord(shares[0])) > 57 or int(ord(shares[0])) < 48 or int(shares) > oldshares or int(shares) < 0:
            return apology("invalid shares", 403)
        else:
            price = lookup(symbol)["price"]
            sum = round(int(shares) * float(price), 2)

            # Update stock and transcastion
            db.execute("UPDATE stocks SET shares = ? WHERE symbol = ? AND user_id = ?", oldshares - int(shares), symbol, session["user_id"])
            db.execute("INSERT INTO transactions (symbol, shares, price, sum, user_id) VALUES (?, ?, ?, ?, ?)", symbol, "-" + shares, price, sum, session["user_id"])

            # Update cash
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sum, session["user_id"])

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        stocks = db.execute("SELECT symbol FROM stocks WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """ Change password """
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirmed password", 403)

        # Ensure passwords are same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("different password typed", 403)

        else:
            # Insert into database
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
