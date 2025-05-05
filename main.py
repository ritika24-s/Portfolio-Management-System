if __name__ == "__main__":
    from read_data import read_file
    from Trading.trade_processor import TradeProcessor

    #  read the input file
    trade_data = read_file()
    
    # add the trades to the processor
    processor = TradeProcessor()
    processor.process_trades(trade_data)
    