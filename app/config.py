import os

POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'postgresql://postgres:test@localhost:5432/handeha_voyage'

CORS_ALLOWED = os.environ.get('CORS_ALLOWED') or ["http://localhost:5173", "http://localhost:3000",
                                                  "http://localhost:8080"]

DAILY_CRON_HOUR = os.environ.get('DAILY_CRON_HOUR') or "12"
DAILY_CRON_MINUTE = os.environ.get('DAILY_CRON_MINUTE') or "07"

WEEKLY_CRON_DAY_OF_WEEK = os.environ.get('WEEKLY_CRON_DAY_OF_WEEK') or "thu"
WEEKLY_CRON_HOURS = os.environ.get('WEEKLY_CRON_HOURS') or "9"
WEEKLY_CRON_MINUTES = os.environ.get('WEEKLY_CRON_MINUTES') or "34"

MONTHLY_CRON_DAY = os.environ.get('MONTHLY_CRON_DAY') or "1"
MONTHLY_CRON_HOURS = os.environ.get('MONTHLY_CRON_HOURS') or "10"
MONTHLY_CRON_MINUTES = os.environ.get('MONTHLY_CRON_MINUTES') or "0"

YEARLY_CRON_MONTH = os.environ.get('YEARLY_CRON_MONTH') or "1"
YEARLY_CRON_DAY = os.environ.get('YEARLY_CRON_DAY') or "1"
YEARLY_CRON_HOURS = os.environ.get('YEARLY_CRON_HOURS') or "0"
YEARLY_CRON_MINUTES = os.environ.get('YEARLY_CRON_MINUTES') or "0"
