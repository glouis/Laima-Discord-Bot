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

from peewee import *

laima_db = SqliteDatabase("laima.db")

class BaseModel(Model):
    class Meta:
        database = laima_db

class Draft(BaseModel):
    victories_number = IntegerField(unique=True)
    level = IntegerField()
    pack = CharField()
    kamas = CharField()
    chips = CharField()
    earnings = CharField()

    class Meta:
        order_by = ('victories_number',)

class Channel(BaseModel):
    id = CharField(unique=True)
    twitter = BooleanField()

    class Meta:
        order_by = ('id',)

def create_tables():
    laima_db.connect()
    laima_db.create_tables([Draft, Channel])
    laima_db.close()

def init_draft():
    for i in range(13):
        if i < 7:
            pack = "Bronze"
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
                pack = "Silver"
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
                pack = "Gold"
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
