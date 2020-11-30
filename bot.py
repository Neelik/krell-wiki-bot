from discord import Embed, Colour, Member
from discord.ext import commands
from index import update_index
from pages.page import Page
from titlecase import titlecase
import random
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


@bot.command(aliases=["history", "turnpage", "reveal"])
async def check(ctx, *name):
    global index
    if len(name) > 1:
        name = " ".join(name)
    else:
        name = name[0]

    # Set the name up for index checking
    for_check = name.lower()
    name_cased = titlecase(for_check)
    uri_encoded = name_cased.replace(" ", "_")

    if for_check in index.indexed_pages:
        page_uri = page_base + uri_encoded
        page = __scrape(page_uri)

        formatted_overview = " ".join(page.character_overview.split())
        ret_str = f"\n[Full Page]({page_uri})\n\n{formatted_overview}"
        embed = Embed(title="Arca Daliam Wiki", color=Colour.dark_teal())
        embed.add_field(name=name_cased, value=ret_str)
        index = update_index()

        await ctx.send(embed=embed)

    else:
        embed = Embed(title="Oops! Missing Info")
        embed.add_field(name="Character not found :sob:", value="{} could not be found on the Wiki".format(name_cased))
        await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def roll(ctx, dice):
    """

    :param dice: String of what dice to roll and how many, plus modifier of the form: "1d4+2"
    :return: String representing each individual dice and their sum
    """
    modifier = 0

    # Parse the dice
    no_spaces = "".join(dice.split())

    # check for modifier
    if "+" in no_spaces:
        modifier = no_spaces.split("+")[-1]
        no_mod = no_spaces[:-2]
    else:
        no_mod = no_spaces

    splits = no_mod.split("d")
    num_dice = int(splits[0])
    die = int(splits[1])

    rolls = []
    for roll in range(num_dice):
        rolls.append(random.randint(1, die))

    results = " + ".join(rolls)
    results = f"{results} + {modifier} = {sum(rolls) + modifier}"
    embed = Embed(title=f"Rolling {dice}")
    embed.add_field(name="You rolled:", value=results)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def roles(ctx, member: Member):
    member_roles = member.roles
    await ctx.send(member_roles[1:])


@bot.command()
@commands.is_owner()
async def dump(ctx, *args):
    global index
    ret_str = str("""```bash\n\"{}\"```""").format("Page Index dumped to console.")
    embed = Embed(title="Page Index")
    embed.add_field(name="Status", value=ret_str)
    await ctx.send(embed=embed)


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
