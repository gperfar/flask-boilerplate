from flask import Blueprint, request
from api.models import db, User, Sentence, Connection
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect

main = Blueprint("main", __name__)  # initialize blueprint


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    # access the logger with the logger from api.core and uses the standard logging module
    # try using ipdb here :) you can inject yourself
    logger.info("Hello, Ring Bearer")
    return "<h1>Hello, Ring Bearer</h1>"

# function that is called when you visit /persons
@main.route("/init", methods=["GET"])
def init_data():
    dummyusers =[]
    user1 = User(name="Aragorn", email="AragornStrider@gondor.com", password="KingOfGondor123")
    user2 = User(name="Gandalf", email="WhiteWizard@gondor.com", password="FlyYouFools!")
    dummyusers.append(user1)
    dummyusers.append(user2)
    db.session.add_all(dummyusers)
    # db.session.add(person1)
    # db.session.add(person2)
    db.session.commit()
    return "Data has been initialized :D"

@main.app_errorhandler(404)
def page_not_found(e):
    return "<h1>404: Not found</h1><p>\" I have no memory of this place\".</p><p>Gandalf the Grey</p> <img src=\"https://media1.tenor.com/images/034e7f9bd0df198f758dad87858b0004/tenor.gif?itemid=9228837\">", 404

# function that is called when you visit /connections
@main.route("/connections", methods=["GET"])
def get_connections():
    connections = Connection.query.all()
    return create_response(data={"connections": serialize_list(connections)})


# function that is called when you visit /users
@main.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()
    return create_response(data={"users": serialize_list(users)})

# POST request for /users
@main.route("/users", methods=["POST"])
def create_person():
    data = request.get_json()

    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "email" not in data:
        msg = "No email provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)

    # create SQLAlchemy Objects
    new_user = User(name=data["name"])
    new_person.emails.append(email)

    # commit it to database
    db.session.add_all([new_user, email])
    db.session.commit()
    return create_response(
        message=f"Successfully created person {new_user.name} with id: {new_user._id}"
    )
