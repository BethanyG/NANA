# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:21:03 2015

@author: bethanygarcia
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()