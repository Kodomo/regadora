from web import create_app

iapp = create_app()

if __name__ == '__main__':
    iapp.run(host='0.0.0.0')
