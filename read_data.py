def get_columns():
    # <user_id>,<trade_id>,<trade_type>,<symbol>,<direction>,<quantity>,<price>
    return ["user_id", "trade_id", "trade_type", "symbol", "direction", "quantity", "price"]

def read_file():
    with open("trade_data.txt", "r") as fh:
        
        columns = get_columns()
        trade_data = []
        
        # read the file line by line and append to the trade_data list
        for line in fh.readlines():
            trade_data.append(dict(zip(columns, line.strip().split(","))))

    return trade_data
