from discord import Embed
from discord.ext import commands
from index import update_index
from pages.page import Page
import requests
import sys
import os

# from bot_token import token

# Set up the package path for imports to work
sys.path.insert(1, os.getcwd())

bot = commands.Bot(command_prefix=">")
token = os.getenv("DISCORD_BOT_TOKEN")
page_base = "https://arcadaliam.fandom.com/wiki/"
wiki_home = "https://arcadaliam.fandom.com/wiki/ArcaDaliam_Wiki"
search_base = "https://arcadaliam.fandom.com/wiki/Special:Search?query={}&navigationSearch=true"

index = update_index()

def __scrape(url):
    entry = requests.get(url)
    page = Page(entry.text)
    return page


@bot.command()
async def character(ctx, *name):
    global index
    if len(name) > 1:
        name = " ".join(name)
    else:
        name = name[0]

    if name in index.indexed_pages:
        character_page = page_base + name.replace(" ", "_")
        page = __scrape(character_page)
        ret_str = str("""```bash\n\"{}\"```""").format(page.character_overview)
        embed = Embed(title=name)
        embed.add_field(name="Overview", value=ret_str)
        index = update_index()
        await ctx.send(embed=embed)
    else:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="Character not found :sob:", value="{} could not be found on the Wiki".format(name))
        await ctx.send(embed=embed)


@bot.command()
async def npc(ctx, *name):
    global index
    if len(name) > 1:
        name = " ".join(name)
    else:
        name = name[0]

    if name in index.indexed_pages:
        npc_page = page_base + name.replace(" ", "_")
        page = __scrape(npc_page)
        ret_str = str("""```bash\n\"{}\"```""").format(page.npc_overview)
        embed = Embed(title=name)
        embed.add_field(name="Overview", value=ret_str)
        index = update_index()
        await ctx.send(embed=embed)
    else:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="NPC not found :sob:", value="{} could not be found on the Wiki".format(name))
        await ctx.send(embed=embed)


@bot.command()
async def location(ctx, *name):
    global index
    if len(name) > 1:
        name = " ".join(name)
    else:
        name = name[0]

    if name in index.indexed_pages:
        location_page = page_base + name.replace(" ", "_")
        page = __scrape(location_page)
        ret_str = str("""```bash\n\"{}\"```""").format(page.location_overview)
        embed = Embed(title=name)
        embed.add_field(name="Overview", value=ret_str)
        index = update_index()
        await ctx.send(embed=embed)
    else:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="Location not found :sob:", value="{} could not be found on the Wiki".format(name))
        await ctx.send(embed=embed)


# @bot.command()
# async def dump(ctx, *args):
#     global index
#     print("Sections\n", "-"*25, "\n", index.indexed_pages)
#     ret_str = str("""```bash\n\"{}\"```""").format("Page Index dumped to console.")
#     embed = Embed(title="Page Index")
#     embed.add_field(name="Status", value=ret_str)
#     await ctx.send(embed=embed)


@bot.command()
async def update(ctx, *args):
    try:
        global index
        index = update_index()
        ret_str = str("""```bash\n\"{}\"```""").format("Page Index update completed.")
        embed = Embed(title="Page Index")
        embed.add_field(name="Status", value=ret_str)
        await ctx.send(embed=embed)
    except:
        ret_str = str("""```bash\n\"{}\"```""").format("Page Index update FAILED.")
        embed = Embed(title="Page Index")
        embed.add_field(name="Status", value=ret_str)
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
