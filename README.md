# Laima Discord Bot

Laima is a [Discord](https://discordapp.com/) bot for the [Krosmaga](https://www.krosmaga.com/) CCG (Collecting Card Game).
**[Click here](https://discordapp.com/oauth2/authorize?client_id=330684050736021506&scope=bot&permissions=0)** to add it to your Discord server!

<div align="center">
    <img src="http://pre00.deviantart.net/688f/th/pre/i/2013/005/5/7/joker_and_bow_meow_by_renajvi-d5qi3jx.jpg" alt="Joker and bow Meow" width="254">
    <p>Illustration by <a href="http://fearei.deviantart.com/">FeaRei</a></p>
</div>

## Commands

### About
Give information about the bot.

### Draft

#### No subcommand
Calculate the earnings of the draft mode. Give the play number(s) where you lose.

    &draft 4 8

If you reached the level four, you will be ask to indicate the play number(s) where you did an all-in. You need to give the play number(s) or one of the accepted key-words: none, 0, all.

#### Table
Display a table with the potential earnings. Give the number(s) of victories for which you want an estimation of the earnings. Without parameters, display the complete table.

    &draft table 4 5 6

### Lang
Allow to change the language used on the server or in a channel. Takes two parameters. First is to precise where you want to change the language (channel or server). Second is to indicate which language you want to use (available: en, fr) ; use 0 for a channel to make it use the language of the server.

    &lang server fr

### Prefix
Change the prefix to call Laima on a server. Give the new prefix you want to use. Limited to 3 characters.

    &prefix ß

### Season
Display the rewards of the ranked mode. Give the rank(s) for which you want to know the rewards. Accepted values are number from 6 to 30, top100, top20, 3rd, 2nd and 1st. If no rank are given, display the all table.

    &season 21

### Rss
Allow to subscribe or unsubscribe to the rss feed of the [Krosmaga website](https://www.krosmaga.com). The news are displayed in the language of the channel (or server if not defined).

#### Subscribe | On
Subscribe the current channel

    &rss on

#### Unsubscribe | Off
Unsubscribe the current channel

    &rss off

#### Status
Indicate if the current channel is currently subscribed or not

    &rss status

### Twitter
Allow to subscribe or unsubscribe to one of the twitter timeline of Krosmaga. The tweets displayed are from the timeline of the same language as the one of the channel (or server if not defined).

#### Subscribe | On
Subscribe the current channel

    &twitter on

#### Unsubscribe | Off
Unsubscribe the current channel

    &twitter off

#### Status
Indicate if the current channel is currently subscribed or not

    &twitter status

#### Last
Display the last tweet of Krosmaga

    &twitter last

## Developer guide
Here you will find some instruction to launch ***Laima Discord Bot***. It is recommanded to use Python3.
1. Create a python virtual environnement and activate it
2. Install the dependencies using the *requirements.txt* file
3. Complete the *laima/config.py* file with your Discord & Twitter data
4. Before the first launch, create the database running this command from the root folder of the project:
```bash
python laima/create_database.py
```
5. Run the following command (still in the root folder of the project):
```bash
python laima/main.py
```
If all works correctly, you should see this:
```
Logged in as
Laima
481516234211235813
------
```

## Translator guide
If you want to use Laima in a language that is not yet supported, you can provide it! Simply clone the project, create a folder with the [two-letter abbrevation](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of your language and a subfolder LC_MESSAGES under laima/i18n. Copy the laima.po in it, and translate it (see example of existing languages). You can use [Poedit](https://poedit.net/) to help you in the task. Finally, do a push request, your help will be very appreciated!
