
from flask import Flask
from applications.database import db

app = None

def create_app():
    app = Flask(__name__)  # we can use flask functions when we call app variable
    app.secret_key = 'super_secret_unpredictable_key_string'
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

    db.init_app(app)

    app.app_context().push()  # activates Flask environment manually.
    return app


app = create_app()

from applications.controller import *  # written here because we need to define the app first
# from applications.models import * we will not write this as we don't need all things from model 
# so instead we will have an indirect connection 


if __name__ == '__main__':  # run this app only when it is invoked (called)
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(username="admin1").first()

        if admin is None:
            admin = User(id=1,
                username="admin1",
                email="admin1@admin.com",
                password="admin1",
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    app.run()






# note:
# When we run this file then flask will create a proxy object as current_app
# which we can use later in other files and it will also avoid
# circular import error. Mapping happens at this place.
# Milestone 0 check and Save.
