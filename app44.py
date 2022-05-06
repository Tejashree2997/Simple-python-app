#import dns.resolver
# dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers=['8.8.8.8']
# mongodb://Customer:Customer@localhost:27017/?readPreference=primary&ssl=false
import email
from flask import Flask, render_template, request, redirect, url_for, session, g
from bson import ObjectId  # For ObjectId to work
from http import client
import bcrypt
#from flask_session import Session

# import pymongo
from pymongo import MongoClient
#from bson.json_util import dumps
#import json
import sys
import subprocess
import shlex
#subprocess.run(["ls", "-l"])

app = Flask(__name__)

#SECRET_KEY must be set in config to access session:
app.config['SECRET_KEY'] = 'AJDJRJS24$($(#$$33--' 


def get_db():
    client = MongoClient(host='app_mongodb',
                         port=27017,
                         username='Customer',
                         password='Customer',
                         authSource="admin"
                         )
    db = client["Customer"]
    print ("Connected")
    return db

def getNextIP(EnvType,p):
    s = '.'
    #cursor = db.todo.find().sort({"_id":-1}).limit(1)
    #key = EnvType
    #refer = "Environment"    
    address_space = ""
    for doc in todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1):
        address_space = doc["Address_Space"]
        
    #p = 1	
    listOfrange = address_space.split(s)
    listOfrange[p] = str(int(listOfrange[p])+1)
    return s.join(listOfrange)

def getMongoSub(EnvType,p):
    s = '.'
    #cursor = db.todo.find().sort({"_id":-1}).limit(1)
    #key = EnvType
    #refer = "Environment"    
    mongo_subnet = ""
    for doc in todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1):
        mongo_subnet = doc["Mongo_Subnet"]
    
    #p = 1	
    listOfrange = mongo_subnet.split(s)
    listOfrange[p] = str(int(listOfrange[p])+1)
    return s.join(listOfrange)

def getREL_IDSub(EnvType,p):
    s = '.'
    #cursor = db.todo.find().sort({"_id":-1}).limit(1)
    #key = EnvType
    #refer = "Environment"    
    relid_subnet = ""
    for doc in todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1):
        relid_subnet = doc["Rel-ID_Subnet"]
    
    #p = 1
    listOfrange = relid_subnet.split(s)
    listOfrange[p] = str(int(listOfrange[p])+1)
    return s.join(listOfrange)


title = "To Save requirements from Customer"
heading = "Customer Requirements"

#client = MongoClient('app_mongodb:27017')
#client = MongoClient("mongodb+srv://Customer:customer@cluster0.usknk.mongodb.net/Customer?retryWrites=true&w=majority")

db = get_db()
# client.get_database('Customer')   #Select the database
todos = db.todo  # collection for storing customer information
records = db.register

def redirect_url():
    return request.args.get('next') or \
        request.referrer or ('index')

#@app.before_request
#def load_user():
#    if session["username"]:
#        user = records.find_one(username=session["Username"]).first()
#    else:
#        user = {"name": "Guest"}  # Make it better, use an anonymous User instead
#
#    g.user = user

@app.route("/", methods=['post', 'get'])
def index():
    
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        username = request.form.get("Username")
        email = request.form.get("email")
        password = request.form.get("password")
        session["Username"] = username
        
        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in',))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in",))
                message = 'Wrong password'
                return render_template('index.html', message=message)
        else:
            message = 'Email not found'
            return render_template('index.html', message=message)
    return render_template('index.html', message=message)


@app.route("/Register", methods=["POST", "GET"])
def Register():
    
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("Username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #role = request.form.get("role")
        
        #if found in database showcase that it's found 
        user_found = records.find_one({"Username": user})
        email_found = records.find_one({"email": email})
        #role_found = records.find_one({"role": role})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('Register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('Register.html', message=message)
        #if role_found:
         #   message = 'This username already exist in database'
          #  return render_template('Register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('Register.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'Username': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to login page for login
            return render_template('registered.html', email=new_email)
    return render_template('Register.html')


@app.route("/login", methods=["POST", "GET"])
def login():

    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        username = request.form.get("Username")
        email = request.form.get("email")
        password = request.form.get("password")
        session["username"] = username
        print(username)

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('index.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():

    todos_l = todos.find({})
    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a1 = "active"
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email, a1=a1, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)
    else:
        return redirect(url_for("login"))

@app.route("/list")
def lists():
    
    todos_l = todos.find()

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a1 = "active"
    return render_template('logged_in.html', a1=a1, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/")
@app.route("/uncompleted")
def tasks():
   
    # Display the Uncompleted Tasks
    print('Calling logged_in.html')
    todos_l = todos.find({"done": "no"})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])
    print('calling logged_in.html')
    a2 = "active"
    return render_template('logged_in.html', a2=a2, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/completed")
def completed():
    
    # Display the Completed Tasks
    todos_l = todos.find({"done": "yes"})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a3 = "active"
    return render_template('logged_in.html', a3=a3, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/done")
def done():
    
    # Done-or-not ICON
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})
    if(task[0]["done"] == "yes"):
        todos.update({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
    else:
        todos.update({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})
    redir = redirect_url()

    return redirect(redir)

@app.route("/action", methods=['POST'])
def action():

    name = request.form.get("name")
    envtype = request.form.get("environment")
    date = request.form.get("date")
    region = request.form.get("region")
    #username = request.form.get("Username")
    username = session["Username"] = request.form.get("Username")
    
    if envtype == "Development":
        newaddressspace = getNextIP(envtype,1)
        print(newaddressspace)
        NewMongoSubnet = getMongoSub(envtype,1)
        print(NewMongoSubnet)
        todos.insert_one({ "name": name, "Environment": envtype,
                     "date": date, "Region": region, "Address_Space":newaddressspace, "Mongo_Subnet":NewMongoSubnet, "done": "no"})

        subprocess.call(shlex.split(f"./0-Start.sh {name} {envtype} \"{region}\" {newaddressspace} {NewMongoSubnet}"))

    else:
        newaddressspace = getNextIP(envtype,1)
        print(newaddressspace)
        NewMongoSubnet = getMongoSub(envtype,1)
        print(NewMongoSubnet)
        NewRelIDSubnet = getREL_IDSub(envtype,1)
        print(NewRelIDSubnet)
        todos.insert_one({"name": name, "Environment": envtype,
                     "date": date, "Region": region, "Address_Space":newaddressspace, "Mongo_Subnet":NewMongoSubnet, "Rel-ID_Subnet":NewRelIDSubnet, "done": "no"})

        subprocess.call(shlex.split(f"./0-Start.sh {name} {envtype} \"{region}\" {newaddressspace} {NewMongoSubnet} {NewRelIDSubnet}"))
        
    # print(environment)
    # return redirect('index.html', regions=regions, answers=regions)
    #rc = subprocess.call("./script.sh")
    #subprocess.check_call(['./script.sh', 'name', 'region', 'envtype'])

    return redirect("/list") 

@app.route("/remove")
def remove():
    session['secrrt']='sec'
    # Deleting a Task with various references
    key = request.values.get("_id")
    todos.delete_one({"_id": ObjectId(key)})
    return redirect("/")

@app.route("/update")
def update():
    session['secrrt']='sec'
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    return render_template('update.html', tasks=task, h=heading, t=title, regions=regions, envtypes=envtypes)


@app.route("/action3", methods=['POST', 'GET'])
def action3():
    session['secrrt']='sec'
    # Updating a Task with various references
    name = request.values.get("name")
    envtype = request.values.get("environment")
    print("The type is : ", type(envtype))
    date = request.values.get("date")
    region = request.values.get("region")
    id = request.values.get("_id")
    todos.update_one({"_id": ObjectId(id)}, {'$set': {
                     "name": name, "Environment": envtype, "date": date, "Region": region}})
    return redirect("/")


@app.route("/search", methods=['GET'])
def search():
    session['secrrt']='sec'
    # Searching a Task with various references

    key = request.values.get("key")
    refer = request.values.get("refer")
    if(key == "_id"):
        todos_l = todos.find({refer: ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)


@app.route("/logout", methods=["POST", "GET"])

def logout():
    #session['secrrt']='sec'
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for("login"))
    else:
        return render_template('signout.html')

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
    sys.stdout.write("%s\n", app('environ', 'start_response'))
    
