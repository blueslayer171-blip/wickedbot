import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import webserver

load_dotenv()
TOKEN = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@tree.command(name='scrim', description='Create a scrim embed')
@app_commands.describe(
    team='The other team name',
    time='Time of the scrim',
    player1='Player 1',
    player2='Player 2',
    player3='Player 3',
    player4='Player 4',
    player5='Player 5',
    subs='Substitute players',
    host='Host name',
    password='Lobby password',
    info='Extra info'
)
async def scrim(
    interaction: discord.Interaction,
    team: str,
    time: str = 'N/A',
    player1: str = 'N/A',
    player2: str = 'N/A',
    player3: str = 'N/A',
    player4: str = 'N/A',
    player5: str = 'N/A',
    subs: str = 'None',
    host: str = 'N/A',
    password: str = 'N/A',
    info: str = 'None'
):
    embed = discord.Embed(
        title=f'Scrim vs {team}',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name='Other Team', value=team, inline=True)
    embed.add_field(name='🕙 Time', value=time, inline=True)
    embed.add_field(name='\u200B', value='\u200B', inline=True)

    embed.add_field(name='Player 1', value=player1, inline=True)
    embed.add_field(name='Player 2', value=player2, inline=True)
    embed.add_field(name='Player 3', value=player3, inline=True)
    embed.add_field(name='Player 4', value=player4, inline=True)
    embed.add_field(name='Player 5', value=player5, inline=True)
    embed.add_field(name='\u200B', value='\u200B', inline=True)

    embed.add_field(name='☎️ Subs', value=subs, inline=False)
    embed.add_field(name='👑 Host', value=host, inline=True)
    embed.add_field(name='🔒 Password', value=password, inline=True)
    embed.add_field(name='📖 Extra Info', value=info, inline=False)

    await interaction.response.send_message(
        content='<@&1475257569231769699>',
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )


@tree.command(name='availability', description='Post weekly availability')
async def availability(interaction: discord.Interaction):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    await interaction.response.send_message(
        content='<@&1475257569231769699>',
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

    for day in days:
        msg = await interaction.channel.send(day)
        await msg.add_reaction('7️⃣')
        await msg.add_reaction('9️⃣')

@tree.command(name='match-reminder', description='Send a scrim reminder')
@app_commands.describe(time='Time of the scrim')
async def match_reminder(interaction: discord.Interaction, time: str):
    embed = discord.Embed(
        title='SCRIM REMINDER',
        description=f'Scrim at {time}',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(
        content='<@&1475257569231769699>',
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

@tree.command(name='roster', description='Display the team roster')
@app_commands.describe(
    main1='Main player 1',
    main2='Main player 2',
    main3='Main player 3',
    main4='Main player 4',
    main5='Main player 5',
    subs='Substitute players'
)
async def roster(
    interaction: discord.Interaction,
    main1: str = 'N/A',
    main2: str = 'N/A',
    main3: str = 'N/A',
    main4: str = 'N/A',
    main5: str = 'N/A',
    subs: str = 'N/A'
):
    embed = discord.Embed(
        title='WICKED ROSTER',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(
        name='Main Roster',
        value=f'{main1}\n{main2}\n{main3}\n{main4}\n{main5}',
        inline=False
    )

    embed.add_field(
        name='Subs',
        value=subs,
        inline=False
    )

    await interaction.response.send_message(embed=embed)

    def get_winner(score: str, opposing_team: str) -> str:
        try:
            parts = score.replace(' ', '').split('-')
            if int(parts[0]) == 7:
                return 'WICKED Win'
            elif int(parts[1]) == 7:
                return f'{opposing_team} Win'
            else:
                return 'Unknown'
        except:
            return ''

@tree.command(name='scrim-result', description='Post scrim results')
@app_commands.describe(
    opposing_team='The opposing team name',
    map1='Map 1 name',
    map1_score='Map 1 score (e.g. 7-2)',
    map2='Map 2 name',
    map2_score='Map 2 score (e.g. 6-7)',
    map3='Map 3 name',
    map3_score='Map 3 score (e.g. 7-4)',
    mvps='MVP players',
    notes='Any additional notes'
)
async def scrim_result(
    interaction: discord.Interaction,
    opposing_team: str,
    map1: str,
    map1_score: str,
    map2: str = None,
    map2_score: str = None,
    map3: str = None,
    map3_score: str = None,
    mvps: str = 'N/A',
    notes: str = 'None'
):
    embed = discord.Embed(
        title=f'Scrim vs {opposing_team}',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    maps_value = f'{map1} : {map1_score} - {get_winner(map1_score, opposing_team)}\n'

    if map2 and map2_score:
        maps_value += f'{map2} : {map2_score} - {get_winner(map2_score, opposing_team)}\n'

    if map3 and map3_score:
        maps_value += f'{map3} : {map3_score} - {get_winner(map3_score, opposing_team)}\n'

    embed.add_field(name='\u200B', value=maps_value, inline=False)
    embed.add_field(name='MVP', value=mvps, inline=False)
    embed.add_field(name='Notes', value=notes, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    guild = discord.Object(id=1475257569231769690)
    tree.clear_commands(guild=guild)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f'Logged in as {bot.user}')


bot.run(TOKEN)