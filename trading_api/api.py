from futu import OpenQuoteContext

class FutuQuoteContext():
    def __init__(self):
        self.ctx = self.initialize_quote_ctx()

    def __del__(self):
        self.terminate_quote_ctx()
        self.ctx = None
    
    def initialize_quote_ctx(self, host_ip = '127.0.0.1', port = 11111):
        quote_ctx = OpenQuoteContext(
            host = host_ip,
            port = port
        )
        print("[LOG] Futu OpenQuoteContext initialized with host_ip: %s, port: %s" % (host_ip, port))
        return quote_ctx
    
    def terminate_quote_ctx(self):
        print("[LOG] Futu OpenQuoteContext terminated")
        self.ctx.close()
