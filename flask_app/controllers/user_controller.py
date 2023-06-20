from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

#Import Models as Class into Controller to use their classmethods
#from flask_app.controller.name_model import classname

# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================
@app.route('/')
def index():
    return render_template('reg_log.html')

@app.route('/recipes')
def show_all_recipes():
    if 'user_id' not in session:
        return redirect ('/')
    one_user = User.get_user_by_id({'id' : session['user_id']})

    all_recipes = Recipe.get_all_recipes()

    return render_template('dashboard.html', one_user=one_user, all_recipes=all_recipes)

@app.route('/register', methods=['POST'])
def successful_registration():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    new_user_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.save(new_user_data)

    session['user_id'] = user_id

    return redirect ('/recipes')

# ====================================
# Login Validations Route
# ====================================

@app.route('/login_user', methods=['POST'])
def login_user():
    email_data = {
        'email' : request.form['email']
    }

    user_in_db = User.get_user_by_email(email_data)

    if not user_in_db:
        flash('Invalid Email/Password.', 'login')
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['loginpassword']):
        flash('Invalid Email/Password.', 'login')
        return redirect ('/')
    session['user_id'] = user_in_db.id
    return redirect('/recipes')


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect ('/')



# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================
@app.route('/success/<int:user_id>')
def show_success(user_id):
    if 'user_id' not in session:        #must be successfully registered or logged in to make it here
        return redirect('/')
    newUser = User.get_user_by_id({'user_id' : user_id})
    return render_template('')







# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================

@app.route('/update', methods=['POST'])
def update_name():
    User.update(request.form)
    return redirect('/')







# ====================================
#    Delete Routes
# ====================================

# @app.route('/delete/<int:user_id>')
# def delete(user_id):
#     data = {
#         'id' : user_id
#     }

#     Recipe.delete(data)
#     return redirect('/')