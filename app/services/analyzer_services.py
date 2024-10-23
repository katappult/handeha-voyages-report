from app.utils.utils import fill_country


class DataAnalyzer:
    @staticmethod
    def set_country(df):
        print("Setting country ...")
        return fill_country(df)

    @staticmethod
    def drop_unused_column(df):
        columns_to_drop = ['oid', 'latitude', 'longitude']
        print("Dropping unused column ...")
        return df.drop(columns=columns_to_drop)
