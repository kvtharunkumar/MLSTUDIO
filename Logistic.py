from datetime import datetime
import pickle
import re
from bson import Binary
from pydantic import model_serializer
from pymongo import MongoClient
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def Logisticregression(x, y,selected_range):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=selected_range, shuffle=True)

    l = LogisticRegression()
    model=l.fit(x_train, y_train)
    pred = l.predict(x_test)

    score = r2_score(y_test, pred)
    return score,model

    

