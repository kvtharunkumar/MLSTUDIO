import base64
from io import BytesIO
import io
import zipfile
from bson import ObjectId
from flask import Flask, abort, redirect, send_file, url_for, render_template, request,redirect,session
import fsspec
import pandas as pd
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from config import mongo

app = Flask(__name__)

appConf={
   
    }

oauth= OAuth(app)


mongo_uri = uri = mongo()
client = MongoClient(mongo_uri)
db = client.mlstudio 
users_collection = db.users

@app.route('/')
def welcome():
    return render_template('index.html')

oauth.register(
    name='mlstudio',
    
)




@app.route('/google-login')
def google():
    return oauth.mlstudio.authorize_redirect(redirect_uri=url_for('googlecallback', _external=True))


@app.route('/glogin')
def googlecallback():
    token = oauth.mlstudio.authorize_access_token()
    user_info = oauth.mlstudio.get('userinfo')
    user_email = user_info.json().get('email') if user_info.status_code == 200 else None
    session['email']=user_info.json().get('email')
    existing_user = users_collection.find_one({'email': user_email})

    if existing_user:
        
        return render_template('trian.html', user_email=user_email)
    else:
        
        users_collection.insert_one({'username': user_email,'email':user_email,'password': None})

        
        return render_template('trian.html', user_email=user_email)
    
        



#Login route
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
            
            return render_template('login.html', exist='Email/Password is Invlaid ')
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


#home route

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
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/forgot-password',methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})
        if user:
            new_password = request.form['new_password']
            users_collection.update_one({'email': email}, {'$set': {'password': new_password}})
            return render_template('forgot_password.html',exist="password updated successfully")
        else:
            return render_template('forgot_password.html',exist='User with this email does not exist.')
            

#history page Route

@app.route('/historys')
def history():
    if 'email'  not in session:
        return redirect(url_for('login'))
    user_email = session['email']
    user_data = users_collection.find_one({'email': user_email})
    models = user_data.get("models", []) if user_data else []

    model_filename = request.args.get("download")  # Check for download request
    # if model_filename:
    #     for model in models:
            
    #             base64_data = model["model_file"]
                
    #             decoded_data = base64.decodebytes(base64_data)  # Convert string to bytes before decoding
                
    #             return send_file(
    #                 io.BytesIO(decoded_data),
    #                download_name=model_filename,
    #                 as_attachment=True
    #             )
    if model_filename:
        for model in models:
            base64_data = model.get("model_file")
            if base64_data:
                try:
                    decoded_data = base64.b64decode(base64_data)
                    return send_file(
                        io.BytesIO(decoded_data),
                        download_name=model_filename,
                        as_attachment=True
                    )
                except base64.binascii.Error as e:
                    # Log the error or handle it appropriately
                    print("Base64 decoding error:", e)
      

        

    return render_template('history.html', models=models,user_email=user_email)


#fecth the file from the user

@app.route("/file_submission", methods=["GET", "POST"])
def chat():
    if request.method == "POST": 
        try:
            file = request.files['file']
            data = pd.read_csv(file)
            dependent_var=data.columns
            user_email = session['email']
            data.to_csv('dataset.csv', index=False)
            return render_template('trian.html',sindep="Select Independent Varibles", sdep="Select Dependent Variable", dependent=dependent_var,user_email=user_email)
        except Exception as e:
            return f"An error occurred: {e}"
        


#fetch the options selected by the user for model training
@app.route("/var_selection",methods=["POST"])
def selection():
    
    if request.method=="POST":
        sel_independent=request.form.getlist(('independent'))
        sel_dependent=request.form.get('dependent')
        user_email = session['email']
        algorithms = request.form['algorithm']
        selected_range=float(request.form['selected_range'])
        from main import selectioned
        selectioned(sel_independent, sel_dependent,algorithms,selected_range,user_email)
    

        user_data = users_collection.find_one({'email': user_email})
        models = user_data.get("models", []) if user_data else []

        

        return render_template('trian.html', models=models)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/forgot')
def resetpass():
    return render_template('forgot_password.html')



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True,port=6210)
    
