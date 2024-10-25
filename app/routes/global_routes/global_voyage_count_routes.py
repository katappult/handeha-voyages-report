from datetime import datetime

import pandas as pd
from flask import jsonify, request
from flask_restful import Resource

from app.utils.fetcher import Fetcher
from app.utils.utils import get_voyage_count


class GlobalVoyageCount(Resource):
    def get(self):
        """
        Get voyage_routes counts based on a date range.

        This endpoint retrieves the count of voyages within a specified `start_date` and `end_date`.

        ---
        parameters:
            - name: start_date
              in: query
              type: string
              required: true
              description: The start date in the format YYYY-MM-DD HH:MM:SS
              example: "2024-01-01 00:00:00"
            - name: end_date
              in: query
              type: string
              required: true
              description: The end date in the format YYYY-MM-DD HH:MM:SS
              example: "2024-01-02 23:59:59"
        responses:
            200:
                description: A list of voyage_routes counts between the specified date range
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    voyage_id:
                                        type: string
                                        description: The unique identifier for the voyage_routes
                                    count:
                                        type: integer
                                        description: The number of times this voyage_routes was recorded
                        example:
                            - voyage_id: "V001"
                              count: 10
                            - voyage_id: "V002"
                              count: 5
            400:
                description: Invalid date format or end date is less than or equal to start date
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                error:
                                    type: string
                                    description: The error message
                        examples:
                            invalid_date_format:
                                summary: Invalid date format
                                value: { "error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS" }
                            end_date_error:
                                summary: End date less than or equal to start date
                                value: { "error": "End date must be greater than start date" }
        """
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        fetcher = Fetcher.fetcher

        # Convert strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM'}), 400

        # Ensure end_date is greater than start_date
        if end_date <= start_date:
            return jsonify({'error': 'End date must be greater than start date'}), 400

        # Fetch table and process data
        new_df = fetcher.fetch_cleaned_navigation_history(start_date, end_date)

        result = get_voyage_count(new_df)

        if new_df.empty:
            return jsonify([])

        else:
            result_json = result.apply(lambda x: x.map(lambda y: str(y) if isinstance(y, pd.Period) else y)).to_dict(
                orient='records')

            return jsonify(result_json)
