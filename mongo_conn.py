import os
import pymongo

from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')
cluster_name = os.getenv('CLUSTER_NAME')

cluster_url = f"mongodb+srv://{user_name}:{password}@{cluster_name}.7ncch.mongodb.net/test?retryWrites=true&w=majority"

db_client = pymongo.MongoClient(cluster_url)

db = db_client[database_name]
