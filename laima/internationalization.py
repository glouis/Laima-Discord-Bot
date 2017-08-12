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

import enum
import gettext
import model

gettext.install('laima', 'laima/i18n')

class Language(enum.Enum):
    ENGLISH = 1
    FRENCH = 2

languages = {}
languages[Language.ENGLISH] = gettext.translation('laima', localedir='laima/i18n', languages=['en'])
languages[Language.FRENCH] = gettext.translation('laima', localedir='laima/i18n', languages=['fr'])

# Set the language to use when a command is called
# Parameters:
#   - message: discord message, the message which called a command
def set_language(message):
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == message.channel.id)
        if channel.lang is None:
            try:
                lang = channel.server.lang
            except model.Server.DoesNotExist:
                lang = Language.ENGLISH.value
        else:
            lang = channel.lang
    except model.Channel.DoesNotExist:
        try:
            with model.laima_db.transaction():
                server = model.Server.get(model.Server.id == message.server.id)
            lang = server.lang
        except model.Server.DoesNotExist:
            lang = Language.ENGLISH.value
    finally:
        languages[Language(lang)].install()

# Allow to change the language used on a server
# Parameters:
#   - message: discord message, the message which called this function
#   - lang: Language, the language to set
# Return:
#   - msg: str, message returned by the bot
def switch_language_server(message, lang):
    msg = _("The language on this server was successfully changed!")
    try:
        with model.laima_db.transaction():
            server = model.Server.get(model.Server.id == message.server.id)
        if server.lang != lang.value:
            server.lang = lang.value
            with model.laima_db.transaction():
                server.save()
        else:
            msg = _("Error, this language was already set on this server")
    except model.Server.DoesNotExist:
        with model.laima_db.transaction():
            model.Server.create(id=message.server.id, lang=lang.value)
    return msg

# Allow to change the language used on a channel
# Parameters:
#   - message: discord message, the message which called this function
#   - lang: Language, the language to set
# Return:
#   - msg: str, message returned by the bot
def switch_language_channel(message, lang):
    msg = _("The language on this channel was successfully changed!")
    try:
        with model.laima_db.transaction():
            channel = model.Channel.get(model.Channel.id == message.channel.id)
        if lang is None and channel.lang is not None:
            channel.lang = lang
            with model.laima_db.transaction():
                channel.save()
        elif lang is not None and channel.lang != lang.value:
            channel.lang = lang.value
            with model.laima_db.transaction():
                channel.save()
        else:
            msg = _("Error, this language was already set on this channel")
    except model.Channel.DoesNotExist:
        with model.laima_db.transaction():
            server = model.Server.get_or_create(id=message.server.id)
            model.Channel.create(id=message.channel.id, lang=lang.value, server=server)
    finally:
        return msg
