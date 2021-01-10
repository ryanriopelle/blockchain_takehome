## Answers to TRM Labs Take Home Test

This repo can be used to test queries. 

A few things to note:
- SQL Queries and solutions can be found under bigquery/SQL
- The three queries include the original, top_n_addresses answer, and direct_exposure answer.
- You can run the flask app by using the instructions on the README from home folder.
- The results are pesented as json format, the schemas for the results can be found under the reporting.sql file.

## Test Queries

**1. Results via API for the initial query provided.**
Can send the following request to get the solution.

```
curl --request GET \
  --url http://127.0.0.1:5000/transfers_data
```

Example Response Should Look Like This

```[
  {
    "chain": "btc",
    "block_timestamp": 1609994001000,
    "block_hash": "0000000000000000000d8cca419b3414e2e326aedbc9e0a06925a9c68f4d312f",
    "sender": "1G47mSr3oANXMafVrR8UC4pzV7FEAzo3r9",
    "receiver": "196pNZG2GUXzrr4iA2WQBAiPe77HrAoPEX",
    "value": 0.01393073
  },
  {
    "chain": "btc",
    "block_timestamp": 1609994001000,
    "block_hash": "0000000000000000000d8cca419b3414e2e326aedbc9e0a06925a9c68f4d312f",
    "sender": "1G47mSr3oANXMafVrR8UC4pzV7FEAzo3r9",
    "receiver": "1G47mSr3oANXMafVrR8UC4pzV7FEAzo3r9",
    "value": 0.01393073
  }, ...
]
```


**2. Part 1: Calculate the Direct Exposure between addresses.**
Can send the following request to get the solution.



