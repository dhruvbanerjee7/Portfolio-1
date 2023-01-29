from flask import Flask, render_template, request
import pandas as pd
# from sklearn.ensemble import RandomForestRegressor

def predict_results_BMA(data):
    
    job = ['management', 'technician', 'entrepreneur', 'blue-collar', 'unknown', 'retired', 'admin.', 'services', 'self-employed',
           'unemployed', 'housemaid', 'student']
    marital = ['married', 'single', 'divorced']
    education = ['tertiary', 'secondary', 'unknown', 'primary']
    housing = ['yes', 'no']
    month = ['may', 'jun', 'jul', 'aug', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'sep']


    
    
    modelfile = open('GB_model.pkl', 'rb')
    
    jb = data["job"]
    mar = data["marital"]
    ed = data["education"]
    hou = data["housing"]
    mon = data["month"]
    input1 = pd.DataFrame(data, index = [1])
    input1.columns = ['age', 'job_'+str(jb), 'marital_'+str(mar), 'education_'+str(ed), 'balance', 'housing_'+str(hou), 'day','month_'+str(mon), 'duration', 'campaign']
    
    for i in job:
        # print(i)
        input1["job_"+str(i)] = 0
    input1["job_"+str(jb)] = 1    
    
    for i in marital:
        # print(i)
        input1["marital_"+str(i)] = 0
    input1["marital_"+str(mar)] = 1    

    for i in education:
        # print(i)
        input1["education_"+str(i)] = 0
    input1["education_"+str(ed)] = 1  
    
    for i in housing:
        # print(i)
        input1["housing_"+str(i)] = 0
    input1["housing_"+str(hou)] = 1  

    for i in month:
        # print(i)
        input1["month_"+str(i)] = 0
    input1["month_"+str(mon)] = 1    

    
    import pickle

    res = pickle.load(modelfile)

    prob = res.predict(input1)

    
    return prob

def predict_results(data):
    
    aspiration = ["std","turbo"]
    carbody = ["convertible","hardtop","hatchback","sedan","wagon"]

    drivewheel = ["4wd","fwd","rwd"]

    
    
    modelfile = open('rf_final_v1.pkl', 'rb')
    # u = data["peakrpm"]
    asp = data["aspiration"]
    cb = data["carbody"]
    dw = data["drivewheel"]

    input1 = pd.DataFrame(data, index = [1])
    input1.columns = ['symboling', 'doornumber', 'carlength', 'carwidth', 'carheight','cylindernumber', 'enginesize',
                      'stroke', 'horsepower','peakrpm', 'highwaympg',   
                      "aspiration_"+str(asp),"carbody_"+str(cb),"drivewheel_"+str(dw)]
    
    for i in aspiration:
        # print(i)
        input1["aspiration_"+str(i)] = 0
    input1["aspiration_"+str(asp)] = 1    
    
    for i in carbody:
        # print(i)
        input1["carbody_"+str(i)] = 0
    input1["carbody_"+str(cb)] = 1    

    for i in drivewheel:
        # print(i)
        input1["drivewheel_"+str(i)] = 0
    input1["drivewheel_"+str(dw)] = 1  
    
    
    import pickle
    res = pickle.load(modelfile)

    prob = res.predict(input1)
    pred_df1 = round(prob[0],2)
    
    return pred_df1

# Configure application
app = Flask(__name__)

@app.route('/index', methods=['POST', 'GET'])
# @app.route('/', methods=['POST', 'GET'])
def index():

    greeting = 'Welcome to My Data Science Portfolio Website'

    return render_template('/index.html')


@app.route('/cpp', methods=['POST', 'GET'])
def home():
    to_predict_list = request.form.to_dict()
    return render_template('cpp.html')

@app.route('/predict_cpp',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    to_predict_list = request.form.to_dict()
    # to_predict_list1 = request.form.get("aspiration")
    # to_predict_list = to_predict_list.update(to_predict_list1)
    prediction = predict_results(to_predict_list)

    # output = round(prediction[0], 2)

    return render_template('cpp.html', prediction_text='The car price should be ${}'.format(prediction))

@app.route('/BMA', methods=['POST', 'GET'])
def home_BMA():
    to_predict_list = request.form.to_dict()
    return render_template('BMA.html')

@app.route('/predict_bma',methods=['POST'])
def predict_BMA():
    '''
    For rendering results on HTML GUI
    '''
    to_predict_list = request.form.to_dict()

    prediction = predict_results_BMA(to_predict_list)
    prediction = prediction[0]

    return render_template('BMA.html', prediction_text='Will the customer by the new scheme: {}'.format(prediction))

@app.route('/cpp_api', methods=['POST', 'GET'])
def api():
    to_predict_list = request.form.to_dict()
    print(to_predict_list)
    return to_predict_list


if __name__ == '__main__':
    app.run(debug=True)