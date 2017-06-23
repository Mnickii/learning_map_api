import os

from api import create_flask_app


configuration = os.getenv("FLASK_CONFIG")
app = create_flask_app(configuration)


@app.route('/')
def index():
    return "Yo, it's working!"

if __name__ == "__main__":
    app.run()
