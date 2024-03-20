import pickle
from bson import Binary
from pymongo import MongoClient
from datetime import datetime
from config import mongo

def Database(score,model,user_email,algorithm):
    if user_email:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Save the model using pickle
        model_filename = f"{timestamp}.pkl"
        serialized_model = Binary(pickle.dumps(model))
<<<<<<< HEAD
        mongo_uri = mongo()
=======
        mongo_uri =mongodb_URI
>>>>>>> 77710e9915e0814d7812d4b9cffe5c386ad8cbd5
        client = MongoClient(mongo_uri)
        db = client.mlstudio
        users_collection = db.users

        # Create a new model entry
        new_model_entry = {
            "algorithm": algorithm,
            "model_file_name": model_filename,
            "Accuracy":score,
            "model_file": serialized_model,
            # Add other relevant information such as accuracy
        }

        # Update the models array for the user
        users_collection.update_one({'email': user_email}, {'$push': {'models': new_model_entry}})


