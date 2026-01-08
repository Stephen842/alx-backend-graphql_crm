from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

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
