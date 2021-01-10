agg_query_columns = {
    'base_query': [['chain', 'STRING'],
                    ['block_timestamp', 'TIMESTAMP'],
                    ['block_hash', 'STRING'],
                    ['sender', 'STRING'],
                    ['receiver', 'STRING'],
                    ['value', 'STRING']],

    'direct_exposure': [['sender', 'STRING'],
                                               ['receiver', 'STRING'],
                                               ['total_value', 'FLOAT64']],
    'top_n_addresses': [['counterparty_address', 'STRING'],
                                           ['inflow', 'FLOAT64'],
                                           ['outflow', 'FLOAT64'],
                                           ['total_flow', 'FLOAT64']]
}