import csv
import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# list to store brews
brews = []

user_notes = []

#loads csv file for ingredients
def load_ingredients():
    with open('ingredients.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

ingredients = load_ingredients()

#renders index.html on launch page
@app.route('/')
def index():
    return render_template('index.html', brews=brews)

#renders new_brew.html
@app.route('/new-brew')
def new_brew():
    return render_template('new_brew.html')

#adds new brew to brews with data from /new-brew and taskes back to launch page
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

#route dependent on number of brew in brews, renders brew_details.html of chosen brew id
@app.route('/brew/<int:brew_id>')
def brew_details(brew_id):
    brew = brews[brew_id]
    return render_template('brew_details.html', brew=brew, brew_id=brew_id)

#deletes a brew from brews and renders launch page
@app.route('/delete-brew/<int:brew_id>', methods=['POST'])
def delete_brew(brew_id):
    if request.method == 'POST':
        del brews[brew_id]
        return redirect('/')
    return render_template('index.html', brews=brews)

#takes input from form in brew_details.html and adds reading to brew in brews of id of the page
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

#takes input from form in brew_details.html and adds update to brew in brews of id of the page
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

#renders abv_calculator.html 
@app.route('/abv-calculator')
def abv_calculator():
    return render_template('abv_calculator.html')

#takes inputs from /abv-calculator and runs abv calculation, renders page with calculated value
@app.route('/calculate-abv', methods=['POST'])
def calculate_abv():
    if request.method == 'POST':
        start_sg = float(request.form['start-sg'])
        end_sg = float(request.form['end-sg'])
        abv = (start_sg - end_sg) * 131.25
        return render_template('abv_calculator.html', abv=round(abv, 2))
    return redirect('/abv-calculator')

#renders all ingredients in /ingredients unless a category is chosen, then only that category of ingredient is shown

@app.route('/ingredients', methods=['GET', 'POST'])
def show_ingredients():
    random_ingredient = random.choice(ingredients)
    if request.method == 'POST':
        selected_category = request.form.get('category')
        filtered_ingredients = [ingredient for ingredient in ingredients if ingredient['category'] == selected_category]
        return render_template('ingredients.html', ingredients_list=filtered_ingredients, selected_category=selected_category, random_ingredient=random_ingredient)
    else:
        return render_template('ingredients.html', ingredients_list=ingredients, selected_category=None, random_ingredient=random_ingredient)
    
@app.route('/random-ingredient', methods=['GET'])
def random_ingredient():
    random_ingredient = random.choice(ingredients)
    return render_template('random_ingredient.html', random_ingredient=random_ingredient)

# Renders the note page where users can type notes
@app.route('/notes')
def show_notes():
    return render_template('notes.html', notes=user_notes)

# Saves the note entered by the user and redirects back to the notes page
@app.route('/save-note', methods=['POST'])
def save_note():
    if request.method == 'POST':
        note = request.form['note']
        user_notes.append(note)
    return redirect('/notes')


if __name__ == '__main__':
    app.run(debug=True)
