import os

from flask import current_app

from api import create_app


configuration = os.getenv("FLASK_CONFIG")

app = create_app(configuration)

@app.route('/')
def index():
    return 'Yo, it\'s working!'

if __name__ == "__main__":
    app.run()
