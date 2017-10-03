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

import asyncio
from datetime import datetime
import discord
import feedparser
import html
import model
import internationalization
import re
from time import mktime

krosfeed = {}
krosfeed["name"] = _("Krosmaga (en)")
krosfeed["url"] = _("http://www.krosmaga.com/en")
krosfeed["icon"] = "https://s.ankama.com/www/static.ankama.com/ankama/cms/images/291/2016/10/11/587298.jpg"
krosfeed["source"] = _("https://www.krosmaga.com/en/rss/news.xml")

first_ligne_regex = re.compile(r".*?(?=\n)")
tag_regex = re.compile(r"(<.*?>)")
img_src_url_regex = re.compile(r"(?<=src=\").*?(?=\")")
first_img_regex = re.compile(r"<img.*?/>")

# Get the feed
# Parameters:
#   - url: str, the url of the feed to read
# Return:
#   - the parsed feed
def get_feed(url):
    return feedparser.parse(url)

# Get the id of the newest entry of the feed
# Parameters:
#   - feed: dict, the feed containing the entries
# Return:
#   - the id of the newest entry
def get_last_entry_id(feed):
    return feed.entries[0].id

# Get a "raw" entry and create a discord embed from it
# Parameters:
#   - entry: dict, the entry to parse
# Return:
#   - embed: discord embed, presents the data
def convert_to_embed(entry):
    first_ligne = first_ligne_regex.search(entry.summary).group(0)
    fl_without_tags = tag_regex.subn('', first_ligne)[0]
    description = html.unescape(fl_without_tags)
    colour = discord.Colour.magenta()
    timestamp = datetime.fromtimestamp(mktime(entry.published_parsed))
    embed = discord.Embed(title=entry.title, description=description, url=entry.link, colour=colour, timestamp=timestamp)
    image = first_img_regex.search(entry.summary)
    if image:
        image_url = img_src_url_regex.search(image.group(0)).group(0)
        embed.set_image(url=image_url)
    embed.set_author(name=_(krosfeed["name"]), url=_(krosfeed["url"]), icon_url=krosfeed["icon"])
    return embed

# Get the new entries that have not yet been parsed
# Parameters:
#   - feed: dict, the feed containing the entries
#   - entry_id: str, the id of the last entry that have been parsed
# Return:
#   - last_entries: list, discord embeds presenting the data of each not parsed entry
def get_last_entries(feed, entry_id):
    last_entries = []
    for entry in feed.entries:
        if entry.id != entry_id:
            embed = convert_to_embed(entry)
            last_entries.append(embed)
        else:
            break
    return last_entries

# Add a discord channel to the subscriber list
# Parameters:
#   - message: discord message, the message which called this function
# Return:
#   - msg: str, a message to say the result of the function
def subscribe(message):
    msg = _("This channel is now subscribed to the rss feed of Krosmaga")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == message.channel.id)
        if channel.rss is False:
            channel.rss = True
            with model.laima_db.transaction():
                channel.save()
        else:
            msg = _("Error, this channel is already subscribed to the rss feed of Krosmaga")
    except model.Channel.DoesNotExist:
        with model.laima_db.transaction():
            server = model.Server.get_or_create(id=message.server.id)[0]
            model.Channel.create(id=message.channel.id, rss=True, server=server)
    return msg

# Remove a discord channel to the subscriber list
# Parameters:
#   - message: discord message, the message which called this function
# Return:
#   - msg: str, a message to say the result of the function
def unsubscribe(message):
    msg = _("Error, this channel is already not subscribed to the rss feed of Krosmaga")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == message.channel.id)
        if channel.rss is True:
            msg = _("This channel is now unsubscribed from the rss feed of Krosmaga")
            channel.rss = False
            with model.laima_db.transaction():
                channel.save()
    except model.Channel.DoesNotExist:
        with model.laima_db.transaction():
            server = model.Server.get_or_create(id=message.server.id)[0]
            model.Channel.create(id=message.channel.id, rss=False, server=server)
    return msg

# Indicate if a discord channel is in the subscriber list
# Parameters:
#   - message: discord message, the message which called this function
# Return:
#   - msg: str, a message to say the status of the channel
def getStatus(message):
    msg = _("This channel is not subscribed to the rss feed of Krosmaga")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == message.channel.id)
        if channel.rss is True:
            msg = _("This channel is subscribed to the rss feed of Krosmaga")
    except model.Channel.DoesNotExist:
        pass
    return msg

# Agent to steadily check if one feed has new entries
# Parameters:
#   - bot: discord bot, the Laima bot
#   - lang: Language, the language of the feed to check
# Return
#   - send embed in subscribed channels corresponding to the feed language
async def rss_agent(bot, lang):
    await bot.wait_until_ready()
    internationalization.languages[lang].install()
    while not bot.is_closed:
        feed = get_feed(_(krosfeed["source"]))
        if feed.entries == []:
            await asyncio.sleep(1800)
        else:
            last_entry_id = get_last_entry_id(feed)
            break
    while not bot.is_closed:
        await asyncio.sleep(1800)
        internationalization.languages[lang].install()
        feed = get_feed(_(krosfeed["source"]))
        if feed.entries == []:
            continue
        new_entry_id = get_last_entry_id(feed)
        if new_entry_id != last_entry_id:
            last_entries = get_last_entries(feed, last_entry_id)
            last_entry_id = new_entry_id
            with model.laima_db.transaction():
                for channel in model.Channel.select():
                    if channel.rss:
                        if channel.lang is None:
                            if channel.server.lang == lang.value:
                                dest = bot.get_channel(channel.id)
                                for entry in last_entries:
                                    await bot.send_message(dest, embed=entry)
                        else:
                            if channel.lang == lang.value:
                                dest = bot.get_channel(channel.id)
                                for entry in last_entries:
                                    await bot.send_message(dest, embed=entry)
