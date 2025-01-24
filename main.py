from flask import Flask
from flask import redirect
from flask import render_template
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging


app = Flask(__name__)
csrf = CSRFProtect(app)

# control for the signup process, asks for username, password and email
@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        Email = request.form["email"]
        dbHandler.insertUser(username, password, Email)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")

@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["GET"])
@csp_header(
    {
        "default-src": "'self'",
        "script-src": "'self'",
        "img-src": "http: https: data:",
        "object-src": "'self'",
        "style-src": "'self'",
        "media-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "base-uri": "",
        "report-uri": "/csp_report",
        "frame-ancestors": "none",
    }
)
def index():
    url = "http://127.0.0.1:3000"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": "Failed to retrieve data from the API"}
    return render_template("index.html", data=data)


@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)