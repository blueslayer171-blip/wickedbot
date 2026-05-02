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

RECORD_CHANNEL_ID = 1500123119812087931

MAPS = ['Factory', 'Skyscraper', 'Hideout', 'Ship', 'Arctic', 'Dam', 'Mall']

async def update_record(client, scrim_won: bool, map_results: list):
    channel = client.get_channel(RECORD_CHANNEL_ID)
    if not channel:
        return

    # Find existing record message
    record_message = None
    async for message in channel.history(limit=50):
        if message.author == client.user and 'WICKED RECORD' in message.content:
            record_message = message
            break

    # Parse existing record or start fresh
    if record_message:
        lines = record_message.content.split('\n')
        # Parse overall record
        overall_line = lines[1]
        parts = overall_line.replace('**Overall:** ', '').split(' - ')
        overall_wins = int(parts[0].replace('W', ''))
        overall_losses = int(parts[1].replace('L', ''))

        # Parse map records
        map_records = {}
        for line in lines[4:]:
            if ':' in line:
                map_name = line.split(':')[0].strip().replace('🗺️ ', '')
                stats = line.split(':')[1].strip()
                w = int(stats.split('/')[0].strip().replace('W', ''))
                l = int(stats.split('/')[1].strip().split('(')[0].strip().replace('L', ''))
                map_records[map_name] = [w, l]
    else:
        overall_wins = 0
        overall_losses = 0
        map_records = {m: [0, 0] for m in MAPS}

    # Update overall record
    if scrim_won:
        overall_wins += 1
    else:
        overall_losses += 1

    # Update map records
    for map_name, won in map_results:
        matched = next((m for m in MAPS if m.lower() == map_name.lower()), None)
        if matched:
            if matched not in map_records:
                map_records[matched] = [0, 0]
            if won:
                map_records[matched][0] += 1
            else:
                map_records[matched][1] += 1

    # Make sure all maps exist
    for m in MAPS:
        if m not in map_records:
            map_records[m] = [0, 0]

    # Build message
    content = '**🏆 WICKED RECORD**\n'
    content += f'**Overall:** {overall_wins}W - {overall_losses}L\n'
    total = overall_wins + overall_losses
    overall_wr = round((overall_wins / total) * 100) if total > 0 else 0
    content += f'**Win Rate:** {overall_wr}%\n\n'
    content += '**Map Records:**\n'

    for map_name in MAPS:
        w, l = map_records.get(map_name, [0, 0])
        total_maps = w + l
        wr = round((w / total_maps) * 100) if total_maps > 0 else 0
        content += f'🗺️ {map_name}: {w}W / {l}L ({wr}% Win Rate)\n'

    if record_message:
        await record_message.edit(content=content)
    else:
        await channel.send(content)

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

    # Calculate map results
    map_results = []
    wicked_map_wins = 0
    opponent_map_wins = 0

    for map_name, score in [(map1, map1_score), (map2, map2_score), (map3, map3_score)]:
        if map_name and score:
            winner = get_winner(score, opposing_team)
            won = winner == 'WICKED Win'
            map_results.append((map_name, won))
            if won:
                wicked_map_wins += 1
            else:
                opponent_map_wins += 1

    scrim_won = wicked_map_wins > opponent_map_wins
    await update_record(interaction.client, scrim_won, map_results)

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