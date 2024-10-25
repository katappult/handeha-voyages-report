from datetime import timedelta, datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flasgger import Swagger
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from flask_restful import Api

from app.analyser import analyser
from app.config import CORS_ALLOWED, DAILY_CRON_HOUR, DAILY_CRON_MINUTE, WEEKLY_CRON_HOURS, WEEKLY_CRON_MINUTES, \
    MONTHLY_CRON_DAY, MONTHLY_CRON_HOURS, MONTHLY_CRON_MINUTES, YEARLY_CRON_MONTH, YEARLY_CRON_DAY, \
    YEARLY_CRON_HOURS, YEARLY_CRON_MINUTES, WEEKLY_CRON_DAY_OF_WEEK
from app.routes.global_routes.global_device_count_routes import GlobalDeviceCount
from app.routes.global_routes.global_device_type_count_routes import GlobalDeviceTypeCount
from app.routes.global_routes.global_navigation_count_routes import GlobalNavigationCount
from app.routes.global_routes.global_referer_count_routes import GlobalRefererCount
from app.routes.global_routes.global_sale_routes import GlobalSale
from app.routes.global_routes.global_search_regions_routes import GlobalSearchRegions
from app.routes.global_routes.global_search_themes_routes import GlobalSearchThemes
from app.routes.global_routes.global_voyage_count_routes import GlobalVoyageCount
from app.routes.voyage_routes.voyage_country_count_routes import VoyageCountryCount
from app.routes.voyage_routes.voyage_sale_routes import VoyageSale
from app.utils.database import Base
from app.utils.fetcher import Fetcher


def create_app():
    app = Flask(__name__)
    api = Api(app)
    Compress(app)
    swagger = Swagger(app, template={
        "info": {
            "title": "Handeha voyage data analysis report API",
            "description": "An API using Flask",
            "version": "1.0.0"
        }
    })
    CORS(app, origins=CORS_ALLOWED)

    scheduler = BackgroundScheduler()

    # Daily job
    @scheduler.scheduled_job(CronTrigger(hour=DAILY_CRON_HOUR, minute=DAILY_CRON_MINUTE))
    def daily_job():
        start_date = datetime.now() - timedelta(days=2)
        end_date = datetime.now() - timedelta(days=1)
        period_type = "day"
        print("Daily data analysis")
        analyser(start_date.strftime("%Y-%m-%d %H:%M"), end_date.strftime("%Y-%m-%d %H:%M"), period_type)

    # Weekly job
    @scheduler.scheduled_job(
        CronTrigger(day_of_week=WEEKLY_CRON_DAY_OF_WEEK, hour=WEEKLY_CRON_HOURS, minute=WEEKLY_CRON_MINUTES))
    def weekly_job():
        start_date = datetime.now() - timedelta(weeks=1)
        end_date = datetime.now() - timedelta(days=1)
        period_type = "week"
        print("Weekly data analysis")
        analyser(start_date.strftime("%Y-%m-%d %H:%M"), end_date.strftime("%Y-%m-%d %H:%M"), period_type)

    # Monthly job
    @scheduler.scheduled_job(CronTrigger(day=MONTHLY_CRON_DAY, hour=MONTHLY_CRON_HOURS, minute=MONTHLY_CRON_MINUTES))
    def monthly_job():
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now() - timedelta(days=1)
        period_type = "month"
        print("Monthly data analysis")
        analyser(start_date.strftime("%Y-%m-%d %H:%M"), end_date.strftime("%Y-%m-%d %H:%M"), period_type)

    # Yearly job
    @scheduler.scheduled_job(
        CronTrigger(month=YEARLY_CRON_MONTH, day=YEARLY_CRON_DAY, hour=YEARLY_CRON_HOURS, minute=YEARLY_CRON_MINUTES))
    def yearly_job():
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now() - timedelta(days=1)
        period_type = "year"
        print("Yearly data analysis")
        analyser(start_date.strftime("%Y-%m-%d %H:%M"), end_date.strftime("%Y-%m-%d %H:%M"), period_type)

    scheduler.start()

    fetcher = Fetcher.fetcher
    Base.metadata.create_all(fetcher.engine)

    api.add_resource(GlobalDeviceCount, '/global_device_count')
    api.add_resource(GlobalDeviceTypeCount, '/global_device_type_count')
    api.add_resource(GlobalSearchRegions, '/global_search_regions')
    api.add_resource(GlobalSearchThemes, '/global_search_themes')
    api.add_resource(GlobalNavigationCount, '/global_navigation_count')
    api.add_resource(GlobalRefererCount, '/global_referer_count')
    api.add_resource(GlobalVoyageCount, '/global_voyage_count')
    api.add_resource(GlobalSale, '/global_sale')
    api.add_resource(VoyageSale, '/voyage_sale')
    api.add_resource(VoyageCountryCount, '/voyage_country_count')

    return app
