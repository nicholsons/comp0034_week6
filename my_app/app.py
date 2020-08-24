from my_app import create_app, config

app = create_app(config.Config)


@app.route('/')
def index():
    return 'This is the home page for my_app'


if __name__ == '__main__':
    app.route()
