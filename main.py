from opensearch_dsl import Search
from opensearchpy import OpenSearch

host = "localhost"
port = 9200
auth = ("neotel", "N3oS3nh@2021")  # For testing only. Don't store credentials in code.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

s = Search(using=client, index="ctm")

response = s.execute()
