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

msg = "```\tRank\t\t\t\t\tCards\tKamas\tPedestal\tTrophy"

def getMessage(rank):
    if rank.common == 2:
        two_cards = "Common"
    if rank.uncommon == 2:
        two_cards = "Uncommon"
    if rank.uncommon == 1:
        one_card = "Uncommon"
    if rank.rare == 1:
        one_card = "Rare"
    if rank.krosmic == 1:
        one_card = "Krosmic"
    if rank.infinite == 1:
        one_card = "Infinite"
    number = util.align_right(rank.number, 8)
    cards = util.align_right("2 {two_cards} & 1 {one_card}".format(two_cards=two_cards, one_card=one_card), 25)
    kamas = util.align_right(str(rank.kamas), 5)
    pedestal = util.align_right("Yes", 8)
    trophy = util.align_right(rank.trophy or "None", 10)
    msg = "{number}{cards}\t{kamas}\t{pedestal}{trophy}".format(number=number, cards=cards, kamas=kamas, pedestal=pedestal, trophy=trophy)
    return msg

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
                msg = "Error, the rank cannot be negative"
            elif num < 6:
                msg = "Sorry, ranks under 6 do not earn anything"
            elif num > 30:
                msg = "Error, there are no rank above 30"
            else:
                with model.laima_db.transaction():
                    rank = model.Rank.get(model.Rank.number == number)
                msg = getMessage(rank)
        except:
            msg = "Error, rank not recognized"
    return msg

def createTable(args):
    msg = "```\tRank\t\t\t\t\tCards\tKamas\tPedestal\tTrophy"
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
