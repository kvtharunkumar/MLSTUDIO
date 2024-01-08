from linear import linear
from Logistic import Logisticregression
from svm import SVM
from navie import naive_bayes
from Decision_tree import DT
def func(x,y,selected_range):
    lis={'linear_regression':{'score':0,'model':""},'logistic_regression':{'score':0,'model':""},'SupportVectorMachine':{'score':0,'model':""},'Navie_bayes':{'score':0,'model':""},'DecisionTree':{'score':0,'model':""}}
    max_score = float('-inf')
    best_model_name = None
    if y.nunique()<=10:
        score, model = Logisticregression(x, y)
        lis['logistic_regression']['score'] = score
        lis['logistic_regression']['model'] = model
        score1,model1=SVM(x,y,selected_range)
        lis['SupportVectorMachine']['score'] = score1
        lis['SupportVectorMachine']['model'] = model1
        score2,model2=DT(x,y,selected_range)
        lis['DecisionTree']['score'] = score2
        lis['DecisionTree']['model'] = model2
        score3,model3=naive_bayes(x,y,selected_range)
        lis['Navie_bayes']['score'] = score3
        lis['Navie_bayes']['model'] = model3

        for model_name, values in lis.items():
            score = values['score']
            if score > max_score:
                max_score = score
                best_model = model_name
            lis={'linear_regression':{'score':0,'model':""},'logistic_regression':{'score':0,'model':""},'SupportVectorMachine':{'score':0,'model':""},'Navie_bayes':{'score':0,'model':""},'DecisionTree':{'score':0,'model':""}}
    max_score = float('-inf')
    best_model = None
    if y.nunique()<=10:
        score, model = Logisticregression(x, y)
        lis['logistic_regression']['score'] = score
        lis['logistic_regression']['model'] = model
        score1,model1=SVM(x,y,selected_range)
        lis['SupportVectorMachine']['score'] = score1
        lis['SupportVectorMachine']['model'] = model1
        score2,model2=DT(x,y,selected_range)
        lis['DecisionTree']['score'] = score2
        lis['DecisionTree']['model'] = model2
        score3,model3=naive_bayes(x,y,selected_range)
        lis['Navie_bayes']['score'] = score3
        lis['Navie_bayes']['model'] = model3

        for model_name, values in lis.items():
            score = values['score']
            if score > max_score:
                max_score = score
                best_model_name = model_name

            best_model = lis[best_model_name]['model']

        return  max_score,best_model,best_model_name

    else:
        score, model =linear(x, y)
        lis['logistic_regression']['score'] = score
        lis['logistic_regression']['model'] = model
        score1,model1=SVM(x,y,selected_range)
        lis['SupportVectorMachine']['score'] = score1
        lis['SupportVectorMachine']['model'] = model1
        score2,model2=DT(x,y,selected_range)
        lis['DecisionTree']['score'] = score2
        lis['DecisionTree']['model'] = model2
        score3,model3=naive_bayes(x,y,selected_range)
        lis['Navie_bayes']['score'] = score3
        lis['Navie_bayes']['model'] = model3
        
        for model_name, values in lis.items():
            score = values['score']
            if score > max_score:
                max_score = score
                best_model_name = model_name

            best_model = lis[best_model_name]['model']

        return  max_score,best_model,best_model_name
