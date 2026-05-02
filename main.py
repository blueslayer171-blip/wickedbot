import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import webserver
import asyncio

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

@tree.command(name='scrim-reminder', description='Send a scrim reminder')
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

@tree.command(name='ping-available', description='Ping available players for a day')
@app_commands.describe(day='Day of the week')
@app_commands.choices(day=[
    app_commands.Choice(name='Monday', value='Monday'),
    app_commands.Choice(name='Tuesday', value='Tuesday'),
    app_commands.Choice(name='Wednesday', value='Wednesday'),
    app_commands.Choice(name='Thursday', value='Thursday'),
    app_commands.Choice(name='Friday', value='Friday'),
    app_commands.Choice(name='Saturday', value='Saturday'),
    app_commands.Choice(name='Sunday', value='Sunday'),
])
async def ping_available(interaction: discord.Interaction, day: app_commands.Choice[str]):
    await interaction.response.defer()

    channel = interaction.client.get_channel(1477396682030452861)
    if not channel:
        await interaction.followup.send('Could not find availability channel.')
        return

    target_message = None
    async for message in channel.history(limit=100):
        if message.author == interaction.client.user and day.value in message.content:
            target_message = message
            break

    if not target_message:
        await interaction.followup.send(f'Could not find availability message for {day.value}.')
        return

    users = set()
    for reaction in target_message.reactions:
        if str(reaction.emoji) in ['7️⃣', '9️⃣']:
            async for user in reaction.users():
                if not user.bot:
                    users.add(user.mention)

    if not users:
        await interaction.followup.send(f'No one is available on {day.value}.')
        return

    await interaction.followup.send(f'Available on **{day.value}**: {" ".join(users)}')

@tree.command(name='mvp-vote', description='Start an MVP vote')
async def mvp_vote(interaction: discord.Interaction):
    players = [
        'Dopiest',
        'Blue Slayer',
        'Fluthagr8',
        'trick.nwm',
        'gamma2-',
        'Deftones',
        'IceBeast'
    ]

    number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    description = 'Vote for the MVP of the scrim!\n\n'
    for i, player in enumerate(players):
        description += f'{number_emojis[i]} - {player}\n'

    embed = discord.Embed(
        title='MVP Vote',
        description=description,
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()

    for i in range(len(players)):
        await message.add_reaction(number_emojis[i])

    await asyncio.sleep(1800)

    message = await interaction.channel.fetch_message(message.id)

    winner_index = 0
    winner_votes = 0
    for i, reaction in enumerate(message.reactions):
        if str(reaction.emoji) in number_emojis:
            count = reaction.count - 1
            if count > winner_votes:
                winner_votes = count
                winner_index = number_emojis.index(str(reaction.emoji))

    winner = players[winner_index]
    await interaction.channel.send(f'🏆 **{winner}** has won the vote for the MVP of the scrim! 🏆')

@bot.event
async def on_ready():
    guild = discord.Object(id=1475257569231769690)
    tree.clear_commands(guild=guild)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f'Logged in as {bot.user}')


bot.run(TOKEN)