from flask import Flask
from flask_cors import CORS
from movie_app.config import Config
from movie_app.models import init_db
from movie_app.routes import bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

init_db(app)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)



