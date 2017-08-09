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
import config
from datetime import datetime
import discord
import model
import internationalization
import twitter

api = twitter.Api(consumer_key=config.twitter_consumer_key,
    consumer_secret=config.twitter_consumer_secret,
    access_token_key=config.twitter_access_token_key,
    access_token_secret=config.twitter_access_token_secret)

twitter_timeline = {}
twitter_timeline["screen_name"] = _("Krosmaga_EN")

# Get the id of the last tweet from krosmaga which is not a reply
# Return:
#   - id: str, the id of the tweet
def getLastTweetId(screen_name):
    statuses = api.GetUserTimeline(screen_name=screen_name)
    i = 0
    while(statuses[i].in_reply_to_user_id is not None):
        i += 1
    return statuses[i].id

# Read a tweet and create a discord embed object to present it
# Parameters:
#   - tweet_id: str, the id of the tweet
# Return:
#   - tweet: discord.Embed, the tweet
def getTweet(tweet_id):
    status = api.GetStatus(tweet_id)
    title = _("Tweet from Krosmaga")
    if status.quoted_status is not None:
        status = status.quoted_status
        title = _("Quoted by Krosmaga")
    elif status.retweeted_status is not None:
        status = status.retweeted_status
        title = _("Retweeted by Krosmaga")
    user = status.user
    description = status.text
    try:
        url = status.urls[0].url
    except:
        url = None
    timestamp = datetime.strptime(status.created_at, "%a %b %d %H:%M:%S %z %Y")
    colour = discord.Colour.blue()
    tweet = discord.Embed(title=title, description=description, url=url, colour=colour, timestamp=timestamp)
    display_user_name = "{user_name} (@{user_screen_name})".format(user_name=user.name, user_screen_name=user.screen_name)
    tweet.set_author(name=display_user_name, url=user.url, icon_url=user.profile_image_url)
    tweet.set_footer(text="Twitter",
        icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Twitter_bird_logo_2012.svg/16px-Twitter_bird_logo_2012.svg.png")
    try:
        image_url = status.media[0].media_url_https
        tweet.set_image(url=image_url)
    except:
        pass
    return tweet

# Add a discord channel to the subscriber list
# Parameters:
#   - channel_id: str, the id of the channel
# Return:
#   - msg: str, a message to say the result of the function
def subscribe(channel_id):
    msg = _("This channel is now subscribed to the twitter timeline of Krosmaga")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == channel_id)
        if channel.twitter is False:
            channel.twitter = True
            with model.laima_db.transaction():
                channel.save()
        else:
            msg = _("Error, this channel is already subscribed to the twitter timeline of Krosmaga")
    except model.Channel.DoesNotExist:
        with model.laima_db.transaction():
            model.Channel.create(id=channel_id, twitter=True)
    return msg

# Remove a discord channel to the subscriber list
# Parameters:
#   - channel_id: str, the id of the channel
# Return:
#   - msg: str, a message to say the result of the function
def unsubscribe(channel_id):
    msg = _("Error, this channel is already not subscribed to the twitter timeline of Krosmaga")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == channel_id)
        if channel.twitter is True:
            msg = _("This channel is now unsubscribed from the twitter timeline of Krosmaga")
            channel.twitter = False
            with model.laima_db.transaction():
                channel.save()
    except model.Channel.DoesNotExist:
        with model.laima_db.transaction():
            model.Channel.create(id=channel_id, twitter=False)
    return msg

# Indicate if a discord channel is in the subscriber list
# Parameters:
#   - channel_id: str, the id of the channel
# Return:
#   - msg: str, a message to say the status of the channel
def getStatus(channel_id):
    msg = _("This channel is not subscribed to the twitter timeline of Krosmaga")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == channel_id)
        if channel.twitter is True:
            msg = _("This channel is subscribed to the twitter timeline of Krosmaga")
    except model.Channel.DoesNotExist:
        pass
    return msg

async def twitterAgent(bot, lang):
    await bot.wait_until_ready()
    internationalization.languages[lang].install()
    last_tweet_id = getLastTweetId(_(twitter_timeline["screen_name"]))
    while not bot.is_closed:
        await asyncio.sleep(300)
        internationalization.languages[lang].install()
        new_tweet_id = getLastTweetId(_(twitter_timeline["screen_name"]))
        if new_tweet_id != last_tweet_id:
            tweet = getTweet(new_tweet_id)
            last_tweet_id = new_tweet_id
            with model.laima_db.transaction():
                for channel in model.Channel.select():
                    if(channel.twitter and channel.lang == lang.value):
                        dest = bot.get_channel(channel.id)
                        await bot.send_message(dest, embed=tweet)
