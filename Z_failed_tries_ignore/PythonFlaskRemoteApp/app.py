from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.migration


@application.route('/')
def showMachineList():
    return render_template('list.html')


@application.route("/getMoveList",methods=['POST'])
def getMachineList():
    try:
        moves = db.movement.find()
        
        moveList = []
        for move in moves:
            print(move)
            moveItem = {
                    'count':move['count'],
                    'in':move['in'],
                    'out':move['out'],
                    'year':move['year'],
                    'id': str(machine['_id'])
                    }
            moveList.append(moveItem)
    except e:
        return str(e)
    return json.dumps(moveList)


if __name__ == "__main__":
    application.run(host='0.0.0.0')

