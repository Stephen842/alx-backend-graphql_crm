from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    query = gql("""
    query {
        customers {
            id
        }
        orders {
            id
            total_amount
        }
    }
    """)

    result = client.execute(query)

    total_customers = len(result["customers"])
    total_orders = len(result["orders"])
    total_revenue = sum(
        float(order["total_amount"]) for order in result["orders"]
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log:
        log.write(
            f"{timestamp} - Report: "
            f"{total_customers} customers, "
            f"{total_orders} orders, "
            f"{total_revenue} revenue\n"
        )
