from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource

from app.utils.fetcher import Fetcher
from app.utils.utils import get_country_count


class GlobalNavigationCount(Resource):
    def get(self):
        """
        Get navigation data based on a date range.

        This endpoint retrieves navigation data between a specified `start_date` and `end_date`.

        ---
        parameters:
            - name: start_date
              in: query
              type: string
              required: true
              description: The start date in the format YYYY-MM-DD
              example: "2024-01-01 00:00:00"
            - name: end_date
              in: query
              type: string
              required: true
              description: The end date in the format YYYY-MM-DD
              example: "2024-01-02 23:59:59"
        responses:
            200:
                description: A list of navigation data by country between the specified date range
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    country:
                                        type: string
                                        description: The country associated with the navigation data
                                    count:
                                        type: integer
                                        description: The number of navigations for that country
                        example:
                            - country: "USA"
                              count: 300
                            - country: "Canada"
                              count: 150
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
                                value: { "error": "Invalid date format. Use YYYY-MM-DD" }
                            end_date_error:
                                summary: End date less than or equal to start date
                                value: { "error": "End date must be greater than start date" }
        """
        # Get start_date and end_date from request arguments
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        fetcher = Fetcher.fetcher

        # Convert strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Ensure end_date is greater than start_date
        if end_date <= start_date:
            return jsonify({'error': 'End date must be greater than start date'}), 400

        new_df = fetcher.fetch_cleaned_search_history(start_date, end_date)

        if new_df.empty:
            return jsonify([])

        else:
            result = get_country_count(new_df)

            # Convert result to JSON format
            result_json = result.to_dict(orient='records')

            return jsonify(result_json)
