from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, time, url
import json

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///workout.db")

# Create table for history, plan, exercise
db.execute("CREATE TABLE IF NOT EXISTS 'history' (user_id TEXT NOT NULL, exercise TEXT NOT NULL, duration TEXT NOT NULL, time DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")
db.execute("CREATE TABLE IF NOT EXISTS 'plan' (user_id TEXT NOT NULL, ord TEXT, plan TEXT NOT NULL, duration TEXT, rest TEXT, exercise TEXT NOT NULL, link TEXT, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(exercise) REFERENCES exercise(name))")
db.execute("CREATE TABLE IF NOT EXISTS 'exercise' (user_id TEXT NOT NULL, name TEXT NOT NULL, part TEXT NOT NULL, link TEXT, PRIMARY KEY(name), FOREIGN KEY(user_id) REFERENCES users(id))")

@app.route("/")
@login_required
def index():
    """Home"""
    return render_template("index.html")

@app.route("/timer")
@login_required
def timer():
    """Timer"""
    return render_template("timer.html")

@app.route("/stop")
@login_required
def stop():
    """Stopwatch"""
    return render_template("stopwatch.html")

@app.route("/history")
@login_required
def history():
    """Show history"""
    history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY TIME DESC", session["user_id"])

    return render_template("history.html", history=history)

@app.route("/plan", methods=["GET", "POST"])
@login_required
def plan():
    """Show plan"""
    if request.method == "POST":
        p = request.form.get("plan")
        if (p == ''):
            return redirect("/plan")
        elif (p == "create"):
            return redirect("/create")
        else:
            plan = db.execute("SELECT * FROM plan WHERE user_id = ? AND plan = ? OR user_id = 0 AND plan = ? ORDER BY ord", session["user_id"], p, p)
            return render_template("start.html", plan=plan, name=plan[0]["plan"], dur=time(int(plan[0]["duration"]) * int(plan[-1]["ord"]) + int(plan[0]["rest"]) * int(plan[-2]["ord"])))

    else:
        plan = db.execute("SELECT DISTINCT plan FROM plan WHERE user_id = ? OR user_id = 0", session["user_id"])
        return render_template("plan.html", plan=plan)


@app.route("/insert")
@login_required
def insert():
    """Insert history into database"""
    db.execute("INSERT INTO history (user_id, exercise, duration) VALUES (?, ?, ?)", session["user_id"], url(request.args.get("e")), url(request.args.get("q")))
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Insert history into database"""
    if request.method == "POST":
        name = request.form.get("name")
        link = request.form.get("link")
        part = request.form.get("part")
        # Invalid plan
        if len(db.execute("SELECT * FROM exercise WHERE user_id = ? AND name = ? OR user_id = 0 AND name = ?", session["user_id"], name, name)) != 0:
            return render_template("addExercise.html", invalid="exercise name existed")
        else:
            db.execute("INSERT INTO exercise (user_id, name, link, part) VALUES (?, ?, ?, ?)", session["user_id"], name, link, part)
            return redirect("/plan")
    else:
        return render_template("addExercise.html")


@app.route("/s")
@login_required
def s():
    """Search for exercise"""
    q = url(request.args.get("q"))
    e = url(request.args.get("e"))
    if (e == ''):
        ex = db.execute("SELECT * FROM exercise WHERE user_id = ? AND name LIKE ? OR user_id = 0 AND name LIKE ? ORDER BY name", session["user_id"], "%" + q + "%", "%" + q + "%")
    elif (q ==''):
        ex = db.execute("SELECT * FROM exercise WHERE user_id = ? AND part LIKE ? OR user_id = 0 AND part LIKE ? ORDER BY name", session["user_id"], e + "%", e + "%")
    elif (e == '' and q == ''):
        ex = db.execute("SELECT * FROM exercise WHERE user_id = ? OR user_id = 0 ORDER BY name", session["user_id"])
    else:
        ex = db.execute("SELECT * FROM exercise WHERE user_id = ? AND name LIKE ? AND part LIKE ? OR user_id = 0 AND name LIKE ? AND part LIKE ? ORDER BY name", session["user_id"], "%" + q + "%", e + "%", "%" + q + "%", e + "%")
    return jsonify(ex)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create workout plan"""
    if request.method == "POST":
        plan = request.form["plan"]
        dur = request.form["dur"]
        rest = request.form["rest"]
        ex = json.loads(request.form["document"])
        # Invalid plan
        if len(db.execute("SELECT * FROM plan WHERE user_id = ? AND plan = ? OR user_id = 0 AND plan = ?", session["user_id"], plan, plan)) != 0:
            return render_template("createPlan.html", invalid="plan name existed")
        else:
            link = []
            for i in range(len(ex)):
                link.append(db.execute("SELECT link FROM exercise WHERE name = ? AND user_id = ? OR name = ? AND user_id = 0 ", ex[i], session["user_id"], ex[i])[0]["link"])
                db.execute("INSERT INTO plan (user_id, exercise, duration, rest, plan, ord, link) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], ex[i], dur, rest, plan, i + 1, link[i])
            return redirect("/plan")

    else:
        ex = db.execute("SELECT * FROM exercise WHERE user_id = ? OR user_id = 0 ORDER BY name", session["user_id"])
        return render_template("createPlan.html", ex=ex)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", invalid="invalid username or password")

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear session
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        name = request.form.get("username")

        # Invalid username
        if len(db.execute("SELECT * FROM users WHERE username = ?", name)) != 0:
            return render_template("register.html", invalid="Username existed")

        else:
            # Insert into database
            db.execute("INSERT INTO users (username, hash) VALUES (? ,?)",
                name, generate_password_hash(request.form.get("password")))

            # Remember which user has logged in
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", name)[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
