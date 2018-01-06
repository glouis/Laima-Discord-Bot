from lxml import html
import requests
import util

def get_ladder(season=None, search=None):
    ladder = dict()
    ladder["eternal"] = False
    rank_elo = "ak-rank"
    url = _('https://www.krosmaga.com/en/community/leaderboard')
    join_char = '?'
    if season == '0':
        url = '/'.join([url, _("eternal")])
        ladder["eternal"] = True
        rank_elo = "ak-elo"
    else:
        url = '/'.join([url, _("seasonal")])
        if season is not None:
            url = join_char.join([url, "season={0}".format(season)])
            join_char = '&'
    if search is not None:
        url = join_char.join([url, "search={0}".format(search)])

    page = requests.get(url)
    tree = html.fromstring(page.content)

    ladder["places"] = tree.xpath('//td[@class="ak-position"]/span/text()')
    ladder["nicknames"] = tree.xpath('//td[@class="ak-nickname"]/text()')
    ladder["rank_elo"] = tree.xpath('//td[contains(@class, $rank_elo)]/text()', rank_elo=rank_elo)
    ladder["victories"] = tree.xpath('//span[@class="ak-win"]/text()')
    ladder["defeats"] = tree.xpath('//span[@class="ak-lose"]/text()')

    return ladder

def create_message(ladder, first=1, last=1):
    if ladder["eternal"]:
        rank_elo = _("   Elo")
    else:
        rank_elo = _("  Rank")
    try:
        msg = "```{place}{nickname}{rank_elo}{win_lose}".format(place="    #", nickname=util.align_right(_("Nickname"), 30), rank_elo=rank_elo, win_lose=_("  Victories/Defeats"))
        for i in range(first-1, last):
            place = util.align_right(ladder["places"][i], 5)
            nickname = util.align_right(ladder["nicknames"][i], 30)
            rank_elo = util.align_right(ladder["rank_elo"][i], len(rank_elo))
            win_lose = util.align_right(ladder["victories"][i] + "/" + ladder["defeats"][i], len(_("  Victories/Defeats")))
            msg = '\n'.join([msg, "{place}{nickname}{rank_elo}{win_lose}".format(place=place, nickname=nickname, rank_elo=rank_elo, win_lose=win_lose)])
        msg = '\n'.join([msg, "```"])
    except IndexError:
        msg = _("Sorry, I did not find anyone.")
    return msg

def create_messages(ladder, first, last):
    msgs = list()
    while last - first >= 20:
        msg = create_message(ladder, first, first + 19)
        first = first + 20
        msgs.append(msg)
    msg = create_message(ladder, first, last)
    msgs.append(msg)

    return msgs
