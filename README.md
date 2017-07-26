# Laima Discord Bot

Laima is a [Discord](https://discordapp.com/) bot for the [Krosmaga](https://www.krosmaga.com/) CCG (Collecting Card Game).
**[Click here](https://discordapp.com/oauth2/authorize?client_id=330684050736021506&scope=bot&permissions=0)** to add it to your Discord server!

<div align="center">
    <img src="http://pre00.deviantart.net/688f/th/pre/i/2013/005/5/7/joker_and_bow_meow_by_renajvi-d5qi3jx.jpg" alt="Joker and bow Meow" style="width: 250px;"/>
    <p>Illustration by [FeaRei](http://fearei.deviantart.com/)</p>
</div>

## Commands

### Draft

#### No subcommand
Calculate the earnings of the draft mode. Give the play number(s) where you lose.

    &draft 4 8

If you reached the level four, you will be ask to indicate the play number(s) where you did an all-in. You need to give the play number(s) or one of the accepted key-words: none, 0, all.

#### Table
Display a table with the potential earnings. Give the number(s) of victories for which you want an estimation of the earnings. Without parameters, display the complete table.

    &draft table 4 5 6

### Twitter
Allow to subscribe or unsubscribe to the [twitter timeline of Krosmaga (fr)](https://twitter.com/krosmaga).

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
4. For the first launch, uncomment the two lines under the **TODO** to create the database (comment them again after)
5. Run the following command from the root folder of the project:
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
