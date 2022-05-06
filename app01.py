#import dns.resolver
# dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers=['8.8.8.8']
# mongodb://Customer:Customer@localhost:27017/?readPreference=primary&ssl=false
from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId  # For ObjectId to work
# import pymongo
from pymongo import MongoClient
#from bson.json_util import dumps
#import json

import sys
import subprocess
#subprocess.run(["ls", "-l"])

app = Flask(__name__)


def get_db():
    client = MongoClient(host='app_mongodb',
                         port=27017,
                         username='Customer',
                         password='Customer',
                         authSource="admin")
    db = client["Customer"]
    return db

def getNextIP(EnvType,p):
    s = '.'
    # db.inventory.find().sort({_id:-1}).limit(1);
    # key = EnvType
    # refer = "Environment"    
    address_spaces = []#not taking address space from dummy entry
    cursor = todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1)
    
    for document in cursor:
        address_spaces.append(document['Address_Space'])        # <- append to the list
    print(address_spaces)
	# p = 1	
	#listOfrange = pIPaddress.split(s)
	#listOfrange[p] = str(int(listOfrange[p])+1)
	#return s.join(listOfrange)

title = "To Save requirements from Customer"
heading = "Customer Requirements"

#client = MongoClient('app_mongodb:27017')
#client = MongoClient("mongodb+srv://Customer:customer@cluster0.usknk.mongodb.net/Customer?retryWrites=true&w=majority")

db = get_db()
# client.get_database('Customer')   #Select the database
todos = db.todo  # collection for storing customer information


def redirect_url():
    return request.args.get('next') or \
        request.referrer or ('index')


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
    return render_template('index.html', a1=a1, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/")
@app.route("/uncompleted")
def tasks():
    # Display the Uncompleted Tasks
    todos_l = todos.find({"done": "no"})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a2 = "active"
    return render_template('index.html', a2=a2, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


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
    return render_template('index.html', a3=a3, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


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

    newaddressspace = getNextIP(envtype,2)
    todos.insert_one({"name": name, "Environment": envtype,
                     "date": date, "Region": region, "Address_Space":newaddressspace, "AS_Mask":"28", "Mongo_Subnet":newaddressspace, "MS_Mask":"29", "done": "no"})
    # print(environment)
    # return redirect('index.html', regions=regions, answers=regions)
    rc = subprocess.call("./script.sh")
    subprocess.check_call(['./script.sh', 'name', 'region', 'envtype'])
    return redirect("/list")


@app.route("/remove")
def remove():
    # Deleting a Task with various references
    key = request.values.get("_id")
    todos.delete_one({"_id": ObjectId(key)})
    return redirect("/")


@app.route("/update")
def update():
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
    # Searching a Task with various references

    key = request.values.get("key")
    refer = request.values.get("refer")
    if(key == "_id"):
        todos_l = todos.find({refer: ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
    sys.stdout.write("%s\n", app('environ', 'start_response'))