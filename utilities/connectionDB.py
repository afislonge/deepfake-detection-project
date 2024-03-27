# import needed libraries
from dotenv import load_dotenv, find_dotenv
import os 
from pymongo import MongoClient                

load_dotenv(find_dotenv())                      # load environment file to use password saved as an evironment var
password = os.environ.get("MONGODB_PWD")        # assing password store in env var

#connection string
MONGODB_URI = f"mongodb+srv://gotudeepfake:{password}@cluster0.jpdo5rg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URI)

db = client.deepfake                            # DataBase
collect= db.deepfake_report                     # Collection to stores counter for report

print(client.list_database_names())  
print(db.list_collection_names())

# insert document in deepfake_report collection
def insert_doc():
    collect= db.deepfake_report                   # access to deepfake_report collection just as a test

    # struct of the document 
    deepfake_report={
        "number_submitted":0 ,
        "real_images_caught":0,
        "fake_images_caught":0
    }
    # insert the documento and get id of the document created in var inserted_id 
    inserted_id= collect.insert_one(deepfake_report).inserted_id 
    print(inserted_id)

insert_doc()
print(db.list_collection_names())