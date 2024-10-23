# How to Run the Project

## Running in Development Mode

1 **Set Up a Virtual Environment:**

   ```bash
   python3 -m venv server_env
   source server_env/bin/activate  # On Windows use `server_env\Scripts\activate`
   ```

2 **Install Dependencies:**
With the virtual environment activated, install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

Run the API from the command line with the following syntax:

```
python ./main.py
```

build the docker image

```
docker build -t handeha_voyage_report .
```

## Run the docker image

- localhost postgresql :
  ```
  docker run -d -e POSTGRES_DB=postgresql://new_user:new_password@host.docker.internal:5432/handeha_voyage -p 5000:5000 handeha_voyage_report
  ```
- other postgresql :
  ```
  docker run -d -e POSTGRES_DB=postgresql://new_user:new_password@new_host:5432/handeha_voyage -p 5000:5000 handeha_voyage_report
  ```
- Allow CORS :
  ```
  docker run -d -e POSTGRES_DB=... -e CORS_ALLOWED=http://localhost:3001,http://localhost:8081 -p 5000:5000 handeha_voyage_report
  ```
- Customize CRON
  ```
  docker run -d -e POSTGRES_DB=... -e CORS_ALLOWED=... -e DAILY_CRON_HOUR=8 -e DAILY_CRON_MINUTE=0 -e WEEKLY_CRON_DAY_OF_WEEK=thu -e WEEKLY_CRON_HOURS=9 -e WEEKLY_CRON_MINUTES=0 -e MONTHLY_CRON_DAY=1 -e MONTHLY_CRON_HOURS=10 -e MONTHLY_CRON_MINUTES=0 -e YEARLY_CRON_MONTH=1 -e YEARLY_CRON_DAY=1 -e YEARLY_CRON_HOURS=0 -e YEARLY_CRON_MINUTES=0 -p 5000:5000 handeha_voyage_report
  ``` 

## the api doc is in

```
http://localhost:5000/apidocs/
```

## Note

Ensure that you have the necessary database connections and access rights set up before running the script. The script
assumes the existence of certain database tables and structures.
