## Answers to TRM Labs Take Home Test

This repo can be used to test queries. 

1. PLEASE SEE BOTTOM OF PAGE FOR WRITEUP
2. ADD BIG QUERY JSON SECRET CREDS HERE :  "bigquery/config/trm_util_config.py"
    * ADD CREDENTIALS ON LINE 23

A few things to note:
- SQL Queries and solutions can be found under bigquery/SQL
- The three queries include the original, top_n_addresses answer, and direct_exposure answer.
- You can run the flask app by using the instructions on the README from home folder and examples below.
- The results are presented as json format, the schemas for the results can be found under the reporting.sql file.

## Test Queries

**1. Results via API for the initial query provided.**
Can send the following request to get the solution.

```
curl --request GET \
  --url http://127.0.0.1:5000/test_api/data
```

Example Response Should Look Like This

```json
{
  "data": [
    {
      "address": "1FGhgLbMzrUV5mgwX9nkEeqHbKbUK29nbQ",
      "inflows": "0",
      "outflows": "0.01733177",
      "total_flows": "0.01733177"
    },
    {
      "address": "1Huro4zmi1kD1Ln4krTgJiXMYrAkEd4YSh",
      "inflows": "0.01733177",
      "outflows": "0",
      "total_flows": "0.01733177"
    }
  ],
  "success": true
}
```

The first query that was provided in the solution can be retrieved with the following curl command through the API

```bash
curl --request GET \
  --url http://127.0.0.1:5000/transfers
```
 Resulting in the following data

```json
{
  "data": [
    {
      "block_hash": "0000000000000000000b0b092ba2bc0706c96b664a5df1c95fd5827d089e7da7",
      "block_timestamp": 1610305395000,
      "chain": "btc",
      "receiver": "3J3kL8ctE1dHPhL17UjcNXjj66gBPdLZUH",
      "sender": "3QYmEZmsFZLRcFLFGwewYM6iaG24xb8gj5",
      "value": 0.02118432
    },
    {
      "block_hash": "0000000000000000000b0b092ba2bc0706c96b664a5df1c95fd5827d089e7da7",
      "block_timestamp": 1610305395000,
      "chain": "btc",
      "receiver": "3QYmEZmsFZLRcFLFGwewYM6iaG24xb8gj5",
      "sender": "3QYmEZmsFZLRcFLFGwewYM6iaG24xb8gj5",
      "value": 0.02118432
    },
    {
      "block_hash": "00000000000000000006dc47a66bc6228100b3f1b6524be982ba274e397c122e",
      "block_timestamp": 1610303698000,
      "chain": "btc",
      "receiver": "bc1qua34f8xrrajtp8fp50l459d4cf5l69aakyylqr",
      "sender": "bc1qeyam8xpfzudyapkktjjwhef0zc282agrcwkvfv",
      "value": 0.00287387
    }, ...
  ],
  "success": true
}
```


## Answers to Problems


**Part 1. Calculate the Direct Exposure between addresses.**
Can send the following request to get the solution.

Curl Request With Parameters
 - address: in format "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd"
 - limit: in format - integer
```buildoutcfg
curl --request GET \
  --url 'http://127.0.0.1:5000/address/exposure/direct?address=bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt&limit=5'
```

Example Response
```json
{
  "data": [
    {
      "block_timestamp": 1609743456000,
      "receiver": "3EdQE1sRccND6aganPejMc8jkkYhD6BnZo",
      "sender": "bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt",
      "total_value": 103.09187091
    },
    {
      "block_timestamp": 1609743456000,
      "receiver": "bc1q4kxrq46qd5uwlhtg3hwy226w5vq979qld05cx9",
      "sender": "bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt",
      "total_value": 103.09187091
    },
    {
      "block_timestamp": 1609743456000,
      "receiver": "1DTUxYbYehZ5jx1nU9ZehhUfpTRHnPwz8f",
      "sender": "bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt",
      "total_value": 103.09187091
    },
    {
      "block_timestamp": 1609743456000,
      "receiver": "bc1q946ev8rrtwhx2syjag3azu3hg8kwvgx8cp2a7m",
      "sender": "bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt",
      "total_value": 103.09187091
    },
    {
      "block_timestamp": 1609743456000,
      "receiver": "1NWLpAAu6LersfyWa3ka3KvXdBE4Nn3zCJ",
      "sender": "bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt",
      "total_value": 103.09187091
    }
  ],
  "success": true
}

```


**Part 2: Calculate the Top N addresses with flows.**
Can send the following request to get the solution.


Curl Request With Parameters 
 - address: in format "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd"
 - top_n: integer
 - flow_type: 'outflow','inflow','both', 'any', 'all'
 - start_date: "%Y-%m-%d", e.g. '2021-01-01'
 - end_date: "%Y-%m-%d", e.g.'2021-01-25'


```buildoutcfg
curl --request GET \
  --url 'http://127.0.0.1:5000/address/top_n_address_flows?address=bc1qk0fqd2ysrlmq9u2qjvcghmuhpr6300eusa84dt&top_n=10&start_date=2021-01-01&end_date=2021-01-25&flow_type=all'
```

Example Response
```json
{
  "data": [
    {
      "counterparty_address": "1HAzhv4TxDaoeS4VjuxJXzYUhuWo1NprGy",
      "flow_type": "outflow",
      "inflow": 0.0,
      "outflow": 103.09187091,
      "total_flow": 103.09187091
    },
    {
      "counterparty_address": "3ELd8DVZ6ikLpa3B92QpMLi8nGqiRKQNxP",
      "flow_type": "outflow",
      "inflow": 0.0,
      "outflow": 103.09187091,
      "total_flow": 103.09187091
    },
    {
      "counterparty_address": "3AxsvND1SPyAS8CrBVr383g3pt6e6eSPyb",
      "flow_type": "outflow",
      "inflow": 0.0,
      "outflow": 103.09187091,
      "total_flow": 103.09187091
    },
    {
      "counterparty_address": "3DG8MPLWASkj1HduLT6K4Lm8g8d6XUu6Kt",
      "flow_type": "outflow",
      "inflow": 0.0,
      "outflow": 103.09187091,
      "total_flow": 103.09187091
    },
    {
      "counterparty_address": "bc1qmydaeyv6neftr7fsa55ecvq85qe47p0fewq4uz",
      "flow_type": "outflow",
      "inflow": 0.0,
      "outflow": 103.09187091,
      "total_flow": 103.09187091
    },
    {
      "counterparty_address": "1CtP2A6CioFhYU4zW6jqa2dnBKEoFvrAWn",
      "flow_type": "outflow",
      "inflow": 0.0,
      "outflow": 103.09187091,
      "total_flow": 103.09187091
    }
  ],
  "success": true
}
```

**Part 3: Design the API which has examples above, additional questions discussed below.**

- What data *store* would you use to store the data? 
   * I used BigQuery here because that's where the original data lived and it enabled me to build the sample without copying data.
     The final datastore choice would depend on a few things.  
     If <= 1 sec responses is good enough --  you could keep it in BigQuery with a few changes to the schema. (see performance section below for the changes)
    If performance is good enough, this offers several advantages:
        1. leaving it in BigQuery removes overhead of additional datastore configuration, scaling, and administration.  
        2. A batch job can easily pull new records from the public dataset into the target copy
        3. BigQuery bills for i/o, so reducing reads also optimizes costs.
    This setup would likely get you responses in under a second but not millisecond response time, since BQ's not really made for this use case.  If that isn't fast enough, the best datastore choice would depend on how you expect it to be accessed.  For example:
        - If you expect filtering largely on the senders/receivers with large date ranges, 
          you could use something like elasticsearch with indexes on the addresses. Or you could use a key/value store (ie google cloud datastore.
        - If you expect narrow date range queries, a traditional RDBMS (postgres/mysql) 
          with partitions by date and indexes on sender/receiver would perform fine.
        - If you expect to broaden the api to track all relationships between senders/receivers, you could use a graph database.
        Any of these other options would require a separate load job or export job to get new records from 
          the BigQuery source, and most would require care and feeding.   
    * PLEASE SEE "<project_root>/bigquery/clients/bigquery_client.py"
    * The data response is in json format. 
    * I used a pandas data frame for simple manipulation upstream of the API, and for any ML that could be added mid stream. 
    * I provided other add ons to the client for storing data as a CSV, listing tables in database, generally querying to local file, 
      getting schemas from bigquery, listing a single column as a result.
    * (The preferred delimiter on files would be a pipe. i.e. "|" )
    * I also have more functions from previous jobs for storing to GCS, querying using spark, ect.
- What data *schema* would you use?
    * PLEASE SEE "<project_root>/bigquery/reporting_sql.py" for schemas
    * If we wanted to store a schema outside of big query I provided a file for doing so, 
      this could be used for things like spark or conerting to other databases.  
    * You can retrieve big query schemas from big query if you would like by using the client add ons as well.
- How would you *load* the data?
    * You could do a Cloud Function that would do incremental loads into your BQ table when new data arrived in the source BQ table.  
      Or export new records to cloud storage for load into your alternative datastore if you use something else.
    * Or you could set a pub/sub event on new row arrival.
    * You can load the data in a similiar way to retrieving the data with the bigquery client, I have personal functions for that
    but you would have to hire me to get those :)
- How would you *update* the data?
    * You can update the data by UPDATE and INSERT (upserting not specifically supported) to big query along with 
      bigquery loads functions described in the last section. 
    * I also have functions for these on my local but did not include them here.
- How would it *scale* to larger data sizes? (ie., multi-terabyte)
    * For larger scale processing you could use Spark to either parrallize processing with dataproc.
    * I have funcitons for this too. 
    * Dataproc specifications can be set using airflow and set to scale dynamically.
- Other considerations?
    * UNIT TESTING - I did a limited amount of unit testing for various functions. 
        - Those functions can be found in this file "<project_root>/bigquery/test/test_client.py"
        - NOTE: other potential examples here for loading and other testing. "<project_root>/bigquery/test/test_other_examples.py"
    * SPEED REQUIREMENTS - 
      With a few changes to the schema, you could keep it in BigQuery.  You could get sub-second responses from BigQuery by creating a copy of the table that does the following:
            1. Unnest the input/output addresses so that the table has just the transaction data you need (timestamp, timestamp month, input & output addresses, and value)
            2. Maintain the date partitioning and add cluster-by columns of input and output address.  This will enable faster searching by address and date.
        - Please Note: In big query UI response time is sub 1 second! 
        - Combined with API I am getting 1-3 seconds with middle layer, any latency due to big query limitation, networking, additional code. 
        - Other ways to improve response time. 
            1. Add predicate pushdowns higher up query stack in query to improve filtering.
            2. Build a materialized table or view so queries dont have to be run each time.
            3. Limit the tables overall size based on time so reduce searching. 
            3. Use Timeit to check if any python code is slow, optimize things like try, accept statements which can be slow.
            4. Add a caching layer with python cache or redis for distributed cache on kubernetes.
            5. For multiple requests at once can use pythons multiprocessing, now in 3.8 new improvements for multithreading around the GIL.
            6. Try a different database: possibly elastic search, relational db, or anything else.
            7. Possible use cpython, not sure if this would help
               
- Data Accuracy?  
    * I wrote both queries two ways, using the UI the data lined up for the most part before I added variable substituion.
    * You could also go through and test for specific usernames and double spot check the data.
    * Note : I did notice I saw a bunch of people paying themselves which was a little weird, not sure if this is acceptable.
    * I assumed total flow meant adding in + out flow.
    * Added the option to filter by outflow, versus inflow, both, or all/any

- Other Notes - Configuration Files: 
    * Configuration files can be found at "<root>/bigquery/config/trm_config.py" and "<root>/bigquery/config/trm_util_config.py"
    * Sorry, I hardcoded the location of the JSON secret file. 
    * Also have an oauth test in the "<root>/bigquery/test/test_oauth_creds.py". 
    * I will send the secret to you as well so you can run this all yourself if you would like. 
    * I added  - from mock import patch - to show how to mock data for unit tests.
      
**Thanks for reviewing!!!  :)**
        
````
             ,-. 
    ,     ,-.   ,-. 
   / \   (   )-(   ) 
   \ |  ,.>-(   )-< 
    \|,' (   )-(   ) 
     Y ___`-'   `-' 
     |/__/   `-' 
     | 
     | 
     |    -RR- 
  ___|_____________ 