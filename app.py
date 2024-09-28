from flask import Flask, render_template, request, redirect, url_for
from utils import preprocess_data  # Assuming utils.py contains the preprocess_data function
from model import train_model  # Assuming model.py contains your model training logic

app = Flask(__name__)

# Global variable for storing user budget
user_budget = 0.0

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    # Add logic to store user credentials (if required)
    return redirect(url_for('input_budget'))

@app.route('/input_budget', methods=['GET', 'POST'])
def input_budget():
    global user_budget
    if request.method == 'POST':
        user_budget = float(request.form['budget'])
        return redirect(url_for('scan_nutrition'))
    return render_template('input_budget.html')

@app.route('/scan_nutrition', methods=['GET', 'POST'])
def scan_nutrition():
    if request.method == 'POST':
        nutrition_info = request.files['nutrition_image']  # Get the nutrition image
        # Logic to process nutrition info (use preprocess_data function)
        return redirect(url_for('input_mrp'))
    return render_template('scan_nutrition.html')

@app.route('/input_mrp', methods=['GET', 'POST'])
def input_mrp():
    if request.method == 'POST':
        mrp = float(request.form['mrp'])  # Get MRP entered by user
        return redirect(url_for('results', mrp=mrp))  # Pass MRP to results page
    return render_template('input_mrp.html')

@app.route('/results/<float:mrp>')
def results(mrp):
    health_percentage = calculate_healthiness()  # Example function to calculate healthiness
    economic_feasibility = is_feasible(mrp, user_budget)  # Compare MRP with user budget
    return render_template('result.html', health_percentage=health_percentage, economic_feasibility=economic_feasibility)

def calculate_healthiness():
    # Placeholder logic, you can implement actual logic using your model
    return 85.5

def is_feasible(mrp, budget):
    return mrp <= budget

if __name__ == '__main__':
    app.run(debug=True)