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

import discord
import internationalization
import model
from peewee import fn
import unidecode

card_types = {}
card_types[model.CardType.CREATURE] = _("Creature")
card_types[model.CardType.SPELL] = _("Spell")
card_types[model.CardType.OBJECT] = _("Object")

extensions = {}
extensions[model.Extension.BASE] = _("Base")
extensions[model.Extension.OROPO] = _("Brotherhood of Oropo")
extensions[model.Extension.NECRO] = _("Necro")

families = {}
families[model.Family.NONE] = _("None")
families[model.Family.IOP] = _("Iop")
families[model.Family.CRA] = _("Cra")
families[model.Family.ENIRIPSA] = _("Eniripsa")
families[model.Family.ENUTROF] = _("Enutrof")
families[model.Family.SRAM] = _("Sram")
families[model.Family.SACRIER] = _("Sacrier")
families[model.Family.FECA] = _("Feca")
families[model.Family.ECAFLIP] = _("Ecaflip")
families[model.Family.XELOR] = _("Xelor")
families[model.Family.OSAMODAS] = _("Osamodas")
families[model.Family.MULTIMAN] = _("Multiman")
families[model.Family.ARACHNEE] = _("Arachnee")
families[model.Family.TOFU] = _("Tofu")
families[model.Family.GOBBALL] = _("Gobball")
families[model.Family.BOOWOLF] = _("Boowolf")
families[model.Family.LARVA] = _("Larva")
families[model.Family.TREECHNID] = _("Treechnid")
families[model.Family.WABBITS] = _("Wabbits")
families[model.Family.RAT] = _("Rat")
families[model.Family.DRHELLER] = _("Drheller")
families[model.Family.VAMPIRE] = _("Vampire")
families[model.Family.CRACKLER] = _("Crackler")
families[model.Family.SCARALEAF] = _("Scaraleaf")
families[model.Family.PIWI] = _("Piwi")
families[model.Family.BLIBLI] = _("Blibli")
families[model.Family.STRICH] = _("Strich")
families[model.Family.MONK] = _("Monk")
families[model.Family.CHAFER] = _("Chafer")
families[model.Family.CAWWOT] = _("Cawwot")
families[model.Family.JELLY] = _("Jelly")
families[model.Family.WHISPERER] = _("Whisperer")
families[model.Family.SADIDA] = _("Sadida")
families[model.Family.BROTHERHOOD_OF_THE_TOFU] = _("Brotherhood of the Tofu")
families[model.Family.UNKNOW] = _("Unknow")
families[model.Family.HUPPERMAGE] = _("Huppermage")
families[model.Family.BOW_MEOW] = _("Bow Meow")
families[model.Family.RIKTUS] = _("Riktus")
families[model.Family.KOKOKO] = _("Kokoko")
families[model.Family.MOOGRR] = _("Moogrr")
families[model.Family.SNAPPER] = _("Snapper")
families[model.Family.SCHNEK] = _("Schnek")
families[model.Family.CROBAK] = _("Crobak")
families[model.Family.DOLL] = _("Doll")
families[model.Family.OUGINAK] = _("Ouginak")
families[model.Family.MASQUERAIDER] = _("Masqueraider")
families[model.Family.ROGUE] = _("Rogue")
families[model.Family.BANDIT] = _("Bandit")
families[model.Family.BELLAPHONE] = _("Bellaphone")
families[model.Family.MUSHD] = _("Mushd")
families[model.Family.BWORK] = _("Bwork")
families[model.Family.PIG] = _("Pig")
families[model.Family.CASTUC] = _("Castuc")
families[model.Family.TOAD] = _("Toad")
families[model.Family.KWISMAS_CREATURE] = _("Kwismas creature")
families[model.Family.DRAGON] = _("Dragon")
families[model.Family.ELIATROPE] = _("Eliatrope")
families[model.Family.SCARECROW] = _("Scarecrow")
families[model.Family.PUDDLY] = _("Puddly")
families[model.Family.GRAMBO] = _("Grambo")
families[model.Family.VIGILANTE] = _("Vigilante")
families[model.Family.KRALOVE] = _("Kralove")
families[model.Family.MOSKITO] = _("Moskito")
families[model.Family.PRINCESS] = _("Princess")
families[model.Family.PRESPIC] = _("Prespic")
families[model.Family.PLANT] = _("Plant")
families[model.Family.POLTER] = _("Polter")
families[model.Family.FLEA] = _("Flea")
families[model.Family.SHARK] = _("Shark")
families[model.Family.ALBATROCIOUS] = _("Albatrocious")
families[model.Family.SHUSHU] = _("Shushu")
families[model.Family.FOGGERNAUT] = _("Foggernaut")
families[model.Family.TAUR] = _("Taur")
families[model.Family.TROOL] = _("Trool")
families[model.Family.MIDGINS] = _("Midgins")
families[model.Family.LOOT] = _("Loot")
families[model.Family.CHEST] = _("Chest")
families[model.Family.PALADIR] = _("Paladir")
families[model.Family.NECRO] = _("Necro")
families[model.Family.TRAP] = _("Trap")
families[model.Family.SNOOFLE] = _("Snoofle")
families[model.Family.DRHELLZERKER] = _("Drhellzerker")
families[model.Family.GHOUL] = _("Ghoul")
families[model.Family.BROTHERHOOD_OF_THE_FORGOTTEN] = _("Brotherhood of the Forgotten")
families[model.Family.PANDAWA] = _("Pandawa")
families[model.Family.ELIOTROPE] = _("Eliotrope")
families[model.Family.FAN] = _("Fan")

gods = {}
gods[model.God.NEUTRAL] = _("Neutral")
gods[model.God.IOP] = _("Iop")
gods[model.God.CRA] = _("Cra")
gods[model.God.ENIRIPSA] = _("Eniripsa")
gods[model.God.ECAFLIP] = _("Ecaflip")
gods[model.God.ENUTROF] = _("Enutrof")
gods[model.God.SRAM] = _("Sram")
gods[model.God.XELOR] = _("Xelor")
gods[model.God.SACRIER] = _("Sacrier")
gods[model.God.FECA] = _("Feca")
gods[model.God.SADIDA] = _("Sadida")
gods[model.God.RUSHU] = _("Rushu")

rarities = {}
rarities[model.Rarity.COMMON] = _("Common")
rarities[model.Rarity.UNCOMMON] = _("Uncommon")
rarities[model.Rarity.RARE] = _("Rare")
rarities[model.Rarity.KROSMIC] = _("Krosmic")
rarities[model.Rarity.INFINITE] = _("Infinite")

colours = {}
colours[model.God.NEUTRAL] = discord.Colour.light_grey()
colours[model.God.IOP] = discord.Colour.red()
colours[model.God.CRA] = discord.Colour.green()
colours[model.God.ENIRIPSA] = discord.Colour(0xffc0cb)
colours[model.God.ECAFLIP] = discord.Colour.magenta()
colours[model.God.ENUTROF] = discord.Colour.gold()
colours[model.God.SRAM] = discord.Colour.dark_teal()
colours[model.God.XELOR] = discord.Colour.dark_blue()
colours[model.God.SACRIER] = discord.Colour.dark_red()
colours[model.God.FECA] = discord.Colour.dark_gold()
colours[model.God.SADIDA] = discord.Colour.dark_green()
colours[model.God.RUSHU] = discord.Colour.dark_orange()

def to_embed(card):
    name = card.name
    inf_lvl = card.card_data.infinite_level
    if inf_lvl is not None:
        name = ' '.join([name, ":star2:" * inf_lvl])
    card_type = _(card_types[model.CardType(card.card_data.card_type)])
    if card.card_data.is_token:
        card_type = ' '.join([card_type, "(token)"])
    god = model.God(card.card_data.god)
    embed = discord.Embed(title=name, description=card.description, colour=colours[god])
    if card.card_data.families:
        card_families = ' / '.join([_(families[model.Family(int(f))]) for f in card.card_data.families.split(',')])
        embed.set_footer(text=card_families)
    embed.add_field(name=":dividers: " + _("Type"), value="> " + card_type)
    embed.add_field(name=":diamond_shape_with_a_dot_inside: " + _("Rarity"), value="> " + _(rarities[model.Rarity(card.card_data.rarity)]))
    embed.add_field(name=":star: " + _("AP Cost"), value="> " + str(card.card_data.ap_cost))
    if card.card_data.card_type == 0:
        embed.add_field(name=":heart: " + _("Life"), value="> " + str(card.card_data.life))
        embed.add_field(name=":dagger: " + _("Attack"), value="> " + str(card.card_data.attack))
        embed.add_field(name=":footprints: " + _("Movement Point"), value="> " + str(card.card_data.movement_point))
    embed.add_field(name=":link: " + _("Extension"), value="> " + _(extensions[model.Extension(card.card_data.extension)]))

    return embed

def search(keywords, lang):
    formated_keywords = [ unidecode.unidecode(keyword).lower() for keyword in keywords ]
    with model.laima_db.transaction():
        query = (model.CardText
            .select(model.CardText, model.CardData)
            .join(model.CardData)
            .switch(model.CardText)
            .where(model.CardText.lang == lang)
            .join(model.CardTextTag)
            .join(model.Tag)
            .where(model.Tag.name << formated_keywords)
            .group_by(model.CardText)
            .having(fn.Count(model.Tag.id) == len(keywords))
            .order_by(model.CardText.name))
        if query.exists():
            count = query.count()
            cards = [ card for card in query ]
            return cards, count
        else:
            return [], 0
