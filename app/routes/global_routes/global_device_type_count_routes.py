from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource

from app.utils.fetcher import Fetcher
from app.utils.utils import get_device_type_count


class GlobalDeviceTypeCount(Resource):
    def get(self):
        """
        Get device type data based on a date range.

        This endpoint retrieves device type data between a given `start_date` and `end_date`.

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
                description: A list of device types between the given date range
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    device_type:
                                        type: string
                                        description: The type of the device
                                    count:
                                        type: integer
                                        description: The number of occurrences
                        example:
                            - device_type: "mobile"
                              count: 120
                            - device_type: "desktop"
                              count: 80
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

        if new_df.empty:
            return jsonify([])
        else:
            result = get_device_type_count(new_df)

            # Convert result to JSON format
            result_json = result.to_dict(orient='records')

            return jsonify(result_json)
