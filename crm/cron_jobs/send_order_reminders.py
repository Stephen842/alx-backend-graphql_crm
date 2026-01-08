#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

# Set up the GraphQL client
transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Calculate the cutoff date (7 days ago)
seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

# GraphQL query — no invalid filters
query = gql(
    """
    query GetOrders {
        orders {
            id
            orderDate
            customer {
                email
            }
        }
    }
    """
)

result = client.execute(query)

# Filter in Python and log
with open(LOG_FILE, "a") as log_file:
    for order in result.get("orders", []):
        order_date = datetime.fromisoformat(order["orderDate"].replace("Z", "+00:00"))

        if order_date >= seven_days_ago:
            log_file.write(
                f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - "
                f"Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
            )

print("Order reminders processed!")
