from datetime import datetime

from app.services.analyzer_services import DataAnalyzer
from app.utils.database import Base
from app.utils.fetcher import Fetcher
from app.utils.utils import get_device_count, get_device_type_count, get_referer_count, get_country_count, \
    get_voyage_count, get_global_search_theme, get_global_search_region, get_global_sale


def analyser(start_date, end_date, period_type):
    analyzer = DataAnalyzer()
    fetcher = Fetcher.fetcher
    Base.metadata.create_all(fetcher.engine)

    try:
        df_navigation_history = fetcher.fetch_gen_global_navigation_history(start_date, end_date)
        df_search_history = fetcher.fetch_gen_global_search_history(start_date, end_date)

        df_navigation_history_with_country = analyzer.set_country(df_navigation_history)
        df_search_history_with_country = analyzer.set_country(df_search_history)

        df_cleaned_navigation_history_with_country = analyzer.drop_unused_column(df_navigation_history_with_country)
        df_cleaned_df_search_history_with_country = analyzer.drop_unused_column(df_search_history_with_country)

        fetcher.insert_cleaned_navigation_history(df_cleaned_navigation_history_with_country)
        fetcher.insert_cleaned_search_history(df_cleaned_df_search_history_with_country)

        new_df = fetcher.fetch_cleaned_navigation_history(start_date, end_date)
        new_df1 = fetcher.fetch_cleaned_search_history(start_date, end_date)

        get_device_count(new_df, True)
        get_device_type_count(new_df, True)
        get_referer_count(new_df, True)
        get_country_count(new_df, True)
        get_voyage_count(new_df, True)
        get_global_search_theme(new_df1, start_date, end_date, True)
        get_global_search_region(new_df1, start_date, end_date, True)
        get_global_sale(new_df, start_date, end_date, period_type, True)

        # # 4. Generate the report PDF
        # report_generator = ReportGenerator()
        # rapport = {
        #     'debutDate': '01/09/2024',
        #     'finDate': '07/09/2024',
        #     'voyages': [
        #         {
        #             'circuitOuSejour': 'Paris Tour',
        #             'reference': 'REF123',
        #             'nombreVue': 100,
        #             'nombreDemandeDevis': 5,
        #             'nombreVente': 2,
        #         },
        #         {
        #             'circuitOuSejour': 'Rome Getaway',
        #             'reference': 'REF456',
        #             'nombreVue': 150,
        #             'nombreDemandeDevis': 7,
        #             'nombreVente': 3,
        #         },
        #     ],
        # }
        # image_path = 'diagram.png'  # Replace with the path to your image
        # output_path = 'recap_semaine.pdf'
        # # report_generator.create_pdf('diagram.png', 'report.pdf')
        # report_generator.create_pdf(image_path, output_path, rapport)

        # # 5. Send the email with the report attached
        # email_sender = EmailSender()
        # email_sender.send_email("recipient@example.com", "Weekly Report", "Here is your report", 'report.pdf')
    except ValueError:
        return ({'error': f'Error when analysing data'}), 500


if __name__ == '__main__':
    analyser(datetime.strptime("2024-9-16 11:40", "%Y-%m-%d %H:%M"),
             datetime.strptime("2024-10-22 11:40", "%Y-%m-%d %H:%M"), "week")
