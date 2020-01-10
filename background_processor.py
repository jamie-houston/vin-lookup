import os
from apscheduler.schedulers.blocking import BlockingScheduler
from app.telly_api import repository, vin_generator, vin_service
from app import create_app, db

sched = BlockingScheduler()

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.app_context().push()

@sched.scheduled_job('interval', minutes=3)
def update_cars():
    found = 0
    while (found < 10):
        print(f"Getting car {found}")
        vin_service.get_next_car()
        found += 1


sched.start()
