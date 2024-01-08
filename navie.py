from datetime import datetime
import pickle
import re
from bson import Binary
from pydantic import model_serializer
from pymongo import MongoClient
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def naive_bayes(x, y,selected_range):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=selected_range, shuffle=True)

    l = GaussianNB()
    model=l.fit(x_train, y_train)
    pred = l.predict(x_test)

    score = accuracy_score(y_test, pred)
    
    return score,model
    

