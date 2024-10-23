from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource

from app.utils.fetcher import Fetcher
from app.utils.utils import get_voyage_sale


class VoyageSale(Resource):
    def get(self):
        """
        Get sales data for a specific voyage_routes
         within a date range.

        This endpoint retrieves sales information for a specified voyage_routes ID and a date range defined by `start_date` and `end_date`.

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
            - name: period_type
              in: query
              type: string
              required: true
              description: The type of period for aggregating sales data
              example: "daily"
            - name: id_voyage
              in: query
              type: string
              required: true
              description: The unique identifier for the voyage_routes
              example: "V001"
        responses:
            200:
                description: A list of sales data for the specified voyage_routes
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                        description: The unique identifier for the sale
                                    voyage_id:
                                        type: string
                                        description: The ID of the voyage_routes
                                    sale_amount:
                                        type: number
                                        format: float
                                        description: The amount of the sale
                                    sale_date:
                                        type: string
                                        format: date-time
                                        description: The date of the sale
                        example:
                            - id: "S001"
                              voyage_id: "V001"
                              sale_amount: 250.0
                              sale_date: "2024-01-01T10:00:00"
                            - id: "S002"
                              voyage_id: "V001"
                              sale_amount: 150.0
                              sale_date: "2024-01-01T12:00:00"
            400:
                description: Invalid date format, end date less than or equal to start date, or missing parameters
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
                            missing_parameter:
                                summary: Missing required parameters
                                value: { "error": "Missing required parameters: start_date, end_date, period_type, id_voyage" }
        """
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

        result = get_voyage_sale(new_df, id_voyage, start_date, end_date, period_type)

        result_json = result.to_dict(orient='records')

        return jsonify(result_json)
