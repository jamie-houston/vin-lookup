import os
from app import create_app, db
from flask_migrate import Migrate

config_name = os.getenv('FLASK_CONFIG')
app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
