from cqu_covid import app

@app.route('/')
def index():
    return 'Hello World! This is flask.'