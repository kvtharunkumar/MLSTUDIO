from datetime import datetime
import pickle
from bson import Binary
from pydantic import model_serializer
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def linear(x, y,selected_range):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=selected_range, shuffle=True)

    l = LinearRegression()
    model=l.fit(x_train, y_train)
    pred = l.predict(x_test)

    score = r2_score(y_test, pred)
    return score,model

    # from main import user_Email
    # if user_Email:
    #     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    #     # Save the model using pickle
    #     model_filename = f"{timestamp}.pkl"
    #     serialized_model = Binary(pickle.dumps(model))
    #     mongo_uri = "mongodb+srv://tharun:tharun123@cluster0.okkoxqs.mongodb.net/?retryWrites=true&w=majority"
    #     client = MongoClient(mongo_uri)
    #     db = client.mlstudio
    #     users_collection = db.users

    #     # Create a new model entry
    #     new_model_entry = {
    #         "algorithm": "linear_regression",
    #         "model_file_name": model_filename,
    #         "Accuracy":score,
    #         "model_file": serialized_model,
    #         # Add other relevant information such as accuracy
    #     }

    #     # Update the models array for the user
    #     users_collection.update_one({'email': user_Email}, {'$push': {'models': new_model_entry}})


