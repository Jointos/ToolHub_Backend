from flask import Flask, render_template, g,request,redirect,url_for,jsonify,current_app
import sqlite3, os, re, io, sys, subprocess, json

app = Flask(__name__)

with app.app_context():
    DATABASE = os.path.join('../db','toolhub_database.sqlite3')
    #Formoknál kell valamiért secret key
    app.config['SECRET_KEY'] = 'any secret string'
    print(current_app.name)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# temporary solution until we switch to docker
@app.route('/run_script',methods=['POST'])
def run_script():
    # input_form = InputForm()
    #
    # if input_form.validate_on_submit():
        # source_file_path=os.path.join('../db/tools',input.data.filename_without_extension+'.py') # input.data.filename_without_extension
        # output = subprocess.check_output("python " + source_file_path + " " + input_form.input.data.input, shell=True) # input_form.input.data.input
        # return output
    return "Error"

def get_tools():
    cursor = get_db().cursor()
    # limit 10 could vary
    rows =  cursor.execute('select name,source_file_name from scripts limit 10').fetchall()
    results = []
    for row in rows:
        with open(os.path.join('../db/tools',row[1]), 'r') as scriptfile:
            results.append({'name':row[0],'source_file_name':row[1].split('.')[0],'source_code':scriptfile.read()})
    return results

@app.route('/')
@app.route('/index')
def index():
    tools=get_tools()
    return str(tools)