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

class Presentation:
    def __init__(self, name, title, description, url=None, avatar=None, image=None, colour=None):
        self.name = name
        self.title = title
        self.description = description
        self.url = url
        self.avatar = avatar
        self.image = image
        self.colour = colour
        self.embed = self._create_embed(name=name, title=title, description=description, url=url, avatar=avatar, image=image, colour=colour)

    def _create_embed(self, **kwargs):
        name = kwargs['name']
        title = kwargs['title']
        description = kwargs['description']
        url = kwargs['url'] or discord.EmptyEmbed
        avatar = kwargs['avatar'] or discord.EmptyEmbed
        image = kwargs['image']
        colour = kwargs['colour'] or discord.EmptyEmbed
        embed = discord.Embed(title=title, description=description, url=url, colour=colour)
        embed.set_author(name=name, icon_url=avatar)
        if image is not None:
            embed.set_image(url=image)
        return embed

laima = Presentation(name="Laima",
    title="Discord bot dedicated to the Krosmaga CCG",
    description="I aim to provide useful commands to the Krosmaga community!",
    url="https://github.com/glouis/Laima-Discord-Bot",
    avatar="https://cdn.discordapp.com/app-icons/330684050736021506/cec86350d6620ac4d16931a74f153bf3.jpg",
    colour=discord.Colour.dark_magenta())

fearei = Presentation(name="FeaRei",
    title="Author of the illustration",
    description="Below is the complete illustration of Laima. You can visit the DeviantArt page of FeaRei by cliking on the title!",
    url="http://fearei.deviantart.com/",
    avatar="http://a.deviantart.net/avatars/f/e/fearei.png",
    image="http://pre00.deviantart.net/688f/th/pre/i/2013/005/5/7/joker_and_bow_meow_by_renajvi-d5qi3jx.jpg",
    colour=discord.Colour.dark_blue())
