# libraries ---------------------------

from flask import redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import openai
from .models import ChatSession
import json

# app init ---------------------------

from source import app

# openai setup ---------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
cs = ChatSession()

# main ---------------------------

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chatcompletion", methods=["GET", "POST"])
def chatcompletion():
    if request.method == "POST":
        cs.add("user", request.form["query"])
        cs.submit()
        return redirect(url_for('chatcompletion'))
    return render_template("chatcompletion.html", messages=cs.messages, n=len(cs.messages))

@app.route("/api", methods=["GET"])
def api():
    return render_template("api.html", messages=cs.messages, n=len(cs.messages))
