import os
import ast
from flask import Flask, g
from neo4j import GraphDatabase, basic_auth


DATABASE_USERNAME = "neo4j"
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_URL = "bolt://localhost"
driver = GraphDatabase.driver(
    DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
)
app = Flask(__name__)


def create_app():
    """
    Creates factory function for application.
    https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/
    """
    application = Flask(__name__, template_folder="templates")

    from flights.views import app

    application.register_blueprint(app)

    return application


def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    value = ""
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)


def get_db():
    if not hasattr(g, "neo4j_db"):
        g.neo4j_db = driver.session()
    return g.neo4j_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "neo4j_db"):
        g.neo4j_db.close()
