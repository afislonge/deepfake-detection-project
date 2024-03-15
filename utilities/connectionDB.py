# import needed libraries
from pymongo import MongoClient                

#connection string
MONGODB_URI = 'mongodb+srv://gotudeepfake:lambton3014@cluster0.jpdo5rg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(MONGODB_URI)

db = client.deepfake
collect= db.deepfake_report

print(client.list_database_names())  
print(db.list_collection_names())

# insert document in deepfake_report collection
def insert_test_doc():
    collect= db.deepfake_report                   # access to test collection

    # struct of the document 
    deepfake_report={
        "number_submitted":0 ,
        "real_images_caught":0,
        "fake_images_caught":0
    }
    # insert the documento and get id of the document created in var inserted_id 
    inserted_id= collect.insert_one(deepfake_report).inserted_id 
    print(inserted_id)

insert_test_doc()
print(db.list_collection_names())