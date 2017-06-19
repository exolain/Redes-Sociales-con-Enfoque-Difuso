from pymongo import MongoClient
import csv
from bson.son import SON
import pprint

client = MongoClient('localhost:27017')
db = client.migration

for year in range(2014,2017):
    migration_data = '/home/lain/Redes-Sociales-con-Enfoque-Difuso/scikit-cmeans/data/clean/'+str(year)+'.csv'

    csv_rows = []
    with open(migration_data) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(1,len(title))}])
            
    for i in csv_rows:
        i['year']=year

    db.migration.insert(csv_rows)

    pipeline=[
        {"$group": {"_id" : {"region_residencia":"$region_residencia","residencia_hace_dos_anos":"$residencia_hace_dos_anos"},  "number":  { "$sum" : 1} }}, 
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
    test=db.migration.aggregate(pipeline)

    for t in test:
        json = {'out': t['_id']['region_residencia'], 
        'in': t['_id']['residencia_hace_dos_anos'], 
        'count':t['number'], 'year':year}

        db.movement.insert_one(json)

