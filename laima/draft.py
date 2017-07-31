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

# Read the database to retrieve the potentials earnings for a number of victories
# Parameters:
#   - value: int, number of victories
# Return:
#   - msg: string, formatted text to include in a table
def getEarnings(value):
    error_msg = None
    try:
        num = int(value)
    except:
        msg = "{value} is not an integer".format(value=value)
        return msg
    if(num < 0):
        msg = "The number of victory cannot be negative"
        return msg
    if(num > 12):
        msg = "The number of victory cannot be greater than 12"
        return msg

    with model.laima_db.transaction():
        draft = model.Draft.get(model.Draft.victories_number == num)

    victories = util.align_right(str(draft.victories_number), 9)
    level = util.align_right(str(draft.level), 5)
    pack_colour = model.pack_colours[model.PackColour(draft.pack)]
    pack = util.align_right(pack_colour, 8)
    kamas = util.align_right(draft.kamas, 5)
    chips = util.align_right(draft.chips, 9)
    earnings = util.align_right(draft.earnings, 8)
    msg = "{victories}\t{level}\t{pack}\t{kamas}\t{chips}\t{earnings}".format(victories=victories, level=level, pack=pack, kamas=kamas, chips=chips, earnings=earnings)
    return msg

# Create a table with the approximate earnings for numbers of victories
# Parameters:
#   - args: list, numbers of victories
# Return:
#   - msg: str, the table to display
def createTable(args):
    msg = "```Victories\tLevel\t\tPack\tKamas\t\tChips\tEarnings"
    if len(args) == 0:
        for i in range(13):
            msg = '\n'.join([msg, getEarnings(i)])
    else:
        for arg in args:
            msg = '\n'.join([msg, getEarnings(arg)])
    msg = '\n'.join([msg, "```"])
    return msg

# Calculate the exact earnings of the first part of a draft (levels 1, 2 & 3)
# Parameters:
#   - args: list, numbers of the matchs where the player lost
# Return:
#   - victories_number: int, number of victories on the draft
#   - defeats_number: int, number of defeats on the draft
#   - chips: int, number of chips earned by the player
#   - results: list, the results of the player in the last part of the draft (level 4)
def calcResultsPartOne(args):
    if(len(args) > 3):
        raise Exception("Vous ne pouvez pas perdre plus de 3 fois !")

    i = 0
    chips = 0
    defeats_number = 0
    victories_number = 0
    results = [1 for j in range(12)]

    for arg in args:
        try:
            play = int(arg) - 1
        except:
            error_msg = "{value} n'est pas un nombre".format(value=arg)
            raise Exception(error_msg)
        if play < 0:
            error_msg = "{value} n'est pas supérieur à 1".format(value=arg)
            raise Exception(error_msg)
        elif play > 11:
            error_msg = "{value} n'est pas inférieur à 12".format(value=arg)
            raise Exception(error_msg)
        results[play] = 0

    while defeats_number < 3 and i < 9:
        if results[i] == 0:
            defeats_number += 1
        else:
            victories_number += 1
            if i < 3:
                chips += 50
            elif i < 6:
                chips += 100
            else:
                chips += 250
        i += 1
    while defeats_number < 3 and i < 12:
        if results[i] == 0:
            defeats_number += 1
        else:
            victories_number += 1
        i += 1
    while i < 12:
        results[i] = 0
        i += 1

    return victories_number, defeats_number, chips, results[-3:]

# Calculate the exact earnings of the second part of a draft (level 4)
# Parameters:
#   - chips: int, number of chips won by the player so far
#   - level_four: list, the results of the player on the fourth level
#   - allins: list, indicate if the player choose to play normally or to bet his chips
# Return:
#   - chips: int, number of chips earned by the player
def calcResultsPartTwo(chips, level_four, allins):
    allin_chips = chips
    for i in range(3):
        result = level_four[i]
        allin = allins[i]
        if result == 0:
            if allin == 1:
                chips = allin_chips = 0
        else:
            if allin == 0:
                allin_chips += 600
                chips += 600
            else:
                allin_chips *= 2
                chips += allin_chips
    return chips

# Define what the player won during his draft
# Parameters:
#   - victories: int, the number of victories of the player
#   - chips: int, the number of chips earned by the player
# Return:
#   - msg: string, formatted text to include in a table
def defineEarnings(victories, chips):
    pack = model.PackColour.BRONZE
    if victories == 0:
        level = 1
        kamas = "15-25"
    elif victories < 4:
        level = 2
        kamas = "25-35"
    elif victories < 7:
        level = 3
        kamas = "35-45"
    elif victories < 10:
        level = 4
        pack = model.PackColour.SILVER
        kamas = "50-60"
    else:
        level = 4
        pack = model.PackColour.GOLD
        kamas = "200"

    interval = kamas.split('-')
    kamas_from_chips = chips / 10
    if len(interval) == 1:
        value = int(interval[0]) + kamas_from_chips
        earnings = "{value:n}".format(value=value)
    else:
        value_min = int(interval[0]) + kamas_from_chips
        value_max = int(interval[1]) + kamas_from_chips
        earnings="{min:n}-{max:n}".format(min=value_min, max=value_max)

    victories_str = util.align_right(str(victories), 9)
    level_str = util.align_right(str(level), 5)
    pack_colour = model.pack_colours[model.PackColour(pack)]
    pack_str = util.align_right(str(pack_colour), 8)
    kamas_str = util.align_right(str(kamas), 5)
    chips_str = util.align_right(str(chips), 9)
    earnings_str = util.align_right(str(earnings), 8)

    msg = "{victories}\t{level}\t{pack}\t{kamas}\t{chips}\t{earnings}".format(victories=victories_str, level=level_str, pack=pack_str, kamas=kamas_str, chips=chips_str, earnings=earnings_str)
    return msg
