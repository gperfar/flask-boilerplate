from flask import Blueprint, request
from api.models import db, User, Sentence, Connection, Postgres, Visualization, Dashboard#, VisualizationLineChart
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect, func
import psycopg2, json

main = Blueprint("main", __name__)  # initialize blueprint

visualization_types=["Area chart", "Bar chart", "Line chart", "Area/Bar/Line chart","Radar chart", "Pie chart", "Radial bar chart", "Scatter chart"]
connection_types=["postgres"]

# function that is called when you visit /
@main.route("/")
def index():
    return "<h1>Hello, Ring Bearer</h1>"

@main.app_errorhandler(404)
def page_not_found(e):
    return "<h1>404: Not found</h1><p>\" I have no memory of this place\".</p><p>Gandalf the Grey</p> <img src=\"https://media1.tenor.com/images/034e7f9bd0df198f758dad87858b0004/tenor.gif?itemid=9228837\">", 404
    
@main.route('/runtemporaryquery', methods=['POST'])
def runtemporaryquery():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "connection_id" not in data:
        msg = "You can't run a query if you don't specify which connection to use."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "sql_query" not in data:
        msg = "You can't run a query if you don't give me the query..."
        logger.info(msg)
        return create_response(status=422, message=msg)
    try:
        conn = Connection.query.get(data["connection_id"]).start_connection()
        cur = conn.cursor()
        cur.execute(data["sql_query"])
        results= cur.fetchall()
        results_json = [dict(zip([key[0] for key in cur.description], row)) for row in results] #Googleada, ni idea cómo funciona pero it does
        return json.dumps({'sentence': data["sql_query"],'results': results_json})
    except(Exception) as error:
        create_response(status=500,message= error)

@main.route('/runquery', methods=['GET']) 
def runquery_get():
    query_params = request.args
    sentence_id = query_params.get('sentence_id')
    if (not(sentence_id)):
        msg = "Missing sentence_id" 
        return create_response(status=422, message=msg)
    try:
        sentence = Sentence.query.get(sentence_id)
        results_json = sentence.execute()
        return json.dumps({'connection name': sentence.connection.name,'sentence': sentence.sql_query,'results': results_json})
    except(Exception) as error:
        create_response(status=500,message= error)


@main.route('/runquery', methods=['POST']) 
def runquery_post():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "user_id" not in data:
        msg = "No user ID provided."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "sentence_id" not in data:
        msg = "No sentence ID provided."
        logger.info(msg)
        return create_response(status=422, message=msg)
    sentence = Sentence.query.get(data["sentence_id"])
    if sentence.connection.user_id == data["user_id"]:
        try:
            results_json = sentence.execute()
            return json.dumps({'connection name': sentence.connection.name,'sentence': sentence.sql_query,'results': results_json})
        except(Exception) as error:
            create_response(status=500,message= error)
    msg = "Sentence is not able to execute: user does not have access."
    logger.info(msg)
    return create_response(status=422, message=msg)

# Init
@main.route("/init", methods=["GET"])
def init_data():
    query_params = request.args
    user_id = query_params.get('user')
    if (not(user_id)):
        msg = "No user provided for init."
        logger.info(msg)
        return create_response(status=422, message=msg)
    # return user_id
    # #Users
    # dummyusers =[]
    # dummyusers.append(User(name="Aragorn", email="AragornStrider@gondor.com", password="KingOfGondor123"))
    # dummyusers.append(User(name="Gandalf", email="WhiteWizard@gondor.com", password="FlyYouFools!"))
    # db.session.add_all(dummyusers)
    # db.session.commit()
    #Connections
    dummyconnections =[]
    postgres1 = Postgres(name="Aragorn's Connection 1", host="AragornStrider.gondor.com", database="Gondor", username = "userr", password = "password", port = 5432, comment = "",user_id = user_id)
    # postgres2 = Postgres(name="Aragorn's Connection 2", host="AragornStrider2.gondor.com", database="Gondor2", username = "userr2", password = "password2",comment = "", user_id = user_id)
    postgres2 = Postgres(name = "Real Connection", host = "drona.db.elephantsql.com", database = "uvqhwsnn", username = "uvqhwsnn", password = "mzwjhs6qcqZHTm-ecCXJkQ3FoLViB9RT", port = 5432, comment = "Conexión real! Base Northwind", user_id = user_id)
    dummyconnections.append(postgres1)
    dummyconnections.append(postgres2)
    # dummyconnections.append(postgres3)
    db.session.add_all(dummyconnections)
    db.session.commit()
    #Sentences
    sentence1 = Sentence(name="Sentence 1", sql_query="SELECT * FROM people WHERE kingdom = 'Rohan'", connection_id = 1, comment = "Keeping tabs on the Rohirrim")
    sentence2 = Sentence(name="Sentence 2", sql_query="SELECT * FROM Customers", connection_id = 2, comment = "Keeping tabs on Customers") 
    sentence3 = Sentence(name="Sentence 3 - using GROUP", sql_query="SELECT city, COUNT(*) AS customers, (COUNT(*)*1.0/2)::float AS customershalf FROM Customers GROUP BY city", connection_id = 2, comment = "Customers we have in each city") 
    db.session.add(sentence1)
    db.session.add(sentence2)
    db.session.add(sentence3)
    # db.session.commit()
    #Visualizations
    visual1 = Visualization(
        name="Line Chart 1 - black", 
        sentence_id = 3, 
        type = "Line chart",
        comment = "Based on the real Sentence on the real Connection - 1", 
        params= {
            'columns':[
                {'name': 'city'},
                {'name': 'customers', 'color': '#FF0000', 'legend': 'Customers'}
                ], 
            'xaxis_label':'City', 
            'yaxis_label':'Number of Customers',
            'legend':True
        }
    )
    visual2 = Visualization(
        name="Bars, Bars, Bars!", 
        type="Bar chart",
        sentence_id = 3, 
        comment = "Based on the real Sentence on the real Connection", 
        params= {
            'columns':[
                {'name': 'city'},
                {'name': 'customers', 'color': 'MidnightBlue', 'legend': 'Active'}
                ], 
            'xaxis_label':'City', 
            'yaxis_label':'Number of Customers',
            'legend':True
        }
    )
    db.session.add(visual1)
    db.session.add(visual2)
    # db.session.commit()
    #Dashboards
    dash1 = Dashboard(name="Dashboard 1", comment = "No comment - 1")
    dash1.visualizations.append(visual1)
    dash2 = Dashboard(name="Dashboard 2", comment = "Dashboard with no comment - 2")
    db.session.add(dash1)
    db.session.add(dash2)
    db.session.commit()
    msg = "Data has been initialized :D"
    return create_response(status=200, message=msg)

####################################
############ Models ###############
####################################

############ Connections ###############
# function that is called when you visit /connections
@main.route("/connections", methods=["GET"])
def get_connections():
    query_params = request.args
    connection_id = query_params.get('id')
    if (not(connection_id)):
        connections = Connection.query.all()
        return create_response(data={"connections": serialize_list(connections)})
    ###### If there was a specific connection as parameter...
    connection_details = Connection.query.get(connection_id).get_fields()
    return create_response(data={"connection_details": connection_details})

# Return (with user ID)
@main.route("/connections", methods=["POST"])
def return_connections():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "user_id" not in data:
        msg = "No user ID provided for connection(s)."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "connection_id" not in data: #We return all connections
        connections = db.session.query(Connection).filter(
            Connection.user_id == data["user_id"]
            ).all()
        return create_response(data={"connections": serialize_list(connections)})
    connection = db.session.query(Connection).filter(
        Connection.id == data["connection_id"],
        Connection.user_id == data["user_id"]
        ).first()
    connection_details = connection.get_fields()
    connection_details.pop('_sa_instance_state', None)
    return create_response(data={"connection": connection_details})

@main.route("/connections/postgres", methods=["GET"])
def get_postgres():
    postgres = Postgres.query.all()
    return create_response(data={"postgres": serialize_list(postgres)})

@main.route("/connections/types", methods=["GET"])
def get_connection_types():
    types = connection_types
    # for connection in Connection.query.distinct(Connection.type):
    #     types.append(connection.type)
    return create_response(message="Type retrieval was a total success!", data={"connection types": types})

#Create
@main.route("/connection/create", methods=["POST"])
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
        new_postgres = Postgres(name=data["name"], host = data["host"], database = data["database"], username = data["username"], password = data["password"], user_id = data["user_id"], comment = data["comment"], port = data["port"])
    # commit it to database
    db.session.add(new_postgres)
    db.session.commit()
    return create_response(
        message=f"Successfully created connection {new_postgres.name} with id: {new_postgres.id}"
    )

#Test
@main.route("/connection/test", methods=["POST"])
def test_connection():
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
        new_postgres = Postgres(name=data["name"], host = data["host"], database = data["database"], username = data["username"], password = data["password"], user_id = data["user_id"], comment = data["comment"], port = data["port"])
        try:
            new_postgres.start_connection()
            return create_response(message=f"Test OK!")
        except:
            return create_response(status=422, message="FAILED")


@main.route("/connection/edit", methods=["POST"])
def edit_connection():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "connection_id" not in data:
        msg = "No ID provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
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
    
    if data["type"] == "postgres":
        # Fetch Connection
        pgconn = Connection.query.get(data["connection_id"])
        # Perform edit
        pgconn.name = data["name"]
        pgconn.host = data["host"]
        pgconn.database = data["database"]
        pgconn.username = data["username"]
        pgconn.password = data["password"]
        pgconn.user_id = data["user_id"]
        pgconn.comment = data["comment"]
        # Commit it to database
        db.session.commit()
    return create_response(
        message=f"Successfully edited connection {pgconn.name} with id: {pgconn.id}"
    )

# Delete
@main.route("/connection/delete", methods=["POST"])
def delete_connection():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "connection_id" not in data:
        msg = "No ID provided for connection."
        logger.info(msg)
        return create_response(status=422, message=msg)
    # Fetch Connection and delete
    db.session.query(Connection).filter(Connection.id == data["connection_id"]).delete()
    # Commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully deleted connection"
    )


############ Sentences ###############
# Return
@main.route("/sentences", methods=["GET"])
def get_sentences():
    query_params = request.args
    sentence_id = query_params.get('id')
    if (not(sentence_id)):
        sentences = Sentence.query.all()
        return create_response(data={"sentences": serialize_list(sentences)})
    ###### If there was a specific sentence as parameter...
    sentence = Sentence.query.get(sentence_id)
    sentence_details = sentence.__dict__
    sentence_details.pop('_sa_instance_state', None)
    # return sentence.connection.user_id
    return create_response(data={"sentence": sentence_details})
    
# Return (with user ID)
@main.route("/sentences", methods=["POST"])
def return_sentences():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "user_id" not in data:
        msg = "No user ID provided for sentences."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "sentence_id" not in data:
        sentences = db.session.query(Sentence).join(Connection).filter(
            Connection.user_id == data["user_id"]
            ).all()
        # return sentences 
        return create_response(data={"sentences": serialize_list(sentences)})
    sentence = db.session.query(Sentence).join(Connection).filter(
        Sentence.id == data["sentence_id"],
        Connection.user_id == data["user_id"]
        ).first()
    sentence_details = sentence.__dict__
    sentence_details.pop('_sa_instance_state', None)
    return create_response(data={"sentence": sentence_details})
    

# Create
@main.route("/sentence/create", methods=["POST"])
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
    new_sentence = Sentence(name = data["name"], sql_query=data["sql_query"], connection_id = data["connection_id"], comment = data["comment"])
    # commit it to database
    db.session.add(new_sentence)
    db.session.commit()
    return create_response(
        message=f"Successfully created sentence {new_sentence.name} with id: {new_sentence.id}"
    )

# Edit
@main.route("/sentence/edit", methods=["POST"])
def edit_sentence():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "sentence_id" not in data:
        msg = "No sentence ID provided for sentence."
        logger.info(msg)
        return create_response(status=422, message=msg)
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
    # Fetch Sentence
    sentence = Sentence.query.get(data["sentence_id"])
    # Perform edit
    sentence.connection_id = data["connection_id"]
    sentence.name = data["name"]
    sentence.sql_query = data["sql_query"]
    sentence.comment = data["comment"]
    # Commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully edited sentence {sentence.name} with id: {sentence.id}"
    )

# Delete
@main.route("/sentence/delete", methods=["POST"])
def delete_sentence():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "sentence_id" not in data:
        msg = "No ID provided for sentence."
        logger.info(msg)
        return create_response(status=422, message=msg)
    # Fetch Sentence and delete
    db.session.query(Sentence).filter(Sentence.id == data["sentence_id"]).delete()
    # Commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully deleted sentence"
    )

############ Visualizations ###############
# Return
@main.route("/visualizations", methods=["GET"])
def get_visualizations():
    visualizations = Visualization.query.all()
    return create_response(data={"visualizations": serialize_list(visualizations)})

@main.route("/visualizations/types", methods=["GET"])
def get_visualization_types():
    types = visualization_types #It's at the top
    return create_response(message="Type retrieval was a total success!", data={"visualization types": types})

# Return (with user ID)
@main.route("/visualizations", methods=["POST"])
def return_visualizations():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "user_id" not in data:
        msg = "No user ID provided for visualizations."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "visualization_id" not in data:
        visualizations = db.session.query(Visualization).join(Sentence).join(Connection).filter(
            Connection.user_id == data["user_id"]
            ).all()
        # return visualizations 
        return create_response(data={"visualizations": serialize_list(visualizations)})
    # If there was a specific visualization requested, fetch it and return it
    visualization = db.session.query(Visualization).join(Sentence).join(Connection).filter(
        Visualization.id == data["visualization_id"],
        Connection.user_id == data["user_id"]
        ).first()
    visualization_details = visualization.get_fields()
    # visualization_details.pop('_sa_instance_state', None)
    return create_response(data={"visualization": visualization_details})

# Create
@main.route("/visualization/create", methods=["POST"])
def create_visualization():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "sentence_id" not in data:
        msg = "No sentence ID provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "type" not in data:
        msg = "No type provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "comment" not in data:
        data["comment"] = ""
    # create SQLAlchemy Object
    new_visualization = Visualization(
        name = data["name"], 
        sentence_id = data["sentence_id"], 
        comment = data["comment"],
        params = data["params"],
        type = data["type"]
    )
    # if data["type"] == "Bar chart":
    #     new_visualization = VisualizationBarChart(
    #         name = data["name"], 
    #         sentence_id = data["sentence_id"], 
    #         comment = data["comment"],
    #         params = data["params"])
    # if data["type"] == "Area chart":
    #     new_visualization = VisualizationAreaChart(
    #         name = data["name"], 
    #         sentence_id = data["sentence_id"], 
    #         comment = data["comment"],
    #         params = data["params"])
    # commit it to database
    db.session.add(new_visualization)
    db.session.commit()
    return create_response(
        message=f"Successfully created visualization {new_visualization.name} with id: {new_visualization.id}"
    )

# Edit
@main.route("/visualization/edit", methods=["POST"])
def edit_visualization():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "visualization_id" not in data:
        msg = "No ID provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "name" not in data:
        msg = "No name provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "sentence_id" not in data:
        msg = "No sentence ID provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "comment" not in data:
        data["comment"] = ""
    # create SQLAlchemy Object
    if "params" not in data:
        msg = "No params provided for line chart visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    visual = Visualization.query.get(data["visualization_id"])
    visual.name = data["name"]
    visual.sentence_id = data["sentence_id"]
    visual.comment = data["comment"]
    visual.params = data["params"]
    visual.type = data["type"]
    # commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully edited visualization {visual.name} with id: {visual.id}"
    )

# Delete
@main.route("/visualization/delete", methods=["POST"])
def delete_visualization():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "visualization_id" not in data:
        msg = "No ID provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    # Fetch Sentence and delete
    db.session.query(Visualization).filter(Visualization.id == data["visualization_id"]).delete()
    # Commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully deleted visual."
    )

# Prepare Render
@main.route("/visualization/pre_render", methods=["POST"])
def pre_render_visualization():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "visualization_id" not in data:
        msg = "No ID provided for visualization."
        logger.info(msg)
        return create_response(status=422, message=msg)
    try:
        # Fetch Sentence
        visualization = db.session.query(Visualization).filter(Visualization.id == data["visualization_id"]).first()
        # Commit it to database
        results = visualization.pre_render()
        # return results
        return create_response(message=f"You were able to render the visualization!", data=results)
    except(Exception) as error:
        create_response(status=500,message= error)


############ Dashboards ###############
# Return
@main.route("/dashboards", methods=["GET"])
def get_dashboards():
    dashboards = Dashboard.query.all()
    return create_response(data={"dashboards": serialize_list(dashboards)})

# Return (with user ID)
@main.route("/dashboards", methods=["POST"])
def return_dashboards():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "user_id" not in data:
        msg = "No user ID provided for dashboards."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "dashboard_id" not in data:
        dashboards = db.session.query(Dashboard).join(Visualization, Dashboard.visualizations).join(Sentence).join(Connection).filter(
            Connection.user_id == data["user_id"]
            ).all()
        return create_response(data={"dashboards": serialize_list(dashboards)})
    dashboard = db.session.query(Dashboard).join(Visualization, Dashboard.visualizations).join(Sentence).join(Connection).filter(
        Dashboard.id == data["dashboard_id"],
        Connection.user_id == data["user_id"]
        ).first()
    dashboard_details = dashboard.__dict__
    dashboard_details.pop('_sa_instance_state', None)
    return create_response(data={"dashboard": dashboard_details})

# Create
@main.route("/dashboard/create", methods=["POST"])
def create_dashboard():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for dashboard."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "comment" not in data:
        data["comment"] = ""
    # create SQLAlchemy Object
    new_dashboard = Dashboard(
        name = data["name"], 
        comment = data["comment"])
    # commit it to database
    db.session.add(new_dashboard)
    db.session.commit()
    return create_response(
        message=f"Successfully created dashboard {new_dashboard.name} with id: {new_dashboard.id}"
    )

# Edit
@main.route("/dashboard/edit", methods=["POST"])
def edit_dashboard():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "dashboard_id" not in data:
        msg = "No ID provided for dashboard."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "name" not in data:
        msg = "No name provided for dashboard."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "comment" not in data:
        data["comment"] = ""
    # Fetch Dashboard
    dash = Dashboard.query.get(data["dashboard_id"])
    # Edit it
    dash.name = data["name"]
    dash.comment = data["comment"]
    ## Missing: add/remove visuals from dashboard
    # commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully edited dashboard {dash.name} with id: {dash.id}"
    )

# Delete
@main.route("/dashboard/delete", methods=["POST"])
def delete_dashboard():
    data = request.get_json()
    logger.info("Data recieved: %s", data)
    if "dashboard_id" not in data:
        msg = "No ID provided for dashboard."
        logger.info(msg)
        return create_response(status=422, message=msg)
    # Fetch Sentence and delete
    db.session.query(Dashboard).filter(Dashboard.id == data["dashboard_id"]).delete()
    # Commit it to database
    db.session.commit()
    return create_response(
        message=f"Successfully deleted dashboard."
    )





############ Dumpster ###############
@main.route("/logintest", methods=["GET"])
def login_test():
    query_params = request.args
    email = query_params.get('email')
    password = query_params.get('password')
    try:
        user = db.session.query(User).filter(User.email == email).first()
        successful_login = user.match_password(password = password)
        if successful_login:
            return create_response(message = "Welcome, you coding beast")
        return create_response(message = "You shall not pass!")
    except:
        return create_response(message = "You shall not pass!")

@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if "email" not in data:
        msg = "No email provided for login."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "password" not in data:
        msg = "No password provided for login."
        logger.info(msg)
        return create_response(status=422, message=msg)
    query_params = request.args
    email = data["email"]
    password = data["password"]
    try:
        user = db.session.query(User).filter(func.lower(User.email) == email.lower()).first()
        successful_login = user.match_password(password = password)
        if successful_login:
            # Identity can be any data that is json serializable
            return create_response(message = str(user.id))
        return create_response(status=400, message = "You shall not pass!")
    except:
        return create_response(status=400, message = "You shall not pass!")

############ Users ###############
# Return all
@main.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return create_response(data={"users": serialize_list(users)})

# Create
@main.route("/user/create", methods=["POST"])
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
