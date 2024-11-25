from App import app  # This assumes your Dash app is defined in 'app.py' as `app`

if __name__ == "__main__":
    app.run_server(debug=False)  # This is optional, Gunicorn will take care of running the app
