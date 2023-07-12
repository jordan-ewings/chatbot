# libraries ---------------------------

from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import openai
from mod import ChatSession

# app init ---------------------------

app = Flask(__name__)

# openai setup ---------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
cs = ChatSession()

# main ---------------------------

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        cs.add("user", request.form["query"])
        cs.submit()
        return redirect(url_for('index'))
    return render_template("index.html", messages=cs.messages, n=len(cs.messages))

if __name__=='__main__':
    app.run(debug=True)

