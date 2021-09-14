from flask import Flask, render_template, url_for, request, session, redirect, escape
#import pymongo
#import bcrypt

import pickle
import sklearn
import numpy as np
import math

app = Flask(__name__)

infile = open("model (1).pkl", "rb")
model = pickle.load(infile)
infile.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['departments']
        education = request.form['graduation']
        employed = request.form['self_employed']
        credit = request.form['credit_history']
        area = request.form['property_area']
        ApplicantIncome = float(request.form['applicant_income'])
        CoapplicantIncome = float(request.form['co_applicant_income'])
        LoanAmount = float(request.form['loan_amount'])
        Loan_Amount_Term = float(request.form['loan_term'])

        # gender
        if (gender == "Male"):
            male = 1
        else:
            male = 0

        # married
        if (married == "Yes"):
            married_yes = 1
        else:
            married_yes = 0

        # dependents
        if (dependents == '1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif (dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif (dependents == "3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0

            # education
        if (education == "Not Graduate"):
            not_graduate = 1
        else:
            not_graduate = 0

        # employed
        if (employed == "Yes"):
            employed_yes = 1
        else:
            employed_yes = 0

        # property area

        if (area == "Semiurban"):
            semiurban = 1
            urban = 0
        elif (area == "Urban"):
            semiurban = 0
            urban = 1
        else:
            semiurban = 0
            urban = 0
        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog, LoanAmountlog, Loan_Amount_Termlog, totalincomelog,
                                     male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate,
                                     employed_yes, semiurban, urban]])

        # print(prediction)

        if (prediction == "N"):
            prediction = "Sorry! Not applicable for the Loan"
        else:
            prediction = "Congratulations! You are apllicable for the Loan"

        return render_template("prediction.html", prediction_text="Result: {}".format(prediction))
    else:
        return render_template('prediction.html')



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=False)