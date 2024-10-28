import pandas as pd
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import POSTGRES_DB

Base = declarative_base()


class CleanedSearchHistory(Base):
    __tablename__ = 'cleaned_search_history'
    id = Column(Integer, primary_key=True)
    create_date = Column(TIMESTAMP)
    created_by = Column(String(255))
    operating_system = Column(String(255))
    browser = Column(String(255))
    local_ip_address = Column(String(255))
    device_version = Column(String(255))
    device = Column(String(2048))
    people_count = Column(Integer)
    departure_date = Column(TIMESTAMP)
    ip_address = Column(String(255))
    regions = Column(String(255))
    themes = Column(String(255))
    country = Column(String(255))


class CleanedNavigationHistory(Base):
    __tablename__ = 'cleaned_navigation_history'
    id = Column(Integer, primary_key=True)
    create_date = Column(TIMESTAMP)
    created_by = Column(String(255))
    referer = Column(String(255))
    operating_system = Column(String(255))
    browser = Column(String(255))
    local_ip_address = Column(String(45))
    voyage_identifier = Column(String(255))
    url_visited = Column(String(2048))
    device_version = Column(String(255))
    ip_address = Column(String(255))
    device = Column(String(255))
    country = Column(String(255))


class GenGlobalNavigationHistory(Base):
    __tablename__ = 'gen_global_navigation_history'
    oid = Column(Integer, primary_key=True)
    create_date = Column(TIMESTAMP)
    created_by = Column(String(255))
    operating_system = Column(String(255))
    referer = Column(String(255))
    browser = Column(String(255))
    local_ip_address = Column(String(255))
    voyage_identifier = Column(String(255))
    url_visited = Column(String(2048))
    device_version = Column(String(255))
    ip_address = Column(String(45))
    device = Column(String(255))
    country = Column(String(255))
    latitude = Column(FLOAT())
    longitude = Column(FLOAT())


class GenGlobalSearchHistory(Base):
    __tablename__ = 'gen_global_search_history'
    oid = Column(Integer, primary_key=True)
    create_date = Column(TIMESTAMP)
    created_by = Column(String(255))
    operating_system = Column(String(255))
    browser = Column(String(255))
    local_ip_address = Column(String(255))
    device_version = Column(String(255))
    device = Column(String(255))
    people_count = Column(Integer)
    departure_date = Column(TIMESTAMP)
    ip_address = Column(String(255))
    regions = Column(String(255))
    themes = Column(String(255))
    country = Column(String(255))
    latitude = Column(FLOAT())
    longitude = Column(FLOAT())


class DatabaseFetcher:
    db_url = POSTGRES_DB

    def __init__(self):
        # Create the engine to connect to the PostgreSQL database
        self.engine = create_engine(self.db_url)
        # Create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)
        # Create a session instance
        self.session = self.Session()

    def fetch_cleaned_navigation_history(self, start_date=None, end_date=None):
        try:
            query = self.session.query(CleanedNavigationHistory)

            if start_date:
                query = query.filter(CleanedNavigationHistory.create_date >= start_date)
            if end_date:
                query = query.filter(CleanedNavigationHistory.create_date <= end_date)

            cleaned_navigation_history = query.order_by(CleanedNavigationHistory.create_date.asc()).all()

            df_navigation_history = pd.DataFrame([entry.__dict__ for entry in cleaned_navigation_history])
            df_navigation_history = df_navigation_history.drop(columns='_sa_instance_state', errors='ignore')

            return df_navigation_history
        except Exception as e:
            print(f"Error fetching cleaned navigation history: {e}")
        finally:
            self.session.close()

    def fetch_cleaned_search_history(self, start_date=None, end_date=None):
        try:
            query = self.session.query(CleanedSearchHistory)

            if start_date:
                query = query.filter(CleanedSearchHistory.create_date >= start_date)
            if end_date:
                query = query.filter(CleanedSearchHistory.create_date <= end_date)

            cleaned_search_history = query.order_by(CleanedSearchHistory.create_date.asc()).all()

            df_search_history = pd.DataFrame([entry.__dict__ for entry in cleaned_search_history])
            df_search_history = df_search_history.drop(columns='_sa_instance_state', errors='ignore')

            return df_search_history
        except Exception as e:
            print(f"Error fetching cleaned search history: {e}")
        finally:
            self.session.close()

    def fetch_gen_global_navigation_history(self, start_date=None, end_date=None):
        try:
            query = self.session.query(GenGlobalNavigationHistory)
            print("query ", query)

            if start_date:
                query = query.filter(GenGlobalNavigationHistory.create_date >= start_date)
            if end_date:
                query = query.filter(GenGlobalNavigationHistory.create_date <= end_date)

            gen_global_navigation_history = query.order_by(GenGlobalNavigationHistory.create_date.asc()).all()

            df_navigation_history = pd.DataFrame([entry.__dict__ for entry in gen_global_navigation_history])
            df_navigation_history = df_navigation_history.drop(columns='_sa_instance_state', errors='ignore')

            return df_navigation_history
        except Exception as e:
            print(f"Error fetching gen global navigation history: {e}")
        finally:
            self.session.close()

    def fetch_gen_global_search_history(self, start_date=None, end_date=None):
        try:
            query = self.session.query(GenGlobalSearchHistory)

            if start_date:
                query = query.filter(GenGlobalSearchHistory.create_date >= start_date)
            if end_date:
                query = query.filter(GenGlobalSearchHistory.create_date <= end_date)

            gen_global_search_history = query.order_by(GenGlobalSearchHistory.create_date.asc()).all()

            df_search_history = pd.DataFrame([entry.__dict__ for entry in gen_global_search_history])
            df_search_history = df_search_history.drop(columns='_sa_instance_state', errors='ignore')

            return df_search_history
        except Exception as e:
            print(f"Error fetching gen global search history: {e}")
        finally:
            self.session.close()

    def insert_cleaned_navigation_history(self, df):
        try:
            for index, row in df.iterrows():
                new_cleaned_navigation_history = CleanedNavigationHistory(**row.to_dict())
                self.session.add(new_cleaned_navigation_history)
            self.session.commit()
            print(f"Cleaned navigation history added successfully.")
        except Exception as e:
            self.session.rollback()  # Rollback the transaction if there's an error
            print(f"Error inserting cleaned navigation history: {e}")
        finally:
            self.session.close()

    def insert_cleaned_search_history(self, df):
        try:
            for index, row in df.iterrows():
                new_cleaned_search_history = CleanedSearchHistory(**row.to_dict())
                self.session.add(new_cleaned_search_history)
            self.session.commit()
            print(f"Cleaned search history added successfully.")
        except Exception as e:
            self.session.rollback()  # Rollback the transaction if there's an error
            print(f"Error inserting cleaned search history: {e}")
        finally:
            self.session.close()
