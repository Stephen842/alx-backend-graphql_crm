from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
LOW_STOCK_LOG = "/tmp/low_stock_updates_log.txt"

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message)

    # Check GraphQL endpoint
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=1,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("query { hello }")
        client.execute(query)
    except Exception:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} Warning: GraphQL endpoint unreachable\n")


def update_low_stock():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                message
                updatedProducts {
                    name
                    stock
                }
            }
        }
        """
    )

    try:
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]

        with open(LOW_STOCK_LOG, "a") as f:
            for prod in updated_products:
                f.write(f"{timestamp} - Product: {prod['name']}, Stock: {prod['stock']}\n")
            f.write(f"{timestamp} - {result['updateLowStockProducts']['message']}\n")
    except Exception as e:
        with open(LOW_STOCK_LOG, "a") as f:
            f.write(f"{timestamp} - Error: {str(e)}\n")