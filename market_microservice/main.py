from flask import Flask, request
from jsonschema import validate, ValidationError
from flask_restx import Api, Resource
import requests
# import os

app = Flask(__name__)

api = Api(app)

# JSON schema for validating market query parameter
market_schema = {
    "type": "object",
    "properties": {"market": {"type": "string"}},
    "required": ["market"],
}


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = {"error": "Bad Request", "message": error.message}
    return response, 400


@api.route("/markets/summaries")
class MarketSummariesResource(Resource):
    @api.doc(responses={200: "Market summaries retrieved successfully"})
    def get(self):
        """
        Get all market summaries
        """
        # api_key = os.environ.get("api_key")
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {api_key}",
        }

        # Make request to Bittrex API
        response = requests.get(
            "https://api.bittrex.com/v3/markets/summaries", headers=headers
        )
        if response.status_code != 200:
            return {"error": "Failed to fetch market summaries"}, response.status_code

        return response.json()


@api.route("/markets")
class MarketSummaryResource(Resource):
    @api.doc(
        params={"market": "Market symbol"},
        responses={200: "Market summary retrieved successfully"},
    )
    def get(self):
        """
        Get market summary by market symbol
        """
        # Validate the market query parameter
        try:
            validate(request.args.to_dict(), market_schema)
        except ValidationError as error:
            return {"error": error.message}, 400

        # Get the market query parameter value
        market = request.args.get("market")

        # api_key = os.environ.get("api_key")
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {api_key}",
        }

        # Make request to Bittrex API for market summary
        url = f"https://api.bittrex.com/v3/markets/{market}/summary"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch market summary"}, response.status_code

        return response.json()


if __name__ == "__main__":
    app.run()
