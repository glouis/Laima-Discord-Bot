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

import itertools
import inspect
import internationalization
import model
from discord.ext.commands.core import GroupMixin, Command
from discord.ext.commands.errors import CommandError
from discord.ext.commands.formatter import HelpFormatter, Paginator

def pack_colour_to_string(pack_colour):
    if pack_colour == model.PackColour.BRONZE:
        return _("Bronze")
    if pack_colour == model.PackColour.SILVER:
        return _("Silver")
    if pack_colour == model.PackColour.GOLD:
        return _("Gold")
    if pack_colour == model.PackColour.NECROM:
        return _("Necroms")

def trophy_to_string(trophy):
    if trophy == model.Trophy.FIRST:
        return _("1st")
    if trophy == model.Trophy.SECOND:
        return _("2nd")
    if trophy == model.Trophy.THIRD:
        return _("3rd")
    if trophy == model.Trophy.TOP20:
        return _("Top 20")
    if trophy == model.Trophy.TOP100:
        return _("Top 100")
    if trophy == model.Trophy.VETERAN:
        return _("Veteran")

# Add spaces on the left of a string
# Parameters:
#   - string: str, the string to align
#   - total_char: int, the number of char of the new string
# Return:
#   - str, the new string
def align_right(string, total_char):
    spaces = ' ' * (total_char - len(string))
    return ''.join([spaces, string])

# Override HelpFormatter to remove indications about categories (which are not used) and allow internationalization
class CustomHelpFormatter(HelpFormatter):
    def get_ending_note(self):
        command_name = self.context.invoked_with
        return _("Type {0}{1} command for more info on a command.").format(self.clean_prefix, command_name)

    def format(self):
        self._paginator = Paginator()

        # we need a padding of ~80 or so

        description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

        if description:
            # <description> portion
            self._paginator.add_line(description, empty=True)

        if isinstance(self.command, Command):
            # <signature portion>
            signature = self.get_command_signature()
            self._paginator.add_line(signature, empty=True)

            # <long doc> section
            if self.command.help:
                self._paginator.add_line(self.command.help, empty=True)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                self._paginator.close_page()
                return self._paginator.pages

        max_width = self.max_name_size

        self._paginator.add_line(_("Commands:"))
        self._add_subcommands_to_page(max_width, self.filter_command_list())

        # add the ending note
        self._paginator.add_line()
        ending_note = self.get_ending_note()
        self._paginator.add_line(ending_note)
        return self._paginator.pages
