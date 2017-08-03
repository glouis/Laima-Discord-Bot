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

import model
import util

# Change the bot command prefix of a server
# Parameters:
#   - prefix: str, the new prefix
#   - server_id: str, id of the server
# Return:
#   - msg: str, response of the bot
def change_prefix(prefix, server_id):
    msg = _("The prefix on this server has been successfully changed")
    if len(prefix) > 3:
        msg = _("The prefix cannot exceed 3 characters")
    else:
        try:
            with model.laima_db.transaction():
                server = model.Server.get(model.Server.id == server_id)
            server.prefix = prefix
            with model.laima_db.transaction():
                server.save()
        except model.Server.DoesNotExist:
            with model.laima_db.transaction():
                model.Server.create(id=server_id, prefix=prefix)
    return msg

# Define the prefix to use as defined here: https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py#L158
# Parameters:
#   - bot: Laima
#   - message: discord.Message, the message to get the prefix from
# Return:
#   - prefix: str, the prefix to use
def prefix(bot, message):
    try:
        server_id = message.server.id
        with model.laima_db.transaction():
            server = model.Server.get(model.Server.id == server_id)
        prefix = server.prefix
    except model.Server.DoesNotExist:
        prefix = "&"
    return prefix
