import os
from apscheduler.schedulers.blocking import BlockingScheduler
from app.telly_api import vin_service
from app import create_app

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=30)
def update_cars():
    scraping_enabled = os.getenv("ENABLE_SCRAPING", False)
    batch_size = os.getenv("SCRAPER_BATCH_SIZE", 500)
    if scraping_enabled != 'True':
        print("scraping not enabled")
    else:
        config_name = os.getenv('FLASK_CONFIG')
        app = create_app(config_name)
        app.app_context().push()
        vin_service.get_next_batch(batch_size)


sched.start()
