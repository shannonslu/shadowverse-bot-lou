import os

import discord
from discord.ext import commands

import card_data
import card_art


bot = commands.Bot(command_prefix=os.environ["BOT_PREFIX"])


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def invite(ctx):
    app_info = await bot.application_info()
    link = f"https://discord.com/api/oauth2/authorize?client_id={app_info.id}&permissions=18432&scope=bot"
    await ctx.send(f"Invite me to your server: <{link}>")


@bot.command()
async def card(ctx, *, query: str):
    async with ctx.typing():
        cards = await card_data.get()
    results = card_data.find(cards, query, num_results=1)
    if not results:
        await ctx.send(f'Found no cards matching "{query}"')
    else:
        [result] = results
        embed = discord.Embed.from_dict(card_data.create_embed(result))
        await ctx.send(embed=embed)


@bot.command()
async def cards(ctx, *, query: str):
    async with ctx.typing():
        cards = await card_data.get()
    results = card_data.find(cards, query, num_results=10)
    if not results:
        await ctx.send(f'Found no cards matching "{query}"')
    else:
        await ctx.send(
            "Found these cards:\n"
            + "\n".join("{card_id}: {card_name}".format(**card) for card in results)
        )


@bot.command()
async def art(ctx, *, query: str):
    async with ctx.typing():
        cards = await card_data.get()

    results = card_data.find(cards, query, num_results=1)
    if not results:
        await ctx.send(f'Found no cards matching "{query}"')
        return
    [result] = results
    card_name = result["card_name"]

    async with ctx.typing():
        image = await card_art.get_asset(result["card_id"])

    if image is None:
        await ctx.send(f'Failed to get card art for "{card_name}"')
    else:
        await ctx.send(card_name, file=discord.File(image, "0.png"))


bot.run(os.environ["DISCORD_TOKEN"])