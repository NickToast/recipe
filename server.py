from flask_app import app

#IMPORT CONTROLLERS INTO SERVER FILE

from flask_app.controllers import user_controller, recipe_controller

#run pipenv install PyMySQL flask flask-bcrypt
#Save .mwb file to folder (ERD)

if __name__ == "__main__":
    app.run(debug=True)