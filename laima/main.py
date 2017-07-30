"""
This file is part of Laima Discord Bot.

Copyright 2017 glouis

Laima Discord Bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Laima Discord Bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Laima Discord Bot. If not, see <http://www.gnu.org/licenses/>.
"""

import about as _about
import asyncio
import config
import discord
from discord.ext import commands
import draft as draft_lib
import logging
import model
import season as _season
import twitter_agent
import util

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = "This bot is dedicated to the Krosmaga CCG."
bot = commands.Bot(command_prefix='&',
    description=description,
    command_not_found="No command called {} found.",
    command_has_no_subcommands="Command {0.name} has no subcommands.",
    formatter=util.CustomHelpFormatter())

async def twitterAgent():
    await bot.wait_until_ready()
    last_tweet_id = twitter_agent.getLastTweetId()
    while not bot.is_closed:
        await asyncio.sleep(300)
        new_tweet_id = twitter_agent.getLastTweetId()
        if new_tweet_id != last_tweet_id:
            tweet = twitter_agent.getTweet(new_tweet_id)
            last_tweet_id = new_tweet_id
            with model.laima_db.transaction():
                for channel in model.Channel.select():
                    if(channel.twitter):
                        dest = bot.get_channel(channel.id)
                        await bot.send_message(dest, embed=tweet)

@bot.command(description="Give information about Laima")
async def about():
    await bot.say(embed=_about.laima.embed)
    await bot.say(embed=_about.fearei.embed)

@bot.group(pass_context=True,
    invoke_without_command=True,
    description="Calculate the earnings of the draft mode",
    help="Give the play number(s) where you lose. If you reached the level four, you will be ask to indicate the play(s) where you did an all-in.")
async def draft(context, *args):
    if context.invoked_subcommand is None:
        msg = "```Victories\tLevel\t\tPack\tKamas\t\tChips\tEarnings"
        try:
            victories, defeats, chips, level_four = draft_lib.calcResultsPartOne(args)
            plays = victories + defeats
            if plays < 10:
                msg = '\n'.join([msg, draft_lib.defineEarnings(victories, chips)])
                msg = '\n'.join([msg, "```"])
            else:
                allins = [0 for j in range(3)]
                await bot.say("Give the play number(s) where you did **all-in**")
                allins_msg = await bot.wait_for_message(timeout=10, author=context.message.author, channel=context.message.channel)
                if allins_msg is not None:
                    args = allins_msg.content.lower().split(' ')
                    if args[0] in ["none", "0"]:
                        pass
                    elif args[0] in ["all"]:
                        allins = [1 for j in range(3)]
                    else:
                        ind_max = (int(plays) - 1) % 3
                        args = args[:3]
                        for arg in args:
                            ind = (int(arg) - 1) % 3
                            if ind <= ind_max:
                                allins[ind] = 1
                chips = draft_lib.calcResultsPartTwo(chips, level_four, allins)
                msg = '\n'.join([msg, draft_lib.defineEarnings(victories, chips)])
                msg = '\n'.join([msg, "```"])
        except Exception as e:
            msg = e.args[0]
            if msg.startswith("invalid literal for int() with base 10"):
                msg = "The number must be an integer"
        finally:
            await bot.say(msg)

@draft.command(description="Display a table with the potential earnings",
    help="""Give the number(s) of victories for which you want an estimation of the earnings. Without parameters, display the complete table""")
async def table(*args : str):
    msg = "```Victories\tLevel\t\tPack\tKamas\t\tChips\tEarnings"
    if len(args) == 0:
        for i in range(13):
            msg = '\n'.join([msg, draft_lib.getEarnings(i)])
    else:
        for arg in args:
            msg = '\n'.join([msg, draft_lib.getEarnings(arg)])
    msg = '\n'.join([msg, "```"])
    await bot.say(msg)

@bot.command(description="Give the rewards of the ranked mode",
    help="Give the rank(s) for which you want the rewards. Accepted values are number from 6 to 30, top100, top20, 3rd, 2nd and 1st. If no rank are given, display the all table.")
async def season(*args : str):
    msg = _season.createTable(args)
    await bot.say(msg)

@bot.group(pass_context=True,
    description="Allow to subscribe or unsubscribe to the twitter timeline of Krosmaga (fr)",
    help="Use one of the subcommands")
async def twitter(context):
    if context.invoked_subcommand is None:
        await bot.say("No subcommand used. Run ```{prefix}help twitter``` for more help.".format(prefix=bot.command_prefix))

@twitter.command(pass_context=True,
    aliases=["on"],
    description="Subscribe the current channel")
async def subscribe(context):
    msg = twitter_agent.subscribe(context.message.channel.id)
    await bot.say(msg)

@twitter.command(pass_context=True,
    aliases=["off"],
    description="Unsubscribe the current channel")
async def unsubscribe(context):
    msg = twitter_agent.unsubscribe(context.message.channel.id)
    await bot.say(msg)

@twitter.command(pass_context=True,
    description="Indicate if the current channel is currently subscribed or not")
async def status(context):
    msg = twitter_agent.getStatus(context.message.channel.id)
    await bot.say(msg)

@twitter.command(pass_context=True,
    description="Display the last tweet of Krosmaga")
async def last(context):
    tweet_id = twitter_agent.getLastTweetId()
    tweet = twitter_agent.getTweet(tweet_id)
    channel = bot.get_channel(context.message.channel.id)
    await bot.send_message(channel, embed=tweet)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.loop.create_task(twitterAgent())
bot.run(config.discord_token)
