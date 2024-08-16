from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load and clean the Excel file
df = pd.read_excel('./data/all-vehicles-model.xlsx')
df = df.drop_duplicates(subset=['Make', 'Model'], keep='first')

@app.route('/', methods=['GET', 'POST'])
def index():
    makes = sorted(df['Make'].unique())
    comparison_results = []
    error = None
    
    if request.method == 'POST':
        num_cars = int(request.form['num_cars'])
        
        for i in range(1, num_cars + 1):
            make = request.form.get(f'make{i}')
            model = request.form.get(f'model{i}')
            
            car = df[(df['Make'] == make) & (df['Model'] == model)]

            # Handle cases where cars are not found or there are multiple entries
            if car.empty:
                error = f"Car {i} not found. Please check your selection."
                break
            elif len(car) > 1:
                error = f"Multiple entries found for car {i}. Please select specific entries if needed."
                break
            else:
                car_specs = car.iloc[0].to_dict()
                comparison_results.append(car_specs)

    return render_template('home.html', makes=makes, comparison_results=comparison_results, error=error)

@app.route('/get_models', methods=['POST'])
def get_models():
    make = request.form['make']
    models = sorted(df[df['Make'] == make]['Model'].unique())
    return jsonify(models=models)

if __name__ == '__main__':
    app.run(debug=True)













