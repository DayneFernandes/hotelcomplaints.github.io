
from flask import Flask, render_template, request, redirect
import mysql.connector
from flask import render_template, render_template_string
from datetime import datetime,date
import gunicorn

app = Flask(__name__)


@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Summerville Beach Resort Guest Portal</title>
        <style>
            body {
                background-color: #f7f7f7;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }

            .container {
                width: 80%;
                margin: 0 auto;
                padding: 50px 0;
                text-align: center;
            }

            h1 {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                font-size: 36px;
                color: #333;
                margin-bottom: 20px;
            }

            p {
                font-size: 18px;
                margin-bottom: 10px;
            }

            a {
                display: inline-block;
                padding: 12px 20px;
                background-color: #007bff;
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }

            a:hover {
                background-color: #0056b3;
            }

            .logo {
                margin-bottom: 30px;
            }

            .message {
                font-size: 20px;
                color: #666;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img class="logo" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUCRhC1D93TwUbeNPTnS-HLSmY0TBRtaGIE3ANZXBD-Q&s" alt="Summerville Beach Resort Logo">
            <h1>Welcome to Summerville Beach Resort Guest Portal</h1>
            <p class="message">We value your stay and are committed to providing exceptional service.</p>
            <p>Kindly choose an option below:</p>
            <p><a href="/submit-complaint">Lodge a Complaint</a></p>
            <p><a href="/complaints">Staff Login</a></p>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    import os
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    app.run(host=host, port=port)
