import csv
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

def load_ingredients():
    with open('ingredients.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

ingredients = load_ingredients()

@app.route('/')
def index():
    return render_template('index.html', brews=brews)

@app.route('/brew/<int:brew_id>')
def brew_details(brew_id):
    brew = get_brew_by_id(brew_id)
    latest_update = get_latest_update(brew_id)
    if latest_update:
        latest_contents = latest_update.get('contents', brew['ingredients'])
    else:
        latest_contents = brew.get('ingredients', '')
    return render_template('brew_details.html', brew=brew, latest_contents=latest_contents, brew_id=brew_id)

@app.route('/delete-brew/<int:brew_id>', methods=['POST'])
def delete_brew(brew_id):
    if request.method == 'POST':
        # Delete brew code here
        return redirect('/')

@app.route('/new-brew')
def new_brew():
    # New brew code here
    return redirect('/')

@app.route('/abv-calculator')
def abv_calculator():
    # ABV calculator code here
    return render_template('abv_calculator.html', abv=round(abv, 2))

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
