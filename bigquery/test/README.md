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


** Part 1. Calculate the Direct Exposure between addresses.**
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


** Part 2: Calculate the Top N addresses with flows.**
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