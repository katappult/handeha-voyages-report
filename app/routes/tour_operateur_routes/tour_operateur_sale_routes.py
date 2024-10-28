from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource

from app.utils.fetcher import Fetcher
from app.utils.utils import get_tour_operateur_sale


class TourOperateurSale(Resource):
    def get(self):
        # Get start_date and end_date from request arguments
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        period_type = request.args.get('period_type')
        id_voyage = request.args.get('id_voyage')

        fetcher = Fetcher.fetcher

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM'}), 400

        if end_date <= start_date:
            return jsonify({'error': 'End date must be greater than start date'}), 400

        # Fetch table and process data
        new_df = fetcher.fetch_cleaned_navigation_history(start_date, end_date)

        if new_df.empty:
            return jsonify([])
        else:
            result = get_tour_operateur_sale(new_df, id_voyage, start_date, end_date, period_type)
            result_json = result.to_dict(orient='records')
            return jsonify(result_json)
