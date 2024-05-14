import csv
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# List to store brews
brews = []

def load_ingredients():
    with open('ingredients.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

ingredients = load_ingredients()

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
            "ingredients": request.form['ingredients'],
            "readings": [],
            "updates": []
        }
        brews.append(brew)
        return redirect('/')
    return render_template('index.html', brews=brews)

@app.route('/brew/<int:brew_id>')
def brew_details(brew_id):
    brew = brews[brew_id]
    return render_template('brew_details.html', brew=brew, brew_id=brew_id)


@app.route('/delete-brew/<int:brew_id>', methods=['POST'])
def delete_brew(brew_id):
    if request.method == 'POST':
        del brews[brew_id]
        return redirect('/')
    return render_template('index.html', brews=brews)

@app.route('/update-brew/<int:brew_id>', methods=['POST'])
def update_brew(brew_id):
    if request.method == 'POST':
        brew = {
            "name": request.form['brew-name'],
            "start_date": request.form['start-date'],
            "total_volume": request.form['total-volume'],
            "start_sg": request.form['start-sg'],
            "ingredients": request.form['ingredients'],
            "readings": brews[brew_id]['readings'],
            "updates": brews[brew_id]['updates']
        }
        brews[brew_id] = brew
        return redirect('/')
    return render_template('index.html', brews=brews)

@app.route('/add-reading/<int:brew_id>', methods=['POST'])
def add_reading(brew_id):
    if request.method == 'POST':
        reading = {
            "date": request.form['reading-date'],
            "specific_gravity": request.form['specific-gravity']
        }
        brews[brew_id]['readings'].append(reading)
        return redirect('/brew/' + str(brew_id))
    return render_template('brew_details.html', brew=brews[brew_id], brew_id=brew_id)

@app.route('/add-update/<int:brew_id>', methods=['POST'])
def add_update(brew_id):
    if request.method == 'POST':
        update = {
            "date": request.form['update-date'],
            "state": request.form['new-state'],
            "contents": request.form['new-contents']
        }
        brews[brew_id]['updates'].append(update)
        return redirect('/brew/' + str(brew_id))
    return render_template('brew_details.html', brew=brews[brew_id], brew_id=brew_id)

@app.route('/abv-calculator')
def abv_calculator():
    return render_template('abv_calculator.html')

@app.route('/calculate-abv', methods=['POST'])
def calculate_abv():
    if request.method == 'POST':
        start_sg = float(request.form['start-sg'])
        end_sg = float(request.form['end-sg'])
        abv = (start_sg - end_sg) * 131.25
        return render_template('abv_calculator.html', abv=round(abv, 2))
    return redirect('/abv-calculator')

@app.route('/ingredients', methods=['GET', 'POST'])
def show_ingredients():
    if request.method == 'POST':
        selected_category = request.form.get('category')
        filtered_ingredients = [ingredient for ingredient in ingredients if ingredient['category'] == selected_category]
        return render_template('ingredients.html', ingredients_list=filtered_ingredients, selected_category=selected_category)
    else:
        return render_template('ingredients.html', ingredients_list=ingredients, selected_category=None)

if __name__ == '__main__':
    app.run(debug=True)
