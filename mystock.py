import os

if __name__ == '__main__':
    from app import create_app
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(debug=True)
