from apscheduler.schedulers.blocking import BlockingScheduler
from app.telly_api import repository, vin_generator, vin_service

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def update_cars():
    found = 0
    while (found < 10):
        print(f"Getting car {found}")
        vin_service.get_next_car()
        found += 1


sched.start()
