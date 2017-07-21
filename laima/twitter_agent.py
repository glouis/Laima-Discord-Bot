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

import config
from datetime import datetime
import discord
import model
import twitter

api = twitter.Api(consumer_key=config.twitter_consumer_key,
    consumer_secret=config.twitter_consumer_secret,
    access_token_key=config.twitter_access_token_key,
    access_token_secret=config.twitter_access_token_secret)

# Get the id of the last tweet from krosmaga which is not a reply
# Return:
#   - id: str, the id of the tweet
def getLastTweetId():
    statuses = api.GetUserTimeline(screen_name="krosmaga")
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
    title = "Tweet de Krosmaga"
    if status.quoted_status is not None:
        status = status.quoted_status
        title = "Cité par Krosmaga"
    elif status.retweeted_status is not None:
        status = status.retweeted_status
        title = "Retweeté par Krosmaga"
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
    tweet.set_thumbnail(url="http://abs.twimg.com/favicons/favicon.ico")
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
    msg = "Ce salon est maintenant abonné au fil twitter de Krosmaga."
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == channel_id)
        if channel.twitter is False:
            channel.twitter = True
            with model.laima_db.transaction():
                channel.save()
        else:
            msg = "Erreur, ce salon est déjà abonné au fil twitter de Krosmaga."
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
    msg = "Ce salon n'est maintenant plus abonné au fil twitter de Krosmaga."
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == channel_id)
        if channel.twitter is True:
            channel.twitter = False
            with model.laima_db.transaction():
                channel.save()
        else:
            msg = "Erreur, ce salon n'est déjà pas abonné au fil twitter de Krosmaga."
    except model.Channel.DoesNotExist:
        msg = "Erreur, ce salon n'est déjà pas abonné au fil twitter de Krosmaga."
        with model.laima_db.transaction():
            model.Channel.create(id=channel_id, twitter=False)
    return msg

# Indicate if a discord channel is in the subscriber list
# Parameters:
#   - channel_id: str, the id of the channel
# Return:
#   - msg: str, a message to say the status of the channel
def getStatus(channel_id):
    msg = "Ce salon n'est pas abonné au fil twitter de Krosmaga."
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == channel_id)
        if channel.twitter is True:
            msg = "Ce salon est abonné au fil twitter de Krosmaga."
    except model.Channel.DoesNotExist:
        pass
    return msg
