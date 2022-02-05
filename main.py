import os
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
import requests
from bs4 import BeautifulSoup

from utils.contracts.contractsDatas import datas
from utils.calls import *
from utils.tokenomics import *
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

############################
### ERC20
############################
@bot.command(aliases=["n"])
async def name(ctx):
    n = Erc20("polar").name()
    embed = discord.Embed(title="Name: {}".format(n))
    await ctx.send(embed=embed)

@bot.command(aliases=["s"])
async def symbol(ctx):
    s = Erc20("polar").symbol()
    embed = discord.Embed(title="Symbol: {}".format(s))
    await ctx.send(embed=embed)

@bot.command(aliases=["p"])
async def price(ctx):
    p = getTokenPriceDollar(
        Pair("pair"), datas["polar"]["address"], getNativePriceDollar()
    )
    embed = discord.Embed(title="Price: ${:,}".format(round(p, 2)))
    await ctx.send(embed=embed)

@bot.command(aliases=["ts"])
async def totalSupply(ctx):
    ts = Erc20("polar").totalSupply()
    embed = discord.Embed(title="Total Supply: {:,} POLAR".format(ts))
    await ctx.send(embed=embed)

@bot.command(aliases=["mc"])
async def marketCap(ctx):
    p = getTokenPriceDollar(
        Pair("pair"), datas["polar"]["address"], getNativePriceDollar()
    )
    ts = Erc20("polar").totalSupply()
    embed = discord.Embed(title="Market Cap: ${:,}".format(int(p * ts)))
    await ctx.send(embed=embed)

@bot.command(aliases=["bo"])
async def balanceOf(ctx, addr):
    b = Erc20("polar").balanceOf(addr)
    embed = discord.Embed(title="Balance: {:,} POLAR".format(round(b, 2)))
    await ctx.send(embed=embed)

############################
### Node
############################
@bot.command(aliases=["np"])
async def nodePrice(ctx):
    p = Node("polar").getNodePrice()
    embed = discord.Embed(title="Node Price: {:,} POLAR".format(round(p, 2)))
    await ctx.send(embed=embed)

@bot.command(aliases=["ct"])
async def claimTime(ctx):
    sec = Node("polar").getClaimTime()
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    f = "{:d}h {:02d}m {:02d}s".format(h, m, s)
    embed = discord.Embed(title="Claim Time: {}".format(f))
    await ctx.send(embed=embed)

@bot.command(aliases=["ctr"])
async def claimTimeRewards(ctx):
    r = Node("polar").getRewardPerNode()
    embed = discord.Embed(title="Claim Time Rewards: {:,} POLAR".format(r))
    await ctx.send(embed=embed)

@bot.command(aliases=["dr"])
async def dailyRewards(ctx):
    t = Node("polar").getClaimTime()
    r = Node("polar").getRewardPerNode()
    dr = 24 * 60 * 60 / t * r
    embed = discord.Embed(title="Daily Rewards: {:,} POLAR".format(dr))
    await ctx.send(embed=embed)

@bot.command(aliases=["tcn"])
async def totalCreatedNodes(ctx):
    t = Node("polar").getTotalCreatedNodes()
    embed = discord.Embed(title="Total Created Nodes: {:,}".format(t))
    await ctx.send(embed=embed)

@bot.command(aliases=["nno"])
async def nodeNumberOf(ctx, addr):
    n = Node("polar").getNodeNumberOf(addr)
    embed = discord.Embed(title="Node Number: {:,}".format(n))
    await ctx.send(embed=embed)

############################
### Treasury
############################
@bot.command(aliases=["td"])
async def treasuryDAI(ctx):
    a = Node("polar").futurUsePool()
    b = Erc20("dai").balanceOf(a)
    embed = discord.Embed(title="Treasury DAI: {:,} DAI".format(round(b, 2)))
    await ctx.send(embed=embed)

@bot.command(aliases=["ta"])
async def treasuryAVAX(ctx):
    n = Node("polar")
    a = n.futurUsePool()
    b = n.w3.eth.getBalance(a) / (10**18)
    embed = discord.Embed(title="Treasury AVAX: {:,} AVAX".format(round(b, 2)))
    await ctx.send(embed=embed)

############################
### Holders
############################
def formatHolder(name, val):
    s = " "*5 + "{}: {}\n".format(name, val.strip())
    return s.replace(" ", " ឵឵")

@bot.command(aliases=["ho"])
async def holders(ctx):
    r = requests.get("https://snowtrace.io/token/generic-tokenholders2?a=0x6c1c0319d8ddcb0ffe1a68c5b3829fd361587db4&s=1000000000000000000000000")
    soup = BeautifulSoup(r.content, features="html.parser")
    embed = discord.Embed(title="Top holders")
    i = 0
    for tr in soup.find_all("tr")[1:11]:
        i += 1
        tr = list(tr)
        rank = tr[0].text
        value = formatHolder("address", tr[1].text)
        b = tr[2].text
        try:
            value += formatHolder("balance", b[:b.index(".") + 3] + " POLAR")
        except:
            value += formatHolder("balance", b + " POLAR")
        value += formatHolder("share", tr[3].text)
        embed.add_field(name="Top {}".format(rank), value=value, inline=False)
    await ctx.send(embed=embed)

############################
### Help
############################
def formatLine(cmd, ali, desc):
    s = " "*5 + "{} - {} - {}\n".format(cmd, ali, desc)
    return s.replace(" ", " ឵឵")


@bot.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title="Help Commands")
    
    name = "Help"
    value = formatLine("help", "h", "Display this help")
    embed.add_field(name=name, value=value, inline=False)
    
    name = "ERC20"
    value = formatLine("name", "n", "Display token name")
    value += formatLine("symbol", "s", "Display token symbol")
    value += formatLine("price", "p", "Display token price in dollars")
    value += formatLine("totalSupply", "ts", "Display token total supply")
    value += formatLine("marketCap", "mc", "Display token market cap")
    value += formatLine("balanceOf [addr]", "bo", "Display token balance of [addr]")
    embed.add_field(name=name, value=value, inline=False)

    name = "Node"
    value = formatLine("nodePrice", "np", "Display node price")
    value += formatLine("claimTime", "ct", "Display claim time")
    value += formatLine("claimTimeRewards", "ctr", "Display claim time rewards")
    value += formatLine("dailyRewards", "dr", "Display daily rewards")
    value += formatLine("totalCreatedNodes", "tcn", "Display total created nodes")
    value += formatLine("nodeNumberOf [addr]", "nno", "Display node number of [addr]")
    embed.add_field(name=name, value=value, inline=False)

    name = "Treasury"
    value = formatLine("treasuryDAI", "td", "Display treasury DAI balance")
    value += formatLine("treasuryAVAX", "ta", "Display treasury AVAX balance")
    embed.add_field(name=name, value=value, inline=False)

    name = "Holders"
    value = formatLine("holders", "ho", "Display top 10 holders")
    embed.add_field(name=name, value=value, inline=False)

    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))
