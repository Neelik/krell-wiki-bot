from discord import Embed
from discord.ext import commands
from pages import character_lookup, location_lookup, npc_lookup
from pages.page import Page
from bot_token import token
import requests
import sys
import os

# Set up the package path for imports to work
sys.path.insert(1, os.getcwd())

bot = commands.Bot(command_prefix=">")
page_base = "https://arcadaliam.fandom.com/wiki/"
wiki_home = "https://arcadaliam.fandom.com/wiki/ArcaDaliam_Wiki"
search_base = "https://arcadaliam.fandom.com/wiki/Special:Search?query={}&navigationSearch=true"

def __scrape(url):
    entry = requests.get(url)
    page = Page(entry.text)
    return page


@bot.command()
async def character(ctx, name):
    try:
        character_page = page_base + character_lookup[name.lower()]
        page = __scrape(character_page)
        full_name = " ".join(character_lookup[name.lower()].split("_"))
        ret_str = str("""```bash\n\"{}\"```""").format(page.character_overview)
        embed = Embed(title=full_name)
        embed.add_field(name="Overview", value=ret_str)
        await ctx.send(embed=embed)
    except KeyError:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="Character not found :sob:", value="{} could not be found on the Wiki".format(name))
        await ctx.send(embed=embed)


@bot.command()
async def npc(ctx, name):
    try:
        npc_page = page_base + npc_lookup[name.lower()]
        page = __scrape(npc_page)
        full_name = " ".join(npc_lookup[name.lower()].split("_"))
        ret_str = str("""```bash\n\"{}\"```""").format(page.npc_overview)
        embed = Embed(title=full_name)
        embed.add_field(name="Overview", value=ret_str)
        await ctx.send(embed=embed)
    except KeyError:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="NPC not found :sob:", value="{} could not be found on the Wiki".format(name))
        await ctx.send(embed=embed)


@bot.command()
async def location(ctx, name):
    try:
        location_page = page_base + location_lookup[name.lower()]
        page = __scrape(location_page)
        full_name = " ".join(location_lookup[name.lower()].split("_"))
        ret_str = str("""```bash\n\"{}\"```""").format(page.location_overview)
        embed = Embed(title=full_name)
        embed.add_field(name="Overview", value=ret_str)
        await ctx.send(embed=embed)
    except KeyError:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="Location not found :sob:", value="{} could not be found on the Wiki".format(name))
        await ctx.send(embed=embed)


# Error handling for the commands
@bot.event
async def on_command_error(error, ctx):
    if error.command_failed:
        embed = Embed(title="Command {} failed".format(str(error.command).upper()))
        embed.add_field(name="Sorry about that", value="Are you sure you typed the command correctly? If you are unsure, "
                                                       "try entering >help for further information.")
        await error.send(embed=embed)
    

if __name__ == "__main__":
    # Runs the bot :)
    bot.run(token)
