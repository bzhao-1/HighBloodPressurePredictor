'''
High Blood Pressure Predictor web application using Flask. 

Team C: Ben, Bemnet, Ezra, CS 257 Winter 2023 
'''

import flask
from flask import render_template, request
import json
import sys
import psycopg2
import psqlConfig as config
from sqlapi import *
bp = BloodPressure(database=config.database, user=config.user, password=config.password, host="localhost")


app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/home')
def homeWithForm():
    '''
    Home for webpage where user can enter fields for query results.
    '''
    return render_template('home.html')    


@app.route('/aboutpage')
def aboutPage():
    return render_template('about.html')

@app.route('/sourcepage')
def sourcePage():
    return render_template('source.html')

@app.route('/results', methods=['POST'])
def searchResult():
    '''
    This method is executed once you submit the simple form. It embeds the form responses
    into a web page.
    '''
    if request.method == 'POST':
        try:
            result = get_query_fields(request)
            print(result)
            if result['menu'] == '(1)':
                errorHandlingString(result, False)
                result['image_url'] = bp.plotAverageSystolicBP(result['country'], result['gender'])
                return render_template('results_template1.html', result = result)
            if result['menu'] == '(2)':
                errorHandlingInt(result)
                errorHandlingString(result, True)
                result['image_url'] = bp.plotSortByCountry(result['country'], result['year'])
                return render_template('results_template2.html', result = result)
            if result['menu'] == '(3)':
                errorHandlingInt(result)
                result['image_url'] = bp.plotSortByYear(result['year'])
                return render_template('results_template3.html', result = result)
            if result['menu'] == '(4)':
                errorHandlingString(result, False)
                result['image_url'] = bp.plotAverageDiastolicBP(result['country'], result['gender'])
                return render_template('results_template4.html', result = result)
            if result['menu'] == '(5)':
                errorHandlingString(result, False)
                result['image_url'] = bp.plotcountryContainsTop5(result['country'], result['gender'])
                return render_template('results_template5.html', result = result)
            if result['menu'] == '(6)':
                errorHandlingString(result, False)
                result['image_url_systolic'] = bp.plotAverageSystolicBP(result['country'], result['gender'])
                result['image_url_diastolic'] = bp.plotAverageDiastolicBP(result['country'], result['gender'])
                result['health_metric'] = bp.systolicAndDiastolicAverageBP(result['country'], result['gender'])
                return render_template('results_template6.html', result = result)
            else:
                raise ValueError("Invalid query type")
        except ValueError:
            return render_template('error_template.html')
        
        
def get_query_fields(request):
    '''
    Helper method to collect all fields from a form and returns them as a dictionary.
    '''
    data = {}
    for field in request.form:
        if field == 'year':
            if not request.form[field].isdigit():
                data[field] = ''
            else:
                data[field] = int(request.form[field])
        else:
            data[field] = request.form[field]
    return data


def errorHandlingString(result, skipGenderCheck):
    '''
    Helper method for error handling.
    '''
    countries = bp.countriesList()
    if result['country'] not in countries:
        raise ValueError("Invalid country")
    elif not skipGenderCheck and result['gender'] not in ['Male', 'Female']:
        raise ValueError("Invalid gender")
    else:
        pass

def errorHandlingInt(result):
    if not isinstance(result['year'], int) or result['year'] < 1975 or result['year'] > 2015:
        raise ValueError("Invalid input")
    else:
        pass

'''
Run the program by typing 'python3 localhost [port]', where [port] is one of 
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)

