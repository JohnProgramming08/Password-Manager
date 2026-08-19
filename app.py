from api import create_app

app = create_app()
app.run(port=8000, debug=False)
