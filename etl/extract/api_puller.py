import json
from typing import Any

from etl.common.logger import get_logger

logger = get_logger("APIPuller")


class SimulatedAPIPuller:
    """Simulates REST API ingestion for CloudMart order transaction streams."""

    def __init__(self, api_endpoint: str = "https://api.cloudmart-internal.com/v1/orders"):
        self.api_endpoint = api_endpoint

    def fetch_recent_orders(self, limit: int = 100) -> list[dict[str, Any]]:
        """Simulates REST API GET request returning a JSON list of transaction records."""
        logger.info(f"Triggering GET request to {self.api_endpoint}?limit={limit}")
        # Simulated payload structure returned by REST API
        mock_api_payload = [
            {
                "order_id": f"ORD_API_{1000 + i}",
                "customer_id": f"CUST_{(i % 10) + 1:04d}",
                "product_id": f"PROD_{(i % 5) + 1:04d}",
                "order_timestamp": "2026-09-24T14:30:00Z",
                "quantity": (i % 3) + 1,
                "unit_price": round(29.99 + (i * 5.5), 2),
                "discount_amount": 0.0,
                "payment_method": "Credit Card" if i % 2 == 0 else "PayPal",
                "region_id": f"REG_0{(i % 4) + 1}"
            }
            for i in range(limit)
        ]
        logger.info(f"Successfully pulled {len(mock_api_payload)} transaction records from REST API.")
        return mock_api_payload

    def serialize_to_json_str(self, records: list[dict[str, Any]]) -> str:
        """Serializes list of dict records to JSON string formatted for S3 raw drop."""
        return json.dumps(records, indent=2)
