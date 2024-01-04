from flask import Flask, redirect, url_for, render_template, request,redirect,session
import pandas as pd
from pymongo import MongoClient


app = Flask(__name__)


mongo_uri = uri = mongodb_URI
client = MongoClient(mongo_uri)
db = client.mlstudio 
users_collection = db.users

@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email, 'password': password})

        if user:
            
            session['email'] = user['email']
            return redirect(url_for('train'))
        else:
            
            return render_template('login.html', exist='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email=request.form['email']
    password = request.form['password']
    

    
    existing_user = users_collection.find_one({'username': username})

    if existing_user:
        
        return render_template('login.html', existed='Username already exists')
    else:
        
        users_collection.insert_one({'username': username,'email':email,'password': password})

        
        return redirect(url_for('login'))


@app.route('/index')
def back():
    return render_template('index.html')

@app.route('/trian')
def train():
    if 'email' not in session:
        return redirect(url_for('login'))
    user_email = session['email']
    return render_template('trian.html',user_email=user_email)
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
@app.route('/selection')
def forms():
    return render_template('selection.html')
@app.route('/history')
def history():
    return render_template('history.html')

@app.route("/file_submission", methods=["GET", "POST"])
def chat():
    if request.method == "POST": 
        try:
            file = request.files['file']
            data = pd.read_csv(file)
            dependent_var=data.columns
            user_email = session['email']
            data.to_csv('dataset.csv', index=False)
            return render_template('trian.html', dependent=dependent_var,user_email=user_email)
        except Exception as e:
            return f"An error occurred: {e}"
        

@app.route("/var_selection",methods=["POST"])
def selection():
    
    if request.method=="POST":
        sel_dependent=request.form.getlist(('dependent'))
        sel_independent=request.form.get('independent')
        user_email = session['email']
        from main import selectioned
        selectioned(sel_dependent, sel_independent, user_email)
        algorithms = request.form['algorithm']
        metric = request.form['metrics']
        # from main import my
        # my(sel_dependent,sel_independent)

        return render_template('history.html')


  
   

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True,port=6210)
    
