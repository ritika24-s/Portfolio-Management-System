def read_file():
    with open("trade_data.txt", "r") as fh:
        # <trade_id>,<trade_type>,<symbol>,<direction>,<quantity>,<price>
        columns = ["trade_id", "trade_type", "symbol", "direction", "quantity", "price"]
        trade_data = []
        
        # read the file line by line and append to the trade_data list
        for line in fh.readlines():
            trade_data.append(dict(zip(columns, line.strip().split(","))))

    return trade_data


if __name__ == "__main__":
    from Trading.trade_processor import TradeProcessor

    #  read the input file
    trade_data = read_file()
    
    # add the trades to the processor
    processor = TradeProcessor()
    processor.process_trades(trade_data)
    