from main import app  # Replace 'app' with the actual name of your Flask application object

if __name__ == "__main__":
    # Create an instance of the Gunicorn application
    from gunicorn.app.wsgiapp import WSGIApplication
    gunicorn_app = WSGIApplication()
    gunicorn_app.app_uri = 'main:app'  # Replace 'app:app' with the actual module and Flask app object name

    # Start the Gunicorn server
    gunicorn_app.run()
