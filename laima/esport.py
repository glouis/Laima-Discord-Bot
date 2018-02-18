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

from lxml import html
import requests
import util

def get_ladder():
    params = { 'ladder': 1 }
    headers = { 'X-Requested-With': 'XMLHttpRequest' }
    page = requests.get(_('https://www.krosmaga.com/en/esport'), headers=headers, params=params)
    tree = html.fromstring(page.content)

    ladder = dict()
    ladder["places"] = tree.xpath('//span[@class="ak-place"]/text()')
    ladder["names"] = tree.xpath('//span[@class="ak-name"]/text()')
    ladder["points"] = tree.xpath('//span[@class="ak-pts"]/text()')

    return ladder

def get_calendar():
    page = requests.get(_('https://www.krosmaga.com/en/esport'))
    tree = html.fromstring(page.content)

    calendar = dict()
    calendar["names"] = [elt.rstrip() for elt in tree.xpath('//div[@class="ak-name"]/text()') if elt != '\n']
    calendar["dates"] = [elt.lower() for elt in tree.xpath('//div[@class="ak-date"]/text()')]

    return calendar

def create_rung(ladder, first, last):
    msg = "```{place}{name}{points}".format(place="  #", name=util.align_right(_("Nickname"), 30), points=util.align_right(_("Points"), 9))

    for i in range(first-1, last):
        place = util.align_right(ladder["places"][i], 3)
        name = util.align_right(ladder["names"][i], 30)
        points = util.align_right(ladder["points"][i], 9)
        msg = '\n'.join([msg, "{place}{name}{points}".format(place=place, name=name, points=points)])

    msg = '\n'.join([msg, "```"])
    return msg

def create_ladder(ladder, first=1, last=20):
    msgs = list()
    while last - first >= 20:
        msg = create_rung(ladder, first, first + 19)
        first = first + 20
        msgs.append(msg)
    msg = create_rung(ladder, first, last)
    msgs.append(msg)

    return msgs

def create_calendar(calendar):
    msg = "```{tournament}{date}".format(tournament=util.align_right(_("Tournament"), 21), date=util.align_right(_("Dates"), 37))

    for i in range(len(calendar["names"])):
        name = util.align_right(calendar["names"][i], 21)
        date = util.align_right(calendar["dates"][i], 37)
        msg = '\n'.join([msg, "{name}{date}".format(name=name, date=date)])

    msg = '\n'.join([msg, "```"])

    return msg
