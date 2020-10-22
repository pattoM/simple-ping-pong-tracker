from flask import Flask, render_template, jsonify, request, session 
import os 
from config import * 


#instance 
app = Flask(__name__) 

#config 
if os.getenv('FLASK_DEBUG', None):
    app.config.from_object(DevelopmentConfig) 
else:
    app.config.from_object(ProductionConfig) 

#main route 
@app.route('/')
@app.route('/leaderboard', methods=["GET"]) 
def leaderboard():
    return render_template("index.html")