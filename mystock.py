import os

if __name__ == '__main__':
    from app import create_app
    app = create_app(os.getenv('ENV') or 'default')
    app.run(debug=True)
