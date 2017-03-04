from application import app

if __name__ == '__main__':
    host, port = app.config['SERVER_NAME'].split(":")
    app.run(host=host, port=int(port))
