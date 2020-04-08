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
    #Users
    dummyusers =[]
    user1 = User(name="Aragorn", email="AragornStrider@gondor.com", password="KingOfGondor123")
    user2 = User(name="Gandalf", email="WhiteWizard@gondor.com", password="FlyYouFools!")
    dummyusers.append(user1)
    dummyusers.append(user2)
    db.session.add_all(dummyusers)
    db.session.commit()
    #Connections
    dummyconnections =[]
    connection1 = Connection(
        name="Aragorn's Connection 1", host="AragornStrider.gondor.com", database="Gondor", username = "userr", password = "password", comment = "",user = 1)
    connection2 = Connection(
        name="Aragorn's Connection 2", host="AragornStrider2.gondor.com", database="Gondor2", username = "userr2", password = "password2",comment = "", user = 1)
    dummyconnections.append(connection1)
    dummyconnections.append(connection2)
    db.session.add_all(dummyconnections)
    db.session.commit()
    #Sentences
    sentence1 = Sentence(sentence="SELECT * FROM people WHERE kingdom = 'Rohan'", connection = 1, comment = "Keeping tabs on the Rohirrim")
    db.session.add(sentence1)
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

# POST request for /connections
@main.route("/connections", methods=["POST"])
def create_connection():
    data = request.get_json()
    # logger.info("Data recieved: %s", data)
    # if "name" not in data:
    #     msg = "No name provided for connection."
    #     logger.info(msg)
    #     return create_response(status=422, message=msg)
    # if "host" not in data:
    #     msg = "No host provided for connection."
    #     logger.info(msg)
    #     return create_response(status=422, message=msg)
    #AGREGAR EL RESTO DE LOS FIELDS (REQUIRED)

    # create SQLAlchemy Object
    new_connection = Connection(name=data["name"], host = data["host"], database = data["database"], username = data["username"], password = data["password"], user = data["user"], comment = data["comment"])
    # commit it to database
    db.session.add(new_connection)
    db.session.commit()
    return create_response(
        message=f"Successfully created connection {new_connection.name} with id: {new_connection.id}"
    )

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
    new_user = User(name=data["name"], email = data["email"], password = data["password"])

    # commit it to database
    db.session.add(new_user)
    db.session.commit()
    return create_response(
        message=f"Successfully created person {new_user.name} with id: {new_user.id}"
    )

# function that is called when you visit /sentences
@main.route("/sentences", methods=["GET"])
def get_sentences():
    sentences = Sentence.query.all()
    return create_response(data={"sentences": serialize_list(sentences)})

# POST request for /sentences
@main.route("/sentences", methods=["POST"])
def create_sentence():
    data = request.get_json()
    # logger.info("Data recieved: %s", data)
    # if "name" not in data:
    #     msg = "No name provided for connection."
    #     logger.info(msg)
    #     return create_response(status=422, message=msg)
    # if "host" not in data:
    #     msg = "No host provided for connection."
    #     logger.info(msg)
    #     return create_response(status=422, message=msg)
    #AGREGAR EL RESTO DE LOS FIELDS (REQUIRED)

    # create SQLAlchemy Object
    new_sentence = Sentence(sentence=data["sentence"], connection = data["connection"], comment = data["comment"])
    # commit it to database
    db.session.add(new_sentence)
    db.session.commit()
    return create_response(
        message=f"Successfully created connection {new_sentence.name} with id: {new_sentence.id}"
    )