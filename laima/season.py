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

import internationalization
import model
import util

# Define the ligne with the rewards of a rank
# Parameters:
#   - rank: Rank, the rank to add
# Return:
#   - msg: str, the rewards
def getMessage(rank):
    if rank.common == 2:
        two_cards = _("Common")
    if rank.uncommon == 2:
        two_cards = _("Uncommon")
    if rank.uncommon == 1:
        one_card = _("Uncommon")
    if rank.rare == 1:
        one_card = _("Rare")
    if rank.krosmic == 1:
        one_card = _("Krosmic")
    if rank.infinite == 1:
        one_card = _("Infinite")
    number = util.align_right(rank.number, len(_("   Rank")))
    cards = util.align_right("2 {two_cards} & 1 {one_card}".format(two_cards=two_cards, one_card=one_card), len(_("                    Cards")))
    kamas = util.align_right(str(rank.kamas), len(_("  Kamas")))
    pedestal = util.align_right(_("Yes"), len(_("  Pedestal")))
    if rank.trophy is None:
        trophy = _("None")
    else:
        trophy = util.trophy_to_string(model.Trophy(rank.trophy))
    trophy = util.align_right(trophy, len(_("   Trophy")))
    msg = "{number}{cards}{kamas}{pedestal}{trophy}".format(number=number, cards=cards, kamas=kamas, pedestal=pedestal, trophy=trophy)
    return msg

# Define the message to add to the table
# Parameters:
#   - number: str, rank researched
# Return:
#   - msg: str, the message to add to the table
def getRankEarnings(number):
    if number in ["top100", "top20", "3rd", "2nd", "1st"]:
        if number == "top100":
            number = "Top 100"
        if number == "top20":
            number = "Top 20"
        with model.laima_db.transaction():
            rank = model.Rank.get(model.Rank.number == number)
        msg = getMessage(rank)
    else:
        try:
            num = int(number)
            if num < 0:
                msg = _("Error, the rank cannot be negative")
            elif num < 6:
                msg = _("Sorry, ranks under 6 do not earn anything")
            elif num > 30:
                msg = _("Error, there are no rank above 30")
            else:
                with model.laima_db.transaction():
                    rank = model.Rank.get(model.Rank.number == number)
                msg = getMessage(rank)
        except:
            msg = _("Error, rank not recognized")
    return msg

# Create the table of rewards
# Parameters:
#   - args: list, the arguments given to the season command
# Return:
#   - msg, str, the message to display
def createTable(args):
    msg = "```{rank}{cards}{kamas}{pedestal}{trophy}".format(rank=_("   Rank"), cards=_("                    Cards"), kamas=_("  Kamas"), pedestal=_("  Pedestal"), trophy=_("   Trophy"))
    if len(args) == 0:
        for number in range(6, 31):
            msg = '\n'.join([msg, getRankEarnings(str(number))])
        for number in ["top100", "top20", "3rd", "2nd", "1st"]:
            msg = '\n'.join([msg, getRankEarnings(number)])
    else:
        for arg in args:
            msg = '\n'.join([msg, getRankEarnings(arg.lower())])
    msg = '\n'.join([msg, "```"])
    return msg
