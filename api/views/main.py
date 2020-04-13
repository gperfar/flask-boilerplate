from flask import Blueprint, request
from api.models import db, User, Sentence, Connection, Postgres
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

main = Blueprint("main", __name__)  # initialize blueprint

# function that is called when you visit /
@main.route("/")
def index():
    return "<h1>Hello, Ring Bearer</h1>"

@main.app_errorhandler(404)
def page_not_found(e):
    return "<h1>404: Not found</h1><p>\" I have no memory of this place\".</p><p>Gandalf the Grey</p> <img src=\"https://media1.tenor.com/images/034e7f9bd0df198f758dad87858b0004/tenor.gif?itemid=9228837\">", 404
    
@main.route('/runquery', methods=['POST'])
def runquery():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "connection_id" not in data:
        msg = "You can't run a query if you don't specify which connection to use."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "query" not in data:
        msg = "You can't run a query if you don't give me the query..."
        logger.info(msg)
        return create_response(status=422, message=msg)
    sentence = Sentence(name="Temporary sentence", sql_query=data["query"], connection = data["connection_id"], comment = "Temporary sentence")
    connection = Connection.query.get(data["connection_id"])
    try:
        results_json = sentence.execute()
        return json.dumps({'connection_id':connection.id,'connection name': connection.name,'sentence': sentence.sql_query,'results': results_json})
    except(Exception) as error:
        create_response(status=500,message= error)

@main.route('/runquery', methods=['GET']) #PROBAR SIEMPRE CON LA CONNECTION DE ID 3 Y SENTENCE DE ID 2
def runquery_get():
    query_params = request.args
    sentence_id = query_params.get('sentence_id')
    if (not(sentence_id)):
        msg = "Missing sentence_id" 
        return create_response(status=422, message=msg)
    sentence = Sentence.query.get(sentence_id)
    connection = Connection.query.get(sentence.connection)
    results_json = sentence.execute()
    return json.dumps({'connection name': connection.name,'sentence': sentence.sql_query,'results': results_json})

# function that is called when you visit /persons
@main.route("/init", methods=["GET"])
def init_data():
    #Users
    dummyusers =[]
    dummyusers.append(User(name="Aragorn", email="AragornStrider@gondor.com", password="KingOfGondor123"))
    dummyusers.append(User(name="Gandalf", email="WhiteWizard@gondor.com", password="FlyYouFools!"))
    db.session.add_all(dummyusers)
    db.session.commit()
    #Connections
    dummyconnections =[]
    postgres1 = Postgres(name="Aragorn's Connection 1", host="AragornStrider.gondor.com", database="Gondor", username = "userr", password = "password", comment = "",user = 1)
    postgres2 = Postgres(name="Aragorn's Connection 2", host="AragornStrider2.gondor.com", database="Gondor2", username = "userr2", password = "password2",comment = "", user = 1)
    postgres3 = Postgres(name = "Real Connection", host = "drona.db.elephantsql.com", database = "uvqhwsnn", username = "uvqhwsnn", password = "mzwjhs6qcqZHTm-ecCXJkQ3FoLViB9RT", comment = "Conexión real! Base Northwind", user = 2)
    dummyconnections.append(postgres1)
    dummyconnections.append(postgres2)
    dummyconnections.append(postgres3)
    db.session.add_all(dummyconnections)
    db.session.commit()
    #Sentences
    sentence1 = Sentence(name="Sentence 1", sql_query="SELECT * FROM people WHERE kingdom = 'Rohan'", connection = 1, comment = "Keeping tabs on the Rohirrim")
    sentence2 = Sentence(name="Sentence 2", sql_query="SELECT * FROM Customers", connection = 3, comment = "Keeping tabs on Customers") 
    db.session.add(sentence1)
    db.session.add(sentence2)
    db.session.commit()
    msg = "Data has been initialized :D"
    return create_response(status=200, message=msg)


# function that is called when you visit /connections
@main.route("/connections", methods=["GET"])
def get_connections():
    connections = Connection.query.all()
    return create_response(data={"connections": serialize_list(connections)})

@main.route("/connections/postgres", methods=["GET"])
def get_postgres():
    postgres = Postgres.query.all()
    return create_response(data={"postgres": serialize_list(postgres)})
# POST request for /connections
@main.route("/connections", methods=["POST"])
def create_connection():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "host" not in data:
        msg = "No host provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "database" not in data:
        msg = "No database provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "username" not in data:
        msg = "No username provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "password" not in data:
        msg = "No password provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "user_id" not in data:
        msg = "No user_id provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "comment" not in data:
        data["comment"] = ""
    if ("type" not in data):
        msg = "No type provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    # create SQLAlchemy Object
    if data["type"] == "postgres":
        new_postgres = Postgres(name=data["name"], host = data["host"], database = data["database"], username = data["username"], password = data["password"], user = data["user_id"], comment = data["comment"])
    # commit it to database
    db.session.add(new_postgres)
    db.session.commit()
    return create_response(
        message=f"Successfully created connection {new_postgres.name} with id: {new_postgres.id}"
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
        msg = "No name provided for user."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "email" not in data:
        msg = "No email provided for user."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "password" not in data:
        msg = "No password provided for user."
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
    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for sentence."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "sql_query" not in data:
        msg = "No SQL query provided for sentence."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "connection_id" not in data:
        msg = "No connection ID provided for sentence."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "comment" not in data:
        data["comment"] = ""
    # create SQLAlchemy Object
    new_sentence = Sentence(name = data["name"], sql_query=data["sql_query"], connection = data["connection_id"], comment = data["comment"])
    # commit it to database
    db.session.add(new_sentence)
    db.session.commit()
    return create_response(
        message=f"Successfully created sentence {new_sentence.name} with id: {new_sentence.id}"
    )