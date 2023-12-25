from flask import Flask, render_template, request, redirect, session
import os
import time
import json
import ml_module

app = Flask(__name__)

ingredients = ml_module.ingredients

# Initialize global variables for reviews
reviews = []

def check_Login(user, pas):
    try:
        with open('user.json', 'r') as f:
            data = json.load(f)
        if user in data.keys():
            if pas == data[user]:
                return True
            else:
                return False
        else:
            return False
    except:
        open('user.json', 'w')
        return False

def check_Register(user, pas):
    with open('user.json', 'r') as f:
        data = json.load(f)
    if user in data.keys():
        return False
    else:
        data[user] = pas
        with open('user.json', 'w') as f:
            json.dump(data, f)
        return True

@app.route('/', methods=["get", "post"])
def home():
    return render_template('login.html')

@app.route('/login', methods=["get", "post"])
def login():
    if request.method == "POST":
        formData = request.form
        username = formData['User']
        password = formData['Password']
        if check_Login(username, password):
            session['user'] = username  # Store the user in the session
            return redirect('/input_form')

    return "Invalid credentials"

@app.route('/register', methods=["get", "post"])
def register():
    if request.method == "POST":
        formData = request.form
        username = formData['User']
        password = formData['Password']
        if check_Register(username, password):
            return "Register Success"
    return "Done"

@app.route("/input_form", methods=["get", "post"])
def input_form():
    if 'user' not in session:
        return redirect('/')

    user = session['user']

    if request.method == "POST":
        Selected_Ingredients = request.form.getlist('Selected_ingredients[]')
        out_recom = ml_module.food_recommendation(Selected_Ingredients)

        return render_template("Results.html", output1=out_recom)

    return render_template('inputs_FormPage.html', ingredients=ingredients)

@app.route('/review', methods=['GET', 'POST'])
def review():
    if 'user' not in session:
        return redirect('/')

    user = session['user']
    success_message = None

    if request.method == 'POST':
        review_text = request.form.get('review', '')
        rating = request.form.get('rating', '')

        reviews.append({'user': user, 'review': review_text, 'rating': rating})
        save_reviews_to_file()

        success_message = 'Review submitted successfully!'

    user_reviews = get_user_reviews(user)
    return render_template('review.html', user_reviews=user_reviews, success_message=success_message)

def save_reviews_to_file():
    with open('reviews.json', 'w') as file:
        json.dump(reviews, file, indent=2)

def get_user_reviews(user):
    return [review for review in reviews if review['user'] == user]

if __name__ == '__main__':
    app.secret_key = '1234'  # Set a secret key for session management
    app.run(debug=True)
