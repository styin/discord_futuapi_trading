import discord
from discord.ext import commands

import os
import traceback
from datetime import date, datetime

from dotenv import load_dotenv
load_dotenv()

from trading_api.api import *
from trading_api.quotes.futu_quotes import *

class Query(commands.Cog):
    def __init__(self, bot, debug=False):
        self.bot = bot
        self.debug = debug or bool(os.getenv('DEBUG'))
        self._last_member = None
        self.api_quote_ctx = FutuQuoteContext()
        if self.debug:
            print("[LOG] Debugger Messages are ENABLED for query_cog")
    
    @commands.command(
        aliases=['qq','quick']
    )
    async def quickquote(self, ctx, ticker=None):
        """This command queries for a quick quote for a given ticker"""
        # ticker type validity check
        if not isinstance(ticker, str) or ticker.isdigit():
            await ctx.reply("**Error** | I can't recognize this ticker... :warning:\n"+\
                            "```\n{0}trade <ticker>\n```".format(os.getenv('PREFIX')))
            return
        # query for quote
        try:
            # futu api
            quote = sim_quote(self.api_quote_ctx, ticker)
            # craft embed
            embed_descript =\
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"\
                +"\nYou are making a trade for [{0}](https://finance.yahoo.com/quote/{0}). ".format(quote["ticker"])\
                +"Please note that the quote provided may fluctuate and shall be used for reference only."\
                +"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            embed = discord.Embed(
                title       = "{0}".format(quote["ticker"]),
                description = embed_descript,
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
            embed.add_field(
                name        = "Price",
                value       = "```${0}```".format(quote["price"]),
                inline      = True
            )
            embed.add_field(
                name        = "Time",
                value       = "```{0}```".format(quote["time"]),
                inline      = True
            )
            # attempt to set company logo as embed thumbnail
            # by retrieving the logo from clearbit.com using the display_name or the ticker
            embed.set_thumbnail(
                url = "https://logo.clearbit.com/{0}.com".format(quote["ticker"])
            )
        except Exception as e:
            print("[WARNING] quick_quote command failed")
            print("[WARNING]", traceback.format_exc())
            await ctx.reply("**Error** | The command could not be processed! :warning:\n"+\
                            "```\nUnknown Exception: [{0}]\n```".format(e))
        else:
            await ctx.channel.send(embed=embed)
    
    @commands.command(
        aliases=['q','full']
    )
    async def quote(self, ctx, *, arg):
        """This command queries for a full quote for a given ticker_list"""
        # split single argument into list of tickers
        ticker_list = arg.split(",")
        print(ticker_list)
        # ticker type validity check
        for ticker in ticker_list:
            if not isinstance(ticker, str) or ticker.isdigit():
                await ctx.reply("**Error** | I can't recognize this ticker:`[{0}]` :warning:\n".format(ticker)+\
                                "```\n{0}trade <ticker>\n```".format(os.getenv('PREFIX')))
                return
        
        # query for quote
        try:
            # futu api
            quote = quote_df(self.api_quote_ctx, ticker_list)
            # craft embed
            embed = discord.Embed(
                title       = "Here is your queried result.",
                description = "Queried tickers: {0}\n\u200b\n:warning:\
                    *quotes are provided by Futu OpenAPI, \
                    and shall be used for reference only.*".format(ticker_list),
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
        except Exception as e:
            print("[WARNING] quick_quote command failed")
            print("[WARNING]", traceback.format_exc())
            await ctx.reply("**Error** | The command could not be processed! :warning:\n"+\
                            "```\nUnknown Exception: [{0}]\n```".format(e))
        else:
            await ctx.channel.send(embed=embed)
            await ctx.channel.send("```{0}```".format(quote))

async def setup(bot):
    await bot.add_cog(Query(bot, debug=False))

print("[COG] Loaded query features")