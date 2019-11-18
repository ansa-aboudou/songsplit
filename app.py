# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import logging
import json
import sys
import os
import random
from spleeter.separator import Separator
import stripe

app = Flask(__name__)
app.secret_key = b'\xfe\xc1Z\x89\xb6\xb4\xfco\xa1(\xa9\xa2'
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

from flask_heroku import Heroku
heroku = Heroku(app)
#Stripe info

stripe_keys = {
  'secret_key': os.environ['secret_key'],
  'publishable_key': os.environ['publishable_key']
}
stripe.api_key = stripe_keys['secret_key']

# ======== Routing =========================================================== #
# -------- Landing ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

# -------- Login ------------------------------------------------------------- #
@app.route('/home', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    if not helpers.get_pay():
        return redirect(url_for('purchase'))
    user = helpers.get_user()
    return render_template('home.html', user=user)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))

# -------- Upload ---------------------------------------------------------- #
@app.route("/splitUpload", methods=['POST'])
def splitFileUpload():
    if helpers.get_pay():
        if 'file' in request.files:
            song = request.files['file']
            if song.filename != '':
                random_n = str(random.randint(1,1000000001))
                song_filename = session['username'] + random_n + "_" + song.filename
                song_path = os.path.join('static/upload', song_filename)
                output_path = 'static/upload'
                song.save(song_path)
                #output_path = 'static/upload/output'+ "_" + session['username'] + random_n
                #separator = Separator('spleeter:2stems')
                #separator.separate_to_file(song_path, output_path)
                #src_vocal = "../" + output_path + "/vocals.wav"
                #src_beat = "../" + output_path + "/accompaniment.wav"
                # We use the command line instead that uses less memory
                os.system(u'spleeter separate -i ' + song_path + ' -p spleeter:2stems -o ' + output_path)
                src_vocal = song_path[:-4] + "/vocals.wav"
                src_beat = song_path[:-4] + "/accompaniment.wav"
                return {'vocal': src_vocal, 'beat': src_beat}
    return json.dumps({'status': 'Error'})

# -------- Purchase ---------------------------------------------------------- #
@app.route('/purchase')
def purchase():
    if not session.get('logged_in'):
        return render_template('login.html')
    message = "Please purchase for $1.00 only."
    if helpers.get_pay():
        message = "Thank you for purchasing. You can also support us by purchassing again ;)"
    return render_template('purchase.html', key=stripe_keys['publishable_key'], message=message)

# -------- Charge ---------------------------------------------------------- #
@app.route('/charge', methods=['POST'])
def charge():
    try:
        # amount in cents
        amount = 100
        customer = stripe.Customer.create(
            email='sample@customer.com',
            source=request.form['stripeToken']
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )
        helpers.add_pay(session['username'])
        return redirect(url_for('login'))
    except stripe.error.StripeError:
        return redirect(url_for('login'))

# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
