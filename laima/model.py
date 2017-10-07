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
import json
import os
from peewee import *
import re
import unidecode

laima_db = SqliteDatabase("laima.db")
languages = [("EN", 1), ("FR", 2), ("ES", 3)]

class PackColour(enum.Enum):
    BRONZE = 3
    SILVER = 2
    GOLD = 1
    NECRO = 4

class Trophy(enum.Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    TOP20 = 20
    TOP100 = 100
    VETERAN = 30

class CardType(enum.Enum):
    CREATURE = 0
    SPELL = 1
    OBJECT = 2

class Extension(enum.Enum):
    BASE = 1
    NECRO = 518

class Family(enum.Enum):
    NONE = 0
    IOP = 1
    CRA = 2
    ENIRIPSA = 3
    ENUTROF = 4
    SRAM = 5
    SACRIER = 6
    FECA = 7
    ECAFLIP = 8
    XELOR = 9
    OSAMODAS = 10
    MULTIMAN = 11
    ARACHNEE = 12
    TOFU = 13
    GOBBALL = 14
    BOOWOLF = 15
    LARVA = 16
    TREECHNID = 17
    WABBITS = 18
    RAT = 19
    DRHELLER = 20
    VAMPIRE = 21
    CRACKLER = 22
    SCARALEAF = 23
    PIWI = 24
    BLIBLI = 25
    STRICH = 26
    MONK = 27
    CHAFER = 28
    CAWWOT = 29
    JELLY = 30
    WHISPERER = 31
    SADIDA = 32
    BROTHERHOOD_OF_THE_TOFU = 33
    UNKNOW = 34
    HUPPERMAGE = 35
    BOW_MEOW = 36
    RIKTUS = 37
    KOKOKO = 38
    MOOGRR = 39
    SNAPPER = 40
    SCHNEK = 41
    CROBAK = 42
    DOLL = 43
    OUGINAK = 44
    MASQUERAIDER = 45
    ROGUE = 46
    BANDIT = 47
    BELLAPHONE = 48
    MUSHD = 49
    BWORK = 50
    PIG = 51
    CASTUC = 52
    TOAD = 53
    KWISMAS_CREATURE = 54
    DRAGON = 55
    ELIATROPE = 56
    SCARECROW = 57
    PUDDLY = 58
    GRAMBO = 59
    VIGILANTE = 60
    KRALOVE = 61
    MOSKITO = 62
    PRINCESS = 63
    PRESPIC = 64
    PLANT = 65
    POLTER = 66
    FLEA = 67
    SHARK = 68
    ALBATROCIOUS = 69
    SHUSHU = 70
    FOGGERNAUT = 71
    TAUR = 72
    TROOL = 73
    MIDGINS = 74
    LOOT = 75
    CHEST = 76
    PALADIR = 77
    NECRO = 78
    TRAP = 79
    SNOOFLE = 80
    DRHELLZERKER = 81

class God(enum.Enum):
    NEUTRAL = 0
    IOP = 1
    CRA = 2
    ENIRIPSA = 3
    ECAFLIP = 4
    ENUTROF = 5
    SRAM = 6
    XELOR = 7
    SACRIER = 8
    SADIDA = 10
    RUSHU = 17

class Rarity(enum.Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    KROSMIC = 3
    INFINITE = 4

class BaseModel(Model):
    class Meta:
        database = laima_db

class Draft(BaseModel):
    victories_number = IntegerField(unique=True)
    level = IntegerField()
    pack = IntegerField()
    kamas = CharField()
    chips = CharField()
    earnings = CharField()

    class Meta:
        order_by = ('victories_number',)

class Server(BaseModel):
    id = CharField(unique=True)
    lang = IntegerField(default=1)
    prefix = CharField(default="&")

    class Meta:
        order_by = ('id',)

class Channel(BaseModel):
    id = CharField(unique=True)
    lang = IntegerField(default=None, null=True)
    twitter = BooleanField(default=False)
    rss = BooleanField(default=False)
    server = ForeignKeyField(Server, related_name='channels')

    class Meta:
        order_by = ('id',)

class Rank(BaseModel):
    number = CharField(unique=True)
    common = IntegerField(default = 0)
    uncommon = IntegerField(default = 0)
    rare = IntegerField(default = 0)
    krosmic = IntegerField(default = 0)
    infinite = IntegerField(default = 0)
    kamas = IntegerField()
    pedestal = BooleanField(default = True)
    trophy = IntegerField(default = None, null=True)

    class Meta:
        order_by = ('number',)

class CardData(BaseModel):
    card_id = CharField(unique=True)
    card_type = IntegerField()
    ap_cost = IntegerField()
    life = IntegerField()
    attack = IntegerField()
    movement_point = IntegerField()
    extension = IntegerField()
    families = CharField(default="0")
    god = IntegerField(default=0)
    rarity = IntegerField()
    infinite_level = IntegerField(null=True, default=None)
    is_token = BooleanField(default=False)

    class Meta:
        order_by = ('card_id',)

class CardText(BaseModel):
    card_data = ForeignKeyField(CardData, related_name='texts')
    name = CharField()
    description = TextField()
    lang = IntegerField()

    class Meta:
        order_by = ('name',)

class Tag(BaseModel):
    name = CharField(unique=True)

    class Meta:
        order_by = ('name',)

class CardTextTag(BaseModel):
    cardtext = ForeignKeyField(CardText, related_name='tags')
    tag = ForeignKeyField(Tag, related_name='cardtexts')

def create_tables():
    laima_db.connect()
    laima_db.create_tables([CardData, CardText, CardTextTag, Channel, Draft, Rank, Server, Tag])
    laima_db.close()

def init_draft():
    for i in range(13):
        if i < 7:
            pack = PackColour.BRONZE.value
            if i == 0:
                level = 1
                kamas = "15-25"
                chips = "0"
                earnings = "15-25"
            elif i < 4:
                level = 2
                kamas = "25-35"
                if i == 1:
                    chips = "50"
                    earnings = "30-40"
                if i == 2:
                    chips = "100-150"
                    earnings = "35-50"
                if i == 3:
                    chips = "150-250"
                    earnings = "40-60"
            else:
                level = 3
                kamas = "35-45"
                if i == 4:
                    chips = "250-350"
                    earnings = "60-80"
                if i == 5:
                    chips = "350-600"
                    earnings = "70-105"
                if i == 6:
                    chips = "450-850"
                    earnings = "80-130"
        else:
            level = 4
            if i < 10:
                pack = PackColour.SILVER.value
                kamas = "50-60"
                if i == 7:
                    chips = "700-1100"
                    earnings = "120-170"
                if i == 8:
                    chips = "950-1700"
                    earnings = "145-230"
                if i == 9:
                    chips = "1200-2300"
                    earnings = "170-290"
            else:
                pack = PackColour.GOLD.value
                kamas = "200"
                if i == 10:
                    chips = "1800-2900"
                    earnings = "380-490"
                if i == 11:
                    chips = "2400-2950"
                    earnings = "440-495"
                if i == 12:
                    chips = "3000"
                    earnings = "500"
        with laima_db.transaction():
            Draft.create(victories_number=i,
                level=level,
                pack=pack,
                kamas=kamas,
                chips=chips,
                earnings=earnings)

def init_rank():
    for i in range(6, 31):
        number = str(i)
        if i < 18:
            kamas = (i - 3) * 5
            if i < 11:
                with laima_db.transaction():
                    Rank.create(number=number,
                        common=2,
                        uncommon=1,
                        kamas=kamas)
            elif i < 16:
                with laima_db.transaction():
                    Rank.create(number=number,
                        common=2,
                        rare=1,
                        kamas=kamas)
            else:
                with laima_db.transaction():
                    Rank.create(number=number,
                        uncommon=2,
                        rare=1,
                        kamas=kamas)
        elif i < 26:
            kamas = (i - 10) * 10
            if i < 21:
                with laima_db.transaction():
                    Rank.create(number=number,
                        uncommon=2,
                        rare=1,
                        kamas=kamas)
            else:
                with laima_db.transaction():
                    Rank.create(number=number,
                        uncommon=2,
                        krosmic=1,
                        kamas=kamas)
        else:
            if i == 30:
                with laima_db.transaction():
                    Rank.create(number=number,
                        uncommon=2,
                        infinite=1,
                        kamas=300,
                        trophy=Trophy.VETERAN.value)
            else:
                kamas = (i - 19) * 25
                with laima_db.transaction():
                    Rank.create(number=number,
                        uncommon=2,
                        infinite=1,
                        kamas=kamas)

    with laima_db.transaction():
        Rank.create(number="Top 100",
            uncommon=2,
            infinite=1,
            kamas=300,
            trophy=Trophy.TOP100.value)
        Rank.create(number="Top 20",
            uncommon=2,
            infinite=1,
            kamas=300,
            trophy=Trophy.TOP20.value)
        Rank.create(number="3rd",
            uncommon=2,
            infinite=1,
            kamas=300,
            trophy=Trophy.THIRD.value)
        Rank.create(number="2nd",
            uncommon=2,
            infinite=1,
            kamas=300,
            trophy=Trophy.SECOND.value)
        Rank.create(number="1st",
            uncommon=2,
            infinite=1,
            kamas=300,
            trophy=Trophy.FIRST.value)

def init_card_and_tag(directory):
    for filename in os.listdir(directory):
        print(filename)
        filepath = directory + "/" + filename
        json_to_card_and_tag(filepath)

def json_to_card_and_tag(filepath):
    inf_lvl_regex = re.compile(r"\d$")
    bold_regex = re.compile(r"<.?b>")
    with open(filepath, 'r') as file_data:
        data = json.load(file_data)
        name = {}
        tags = {}
        desc = {}
        families = ','.join([str(fam) for fam in data["Families"]])
        infinite_level = None
        if data["Rarity"] == 4:
            inf_lvl = inf_lvl_regex.search(data["Name"]).group(0)
            infinite_level = int(inf_lvl)
        for language, __ in languages:
            name[language] = data["Texts"]["Name" + language]
            tags[language] = unidecode.unidecode(name[language]).lower().split()
            desc[language] = ' '.join(data["Texts"]["Desc" + language].split())
            desc[language] = bold_regex.subn("**", desc[language])[0]
            if data["Rarity"] == 4:
                tags[language].append(inf_lvl)
        with laima_db.transaction():
            card_data = CardData.create(card_id=data["Name"],
                card_type=data["CardType"],
                ap_cost=data["CostAP"],
                life=data["Life"],
                attack=data["Attack"],
                movement_point=data["MovementPoint"],
                extension=data["Extension"],
                families=families,
                god=data["GodType"],
                rarity=data["Rarity"],
                infinite_level=infinite_level,
                is_token=data["IsToken"])
            for language, lang_id in languages:
                card_text = CardText.create(card_data=card_data,
                    name=name[language],
                    description=desc[language],
                    lang = lang_id)
                for tag in tags[language]:
                    tag_row = Tag.get_or_create(name=tag)[0]
                    card_tag = CardTextTag.create(cardtext=card_text, tag=tag_row)
