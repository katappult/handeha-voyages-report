# Use the official Python slim image as the base
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .

# Install pip and project dependencies, consider using psycopg2-binary
RUN pip3 install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the application will run on
EXPOSE 5000

# Set default environment variables
ENV POSTGRES_DB=postgresql://postgres:test@host.docker.internal:5432/handeha_voyage
ENV CORS_ALLOWED=http://localhost:5173,http://localhost:3000,http://localhost:8080
ENV DAILY_CRON_HOUR=8
ENV DAILY_CRON_MINUTE=0
ENV WEEKLY_CRON_DAY_OF_WEEK=thu
ENV WEEKLY_CRON_HOURS=9
ENV WEEKLY_CRON_MINUTES=0
ENV MONTHLY_CRON_DAY=1
ENV MONTHLY_CRON_HOURS=10
ENV MONTHLY_CRON_MINUTES=0
ENV YEARLY_CRON_MONTH=1
ENV YEARLY_CRON_DAY=1
ENV YEARLY_CRON_HOURS=0
ENV YEARLY_CRON_MINUTES=0

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
#CMD ["waitress-serve", "--port=5000", "main:app"]

