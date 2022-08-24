from futu import *

def sub(ctx, ticker_list, type_list):
    # new subscription to given tickers
    sub_ret, sub_err = ctx.subscribe(ticker_list, type_list)
    # subscription validation
    if sub_ret == RET_OK:
        for ticker in ticker_list:
            print("[OK] subscribed to {0}".format(ticker))
        print("[LOG] current subscription status: ", ctx.query_subscription())
    else:
        print("[ERROR] ", sub_err)

def unsub(ctx, ticker_list, type_list):
    # unsubscribe to given tickers
    unsub_ret, unsub_err = ctx.unsubscribe(ticker_list, type_list)
    # subscription validation
    if unsub_ret == RET_OK:
        for ticker in ticker_list:
            print("[OK] unsubscribed to {0}".format(ticker))
        print("[LOG] current subscription status: ", ctx.query_subscription())
    else:
        print("[ERROR] ", unsub_err)

def unsub_all(ctx):
    # unsubscribe to all tickers
    ctx.unsubscribe_all()
    # subscription validation
    unsub_all_ret, unsub_all_err = ctx.unsubscribe_all()
    if unsub_all_ret == RET_OK:
        print("[OK] Closed ALL subscriptions")
        print("[LOG] current subscription status: ", ctx.query_subscription())
    else:
        print("[ERROR] ", unsub_all_err)

def sim_quote(quote_ctx, ticker) -> dict:
    """returns a simplified quote for a single given ticker"""
    ret, data = quote_ctx.ctx.get_market_snapshot(ticker)
    quote = {}

    if ret == RET_OK:
        data = data.iloc[0]
        quote["ticker"] = data.loc["code"]
        quote["time"] = data.loc["update_time"]
        quote["price"] = data.loc["last_price"]
        return quote
    else:
        print("[ERROR] ", data)
        return None

def quote_df(quote_ctx, ticker_list):
    """returns a pandas.DataFrame as quote for a given ticker list"""
    ret, data = quote_ctx.ctx.get_market_snapshot(ticker_list)
    
    if ret == RET_OK:
        data = data.iloc[:,:8]
        data.to_markdown(tablefmt="grid")
        print(data)
        return data
    else:
        print("[ERROR] ", data)
        return None