from opensearch_dsl import Search
from opensearchpy import OpenSearch
import time
import os
from dotenv import load_dotenv
 
load_dotenv()
 
start_time = time.time()
 
host = os.getenv("OPENSEARCH_IP")
port = 9200
auth = (os.getenv("OPENSEARCH_USER"), os.getenv("OPENSEARCH_PASSWORD"))  # For testing only. Don't store credentials in code.
 
# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)
 
s = (
    Search(using=client, index="ctm")
    .source(["user", "pol_action", "guardpoint", "pol_permission", "policy"])
    .filter("range", timestamp={"gte": "now-30d/d", "lte": "now"})
)
 
response = s.scan()
 
log_counts = {}
error_counts = 0
total_logs = 0
 
for hit in response:
    total_logs += 1
    log = hit.to_dict()
    try:
        key = (log["user"], log["pol_action"], log["guardpoint"], log["pol_permission"], log["policy"])
 
        if key in log_counts:
            log_counts[key] += 1
        else:
            log_counts[key] = 1
    except:
        continue


with open("logs.txt", "w", encoding="utf-8") as f:
    for (user, pol_action, guardpoint, pol_permission, policy), count in log_counts.items():
        f.write(f"{user}, {pol_action}, {guardpoint}, {pol_permission}, {policy}, Count: {count}\n")

end_time = time.time() - start_time
print(f"Finished in {end_time} seconds")
print(f"Total logs: {total_logs}")
print(f"Total unique logs: {len(log_counts)}")
