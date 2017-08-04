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
#   - server_id: str, the id of the current server
def set_language(server_id):
    try:
        with model.laima_db.transaction():
            server = model.Server.get(model.Server.id == server_id)
        lang = server.lang
    except model.Server.DoesNotExist:
        lang = Language.ENGLISH.value
    finally:
        languages[Language(lang)].install()

# Allow to change the language used on a server
# Parameters:
#   - server_id: str, the id of the server
#   - lang: Language, the language to set
# Return:
#   - msg: str, message returned by the bot
def switch_language(server_id, lang):
    msg = _("The language on this server was successfully changed!")
    try:
        with model.laima_db.transaction():
            server = model.Server.get(model.Server.id == server_id)
        if server.lang != lang.value:
            server.lang = lang.value
            with model.laima_db.transaction():
                server.save()
        else:
            msg = _("Error, This language was already set")
    except model.Server.DoesNotExist:
        with model.laima_db.transaction():
            model.Server.create(id=server_id, lang=lang.value)
    return msg
