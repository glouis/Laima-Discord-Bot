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
import draft as _draft
import help_formatter as _help
import logging
import model
import internationalization
import prefix as _prefix
import season as _season
import twitter_agent
import util

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix=_prefix.prefix,
    description=_("This bot is dedicated to the Krosmaga CCG."),
    command_not_found=_("No command called {} found."),
    command_has_no_subcommands=_("Command {0.name} has no subcommands."),
    formatter=_help.CustomHelpFormatter())

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

@bot.command(pass_context=True,
    help=_("Give information about Laima"))
async def about(context):
    internationalization.set_language(context.message.server.id)
    _about.laima.reset_title(_("Discord bot dedicated to the Krosmaga CCG"))
    _about.laima.reset_description(_("I aim to provide useful commands to the Krosmaga community!"))
    _about.laima.reset_embed()
    await bot.say(embed=_about.laima.embed)
    _about.fearei.reset_title(_("Author of the illustration"))
    _about.fearei.reset_description(_("Below is the complete illustration of Laima. You can visit the DeviantArt page of FeaRei by cliking on the title!"))
    _about.fearei.reset_embed()
    await bot.say(embed=_about.fearei.embed)

@bot.group(pass_context=True,
    invoke_without_command=True,
    description=_("Calculate the earnings of the draft mode"),
    help=_("Give the play number(s) where you lose. If you reached the level four, you will be ask to indicate the play(s) where you did an all-in."))
async def draft(context, *args):
    internationalization.set_language(context.message.server.id)
    if context.invoked_subcommand is None:
        msg = "```{victories}{level}{pack}{kamas}{chips}{earnings}".format(victories=_("Victories"), level=_("  Level"), pack=_("    Pack"), kamas=_("  Kamas"), chips=_("      Chips"), earnings=_("  Earnings"))
        try:
            victories, defeats, chips, level_four = _draft.calcResultsPartOne(args)
            plays = victories + defeats
            if plays < 10:
                msg = '\n'.join([msg, _draft.defineEarnings(victories, chips)])
                msg = '\n'.join([msg, "```"])
            else:
                allins = [0 for j in range(3)]
                await bot.say(_("Give the play number(s) where you did **all-in**"))
                allins_msg = await bot.wait_for_message(timeout=10, author=context.message.author, channel=context.message.channel)
                if allins_msg is not None:
                    args = allins_msg.content.lower().split(' ')
                    if args[0] in ["none", "aucune", "0"]:
                        pass
                    elif args[0] in ["all", "toutes"]:
                        allins = [1 for j in range(3)]
                    else:
                        ind_max = (int(plays) - 1) % 3
                        args = args[:3]
                        for arg in args:
                            ind = (int(arg) - 1) % 3
                            if ind <= ind_max:
                                allins[ind] = 1
                chips = _draft.calcResultsPartTwo(chips, level_four, allins)
                msg = '\n'.join([msg, _draft.defineEarnings(victories, chips)])
                msg = '\n'.join([msg, "```"])
        except Exception as e:
            msg = e.args[0]
            if msg.startswith("invalid literal for int() with base 10"):
                msg = _("The numbers must be integers")
        finally:
            await bot.say(msg)

@draft.command(pass_context=True,
    description=_("Display a table with the potential earnings"),
    help=_("Give the number(s) of victories for which you want an estimation of the earnings. Without parameters, display the complete table"))
async def table(context, *args : str):
    internationalization.set_language(context.message.server.id)
    msg = _draft.createTable(args)
    await bot.say(msg)

@bot.command(pass_context=True,
    description=_("Allow to change the language used on the server"),
    help=_("Indicate which language you want to use. Available: en, fr."))
async def lang(context, arg):
    internationalization.set_language(context.message.server.id)
    if context.message.author.server_permissions.administrator:
        if arg == "en":
            lang = internationalization.Language.ENGLISH
        elif arg == "fr":
            lang = internationalization.Language.FRENCH
        else:
            lang = None
            msg = _("Error, use either *en* or *fr* as parameter")
        if lang is not None:
            msg = internationalization.switch_language(context.message.server.id, lang)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@bot.command(pass_context=True,
    description=_("Change the prefix to call Laima on the server"),
    help=_("Give the new prefix you want to use. Limited to 3 characters."))
async def prefix(context, *args):
    internationalization.set_language(context.message.server.id)
    if context.message.author.server_permissions.administrator:
        if(len(args) != 1):
            msg = _("This command takes one unique parameter")
        else:
            prefix = args[0]
            server_id = context.message.server.id
            msg = _prefix.change_prefix(prefix, server_id)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@bot.command(pass_context=True,
    description=_("Give the rewards of the ranked mode"),
    help=_("Give the rank(s) for which you want the rewards. Accepted values are number from 6 to 30, top100, top20, 3rd, 2nd and 1st. If no rank are given, display the all table."))
async def season(context, *args : str):
    internationalization.set_language(context.message.server.id)
    msg = _season.createTable(args)
    await bot.say(msg)

@bot.group(pass_context=True,
    description=_("Allow to subscribe or unsubscribe to the twitter timeline of Krosmaga (fr)"),
    help=_("Use one of the subcommands"))
async def twitter(context):
    internationalization.set_language(context.message.server.id)
    if context.invoked_subcommand is None:
        await bot.say(_("No subcommand used. Run ```{prefix}help twitter``` for more help.").format(prefix=bot.command_prefix))

@twitter.command(pass_context=True,
    aliases=["on"],
    description=_("Subscribe the current channel"))
async def subscribe(context):
    internationalization.set_language(context.message.server.id)
    if context.message.author.server_permissions.administrator:
        msg = twitter_agent.subscribe(context.message.channel.id)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@twitter.command(pass_context=True,
    aliases=["off"],
    description=_("Unsubscribe the current channel"))
async def unsubscribe(context):
    internationalization.set_language(context.message.server.id)
    if context.message.author.server_permissions.administrator:
        msg = twitter_agent.unsubscribe(context.message.channel.id)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@twitter.command(pass_context=True,
    description=_("Indicate if the current channel is currently subscribed or not"))
async def status(context):
    internationalization.set_language(context.message.server.id)
    msg = twitter_agent.getStatus(context.message.channel.id)
    await bot.say(msg)

@twitter.command(pass_context=True,
    description=_("Display the last tweet of Krosmaga"))
async def last(context):
    internationalization.set_language(context.message.server.id)
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
