from google_auth_oauthlib import flow

# TODO: Uncomment the line below to set the `launch_browser` variable.
# launch_browser = True
#
# The `launch_browser` boolean variable indicates if a local server is used
# as the callback URL in the auth flow. A value of `True` is recommended,
# but a local server does not work if accessing the application remotely,
# such as over SSH or from a remote Jupyter notebook.

appflow = flow.InstalledAppFlow.from_client_secrets_file(
    "/Users/ryanriopelle/Desktop/trm_labs_interview/client_sercrets.json", scopes=["https://www.googleapis.com/auth/bigquery"]
)
launch_browser = False
if launch_browser:
    appflow.run_local_server()
else:
    appflow.run_console()

credentials = appflow.credentials
print("credentials", credentials)

from google.cloud import bigquery

# TODO: Uncomment the line below to set the `project` variable.
# project = 'user-project-id'
#
# The `project` variable defines the project to be billed for query
# processing. The user must have the bigquery.jobs.create permission on
# this project to run a query. See:
# https://cloud.google.com/bigquery/docs/access-control#permissions

client = bigquery.Client(project="trm-takehome-ryan-r", credentials=credentials)

query_string = """SELECT * FROM `trm-takehome-ryan-r.trm_sample_data.bitcoin_transfers_sample` LIMIT 20
"""
query_job = client.query(query_string)

# Print the results.
for row in query_job.result():  # Wait for the job to complete.
    print(row)