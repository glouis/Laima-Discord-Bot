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
import card as _card
import config
import discord
from discord.ext import commands
import draft as _draft
import help_formatter as _help
import logging
import internationalization
import prefix as _prefix
import rss_agent
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

@bot.command(pass_context=True,
    help=_("Give information about Laima"))
async def about(context):
    internationalization.set_language(context.message)
    _about.laima.reset_title(_("Discord bot dedicated to the Krosmaga CCG"))
    _about.laima.reset_description(_("I aim to provide useful commands to the Krosmaga community!"))
    _about.laima.reset_embed()
    await bot.say(embed=_about.laima.embed)
    _about.fearei.reset_title(_("Author of the illustration"))
    _about.fearei.reset_description(_("Below is the complete illustration of Laima. You can visit the DeviantArt page of FeaRei by cliking on the title!"))
    _about.fearei.reset_embed()
    await bot.say(embed=_about.fearei.embed)

@bot.command(pass_context=True,
    description=_("Display a card"),
    help=_("Give keywords in order to find the card you want to see."))
async def card(context, *args):
    lang = internationalization.get_language(context.message)
    internationalization.languages[internationalization.Language(lang)].install()
    if len(args) == 0:
        await bot.say(_("You must provide at least a keyword!"))
    else:
        cards, count = _card.search(args, lang)
        if count == 0:
            await bot.say(_("Sorry, no card found."))
        elif count == 1:
            embed = _card.to_embed(cards[0])
            await bot.say(embed=embed)
        elif count > 9:
            await bot.say(_("Sorry, too many card found."))
        else:
            msg = _("Choose the card you want to see:")
            i = 1
            for card in cards:
                name = card.name
                inf_lvl = card.card_data.infinite_level
                if inf_lvl is not None:
                    name = ' '.join([name, ":star2:" * inf_lvl])
                msg = '\n'.join([msg, str(i) + " > " + name])
                i += 1
            await bot.say(msg)
            answer = await bot.wait_for_message(timeout=10, author=context.message.author, channel=context.message.channel)
            if answer is not None:
                try:
                    ind = int(answer.content) - 1
                    embed = _card.to_embed(cards[ind])
                    await bot.say(embed=embed)
                except:
                    await bot.say(_("Sorry, your answer do not correspond to a choice."))
            else:
                await bot.say(_("Sorry, you were too long to answer."))

@bot.group(pass_context=True,
    invoke_without_command=True,
    description=_("Calculate the earnings of the draft mode"),
    help=_("Give the play number(s) where you lose. If you reached the level four, you will be ask to indicate the play(s) where you did an all-in."))
async def draft(context, *args):
    internationalization.set_language(context.message)
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
    internationalization.set_language(context.message)
    msg = _draft.createTable(args)
    await bot.say(msg)

@bot.command(pass_context=True,
    description=_("Allow to change the language used on the server or in a channel"),
    help=_("Takes two paramaters. First is to precise where you want to change the language (channel or server). Second is to indicate which language you want to use (available: en, fr, es) ; use 0 for a channel to make it use the language of the server."))
async def lang(context, scope, language):
    internationalization.languages[internationalization.Language.ENGLISH].install()
    if context.message.author.server_permissions.administrator:
        if language == "en":
            lang = internationalization.Language.ENGLISH
        elif language == "fr":
            lang = internationalization.Language.FRENCH
        elif language == "es":
            lang = internationalization.Language.SPANISH
        elif language == "0":
            lang = None
        else:
            msg = _("Error, the language was not recognised")
        if scope == "channel":
            msg = internationalization.switch_language_channel(context.message, lang)
        elif scope == "server":
            if lang is None:
                msg = _("Error, 0 cannot be used for a server")
            else:
                msg = internationalization.switch_language_server(context.message, lang)
        else:
            msg = _("Error, the scope was not recognised")
    else:
        msg = _("Only administrators of the server can use this command")
    internationalization.set_language(context.message)
    await bot.say(_(msg))

@bot.command(pass_context=True,
    description=_("Change the prefix to call Laima on the server"),
    help=_("Give the new prefix you want to use. Limited to 3 characters."))
async def prefix(context, *args):
    internationalization.set_language(context.message)
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

@bot.group(pass_context=True,
    description=_("Allow to subscribe or unsubscribe to the rss feed of Krosmaga"),
    help=_("Use one of the subcommands"))
async def rss(context):
    internationalization.set_language(context.message)
    if context.invoked_subcommand is None:
        await bot.say(_("No subcommand used. Run ```{prefix}help rss``` for more help.").format(prefix=_prefix.prefix(bot, context.message)))

@rss.command(pass_context=True,
    aliases=["on"],
    help=_("Subscribe the current channel"))
async def subscribe(context):
    internationalization.set_language(context.message)
    if context.message.author.server_permissions.administrator:
        msg = rss_agent.subscribe(context.message)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@rss.command(pass_context=True,
    aliases=["off"],
    help=_("Unsubscribe the current channel"))
async def unsubscribe(context):
    internationalization.set_language(context.message)
    if context.message.author.server_permissions.administrator:
        msg = rss_agent.unsubscribe(context.message)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@rss.command(pass_context=True,
    help=_("Indicate if the current channel is currently subscribed or not"))
async def status(context):
    internationalization.set_language(context.message)
    msg = rss_agent.getStatus(context.message)
    await bot.say(msg)

@bot.command(pass_context=True,
    description=_("Give the rewards of the ranked mode"),
    help=_("Give the rank(s) for which you want the rewards. Accepted values are number from 6 to 30, top100, top20, 3rd, 2nd and 1st. If no rank are given, display the all table."))
async def season(context, *args : str):
    internationalization.set_language(context.message)
    msg = _season.createTable(args)
    await bot.say(msg)

@bot.group(pass_context=True,
    description=_("Allow to subscribe or unsubscribe to the twitter timeline of Krosmaga (fr)"),
    help=_("Use one of the subcommands"))
async def twitter(context):
    internationalization.set_language(context.message)
    if context.invoked_subcommand is None:
        await bot.say(_("No subcommand used. Run ```{prefix}help twitter``` for more help.").format(prefix=_prefix.prefix(bot, context.message)))

@twitter.command(pass_context=True,
    aliases=["on"],
    help=_("Subscribe the current channel"))
async def subscribe(context):
    internationalization.set_language(context.message)
    if context.message.author.server_permissions.administrator:
        msg = twitter_agent.subscribe(context.message)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@twitter.command(pass_context=True,
    aliases=["off"],
    help=_("Unsubscribe the current channel"))
async def unsubscribe(context):
    internationalization.set_language(context.message)
    if context.message.author.server_permissions.administrator:
        msg = twitter_agent.unsubscribe(context.message)
    else:
        msg = _("Only administrators of the server can use this command")
    await bot.say(msg)

@twitter.command(pass_context=True,
    help=_("Indicate if the current channel is currently subscribed or not"))
async def status(context):
    internationalization.set_language(context.message)
    msg = twitter_agent.getStatus(context.message)
    await bot.say(msg)

@twitter.command(pass_context=True,
    help=_("Display the last tweet of Krosmaga"))
async def last(context):
    internationalization.set_language(context.message)
    tweet_id = twitter_agent.getLastTweetId(_(twitter_agent.twitter_timeline["screen_name"]))
    tweet = twitter_agent.getTweet(tweet_id)
    channel = bot.get_channel(context.message.channel.id)
    await bot.send_message(channel, embed=tweet)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    invite = discord.Game(name="https://discord.gg/VsrbrYC", url=None, type=0)
    await bot.change_presence(game=invite)

for lang in internationalization.Language:
    bot.loop.create_task(twitter_agent.twitterAgent(bot, lang))
    bot.loop.create_task(rss_agent.rss_agent(bot, lang))

bot.run(config.discord_token)
