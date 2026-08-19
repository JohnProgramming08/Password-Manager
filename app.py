from api import create_app

app = create_app()
app.run(port=8000, debug=False, host="0.0.0.0")
