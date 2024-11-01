from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource

from app.utils.fetcher import Fetcher
from app.utils.utils import get_global_sale


class GlobalSale(Resource):
    def get(self):
        """
        Get global_routes sales data based on a date range and period type.

        This endpoint retrieves global_routes sales data between a given `start_date` and `end_date`, optionally categorized by `period_type`.

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
            - name: period_type
              in: query
              type: string
              required: false
              description: The type of period to categorize sales (e.g., 'daily', 'weekly', 'monthly')
              example: "daily"
        responses:
            200:
                description: A list of global_routes sales data between the given date range
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    period:
                                        type: string
                                        description: The period type (e.g., day, week, month)
                                    total_sales:
                                        type: number
                                        format: float
                                        description: The total sales for the period
                            example:
                                - period: "2024-01-01"
                                  total_sales: 10500.75
                                - period: "2024-01-02"
                                  total_sales: 9800.50
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
        period_type = request.args.get('period_type')

        fetcher = Fetcher.fetcher

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        if end_date <= start_date:
            return jsonify({'error': 'End date must be greater than start date'}), 400

        new_df = fetcher.fetch_cleaned_navigation_history(start_date, end_date)
        if new_df.empty:
            return jsonify([])
        else:
            result = get_global_sale(new_df, start_date, end_date, period_type)
            return result.to_dict(orient='records')
