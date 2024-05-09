# app.py
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# List to store brews
brews = []

@app.route('/')
def index():
    return render_template('index.html', brews=brews)

@app.route('/new-brew')
def new_brew():
    return render_template('new_brew.html')

@app.route('/save-brew', methods=['POST'])
def save_brew():
    if request.method == 'POST':
        brew = {
            "name": request.form['brew-name'],
            "start_date": request.form['start-date'],
            "total_volume": request.form['total-volume'],
            "start_sg": request.form['start-sg'],
            "ingredients": request.form['ingredients']
        }
        brews.append(brew)
        return redirect('/')
    return render_template('index.html', brews=brews)

@app.route('/brew/<int:brew_id>')
def brew_details(brew_id):
    brew = brews[brew_id]
    return render_template('brew_details.html', brew=brew)

@app.route('/abv-calculator')
def abv_calculator():
    return render_template('abv_calculator.html')

@app.route('/calculate-abv', methods=['POST'])
def calculate_abv():
    if request.method == 'POST':
        start_sg = float(request.form['start-sg'])
        end_sg = float(request.form['end-sg'])
        abv = (start_sg - end_sg) * 131.25
        return render_template('abv_calculator.html', abv=abv)
    return redirect('/abv-calculator')

if __name__ == '__main__':
    app.run(debug=True)
