from cqu_covid import app

@app.route('/')
def index():
    title = app.config['title']
    return title