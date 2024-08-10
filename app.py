import csv
from flask import Flask, render_template, request

app = Flask(__name__)

# Load car data from CSV
car_data = {}
with open('data/car_data.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        car_name = row['car_name']  # Column A
        attribute_r = row['attributeR']  # Column R
        car_data[car_name] = {
            'attributeR': attribute_r
        }

@app.route('/')
def home():
    return render_template('home.html', models=list(car_data.keys()))

@app.route('/compare', methods=['POST'])
def compare():
    car1 = request.form['car1']
    car2 = request.form['car2']
    
    if car1 in car_data and car2 in car_data:
        specs1 = car_data[car1]
        specs2 = car_data[car2]
        return render_template('compare.html', car1=car1, car2=car2, specs1=specs1, specs2=specs2)
    else:
        return "One or both of the car names are not found."

if __name__ == '__main__':
    app.run(debug=True)


