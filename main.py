import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import webserver
import asyncio
from datetime import datetime
import pytz

load_dotenv()
TOKEN = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@tree.command(name='scrim-roster', description='Create a scrim embed')
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

@tree.command(name='match-roster', description='Create a match embed')
@app_commands.describe(
    team='The other team name',
    time='Time of the match',
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
async def match_roster(
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
        title=f'Match vs {team}',
        color=0xFF0000,
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
@app_commands.describe(
    team='The opposing team name',
    time='Time of the scrim (e.g. 8:00 PM)',
    timezone='Your timezone'
)
@app_commands.choices(timezone=[
    app_commands.Choice(name='EST', value='US/Eastern'),
    app_commands.Choice(name='CST', value='US/Central'),
    app_commands.Choice(name='PST', value='US/Pacific'),
])
async def scrim_reminder(interaction: discord.Interaction, team: str, time: str, timezone: app_commands.Choice[str]):
    tz = pytz.timezone(timezone.value)
    now = datetime.now(tz)

    try:
        scrim_time = datetime.strptime(time, '%I:%M %p')
        scrim_time = tz.localize(scrim_time.replace(year=now.year, month=now.month, day=now.day))
        timestamp = int(scrim_time.timestamp())
        time_str = f'<t:{timestamp}:t>'
        countdown_str = f'<t:{timestamp}:R>'
    except:
        await interaction.response.send_message('Invalid time format. Use something like 8:00 PM', ephemeral=True)
        return

    embed = discord.Embed(
        title='SCRIM REMINDER',
        description=f'Scrim vs **{team}**\nTime: {time_str}\n{countdown_str}',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(
        content='<@&1475257569231769699>',
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )


@tree.command(name='match-reminder', description='Send a match reminder')
@app_commands.describe(
    team='The opposing team name',
    time='Time of the match (e.g. 8:00 PM)',
    timezone='Your timezone'
)
@app_commands.choices(timezone=[
    app_commands.Choice(name='EST', value='US/Eastern'),
    app_commands.Choice(name='CST', value='US/Central'),
    app_commands.Choice(name='PST', value='US/Pacific'),
])
async def match_reminder(interaction: discord.Interaction, team: str, time: str, timezone: app_commands.Choice[str]):
    tz = pytz.timezone(timezone.value)
    now = datetime.now(tz)

    try:
        match_time = datetime.strptime(time, '%I:%M %p')
        match_time = tz.localize(match_time.replace(year=now.year, month=now.month, day=now.day))
        timestamp = int(match_time.timestamp())
        time_str = f'<t:{timestamp}:t>'
        countdown_str = f'<t:{timestamp}:R>'
    except:
        await interaction.response.send_message('Invalid time format. Use something like 8:00 PM', ephemeral=True)
        return

    embed = discord.Embed(
        title='MATCH REMINDER',
        description=f'Match vs **{team}**\nTime: {time_str}\n{countdown_str}',
        color=0xFF0000,
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(
        content='<@&1475257569231769699>',
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )
class TryoutView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.accepted = []
        self.declined = []

    async def update_embed(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        date_value = embed.fields[0].value
        time_value = embed.fields[1].value
        accepted_str = '\n'.join(self.accepted) if self.accepted else 'None'
        declined_str = '\n'.join(self.declined) if self.declined else 'None'

        embed.clear_fields()
        embed.add_field(name='📅 Date', value=date_value, inline=True)
        embed.add_field(name='🕙 Time', value=time_value, inline=True)
        embed.add_field(name='\u200B', value='\u200B', inline=True)
        embed.add_field(name='✅ Accepted', value=accepted_str, inline=False)
        embed.add_field(name='❌ Declined', value=declined_str, inline=False)

        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label='✅ Accept', style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.user.display_name
        if name in self.declined:
            self.declined.remove(name)
        if name not in self.accepted:
            self.accepted.append(name)
        await interaction.response.defer()
        await self.update_embed(interaction)

    @discord.ui.button(label='❌ Decline', style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        name = interaction.user.display_name
        if name in self.accepted:
            self.accepted.remove(name)
        if name not in self.declined:
            self.declined.append(name)
        await interaction.response.defer()
        await self.update_embed(interaction)


@tree.command(name='tryout', description='Post a tryout embed')
@app_commands.describe(
    date='Date of the tryout',
    time='Time of the tryout (e.g. 8:00 PM)',
)
async def tryout(interaction: discord.Interaction, date: str, time: str):
    embed = discord.Embed(
        title='WICKED TRYOUT',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name='📅 Date', value=date, inline=True)
    embed.add_field(name='🕙 Time', value=time, inline=True)
    embed.add_field(name='\u200B', value='\u200B', inline=True)
    embed.add_field(name='✅ Accepted', value='None', inline=False)
    embed.add_field(name='❌ Declined', value='None', inline=False)

    view = TryoutView()

    await interaction.response.send_message(
        content='<@&1475290401274593412>',
        embed=embed,
        view=view,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

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

def is_manager():
    async def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.user.roles, id=1475257569244221501)
        if role is None:
            await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

async def update_record(client, scrim_won: bool, map_results: list):
    channel = client.get_channel(RECORD_CHANNEL_ID)
    if not channel:
        return

    record_message = None
    async for message in channel.history(limit=50):
        if message.author == client.user and 'WICKED RECORD' in message.content:
            record_message = message
            break

    if record_message:
        lines = record_message.content.split('\n')
        overall_line = lines[1]
        parts = overall_line.replace('**Overall:** ', '').split(' - ')
        overall_wins = int(parts[0].replace('W', '').strip())
        overall_losses = int(parts[1].replace('L', '').strip())

        map_records = {}
        for line in lines[4:]:
            if '🗺️' in line and ':' in line:
                map_name = line.split(':')[0].strip().replace('🗺️ ', '')
                stats = line.split(':')[1].strip()
                w = int(stats.split('/')[0].strip().replace('W', '').strip())
                l = int(stats.split('/')[1].strip().split('(')[0].strip().replace('L', '').strip())
                map_records[map_name] = [w, l]
    else:
        overall_wins = 0
        overall_losses = 0
        map_records = {m: [0, 0] for m in MAPS}

    if scrim_won:
        overall_wins += 1
    else:
        overall_losses += 1

    for map_name, won in map_results:
        matched = next((m for m in MAPS if m.lower() == map_name.lower()), None)
        if matched:
            if matched not in map_records:
                map_records[matched] = [0, 0]
            if won:
                map_records[matched][0] += 1
            else:
                map_records[matched][1] += 1

    for m in MAPS:
        if m not in map_records:
            map_records[m] = [0, 0]

    total = overall_wins + overall_losses
    overall_wr = round((overall_wins / total) * 100) if total > 0 else 0

    content = '**🏆 WICKED RECORD**\n'
    content += f'**Overall:** {overall_wins}W - {overall_losses}L\n'
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

@tree.command(name='match-result', description='Post match results')
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
async def match_result(
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
        title=f'Match vs {opposing_team}',
        color=0xFF0000,
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
        'passive',
        'Fluthagr8',
        'Flighty',
        'trick.nvm',
        'gamma2-',
        'Deftones',
        'TADASHI',
        'Cutskills'
    ]

    number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

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

@tree.command(name='clear-record', description='Clear the entire record')
@is_manager()
async def clear_record(interaction: discord.Interaction):
    channel = interaction.client.get_channel(RECORD_CHANNEL_ID)
    async for message in channel.history(limit=50):
        if message.author == interaction.client.user and 'WICKED RECORD' in message.content:
            await message.delete()
            await interaction.response.send_message('Record has been cleared.', ephemeral=True)
            return
    await interaction.response.send_message('No record found.', ephemeral=True)


@tree.command(name='undo-record', description='Undo the most recent scrim result')
@is_manager()
@app_commands.describe(result='Was the last scrim a win or loss?')
@app_commands.choices(result=[
    app_commands.Choice(name='Win', value='win'),
    app_commands.Choice(name='Loss', value='loss')
])
async def undo_record(interaction: discord.Interaction, result: app_commands.Choice[str]):
    channel = interaction.client.get_channel(RECORD_CHANNEL_ID)
    record_message = None
    async for message in channel.history(limit=50):
        if message.author == interaction.client.user and 'WICKED RECORD' in message.content:
            record_message = message
            break

    if not record_message:
        await interaction.response.send_message('No record found.', ephemeral=True)
        return

    lines = record_message.content.split('\n')
    overall_line = lines[1]
    parts = overall_line.replace('**Overall:** ', '').split(' - ')
    overall_wins = int(parts[0].replace('W', ''))
    overall_losses = int(parts[1].replace('L', ''))

    if result.value == 'win' and overall_wins > 0:
        overall_wins -= 1
    elif result.value == 'loss' and overall_losses > 0:
        overall_losses -= 1

    total = overall_wins + overall_losses
    overall_wr = round((overall_wins / total) * 100) if total > 0 else 0

    new_content = record_message.content
    new_content = new_content.replace(overall_line, f'**Overall:** {overall_wins}W - {overall_losses}L')
    new_content = new_content.replace(lines[2], f'**Win Rate:** {overall_wr}%')

    await record_message.edit(content=new_content)
    await interaction.response.send_message('Record has been updated.', ephemeral=True)


@tree.command(name='set-record', description='Manually set the overall or map record')
@is_manager()
@app_commands.describe(
    type='Overall or specific map',
    wins='Number of wins',
    losses='Number of losses'
)
@app_commands.choices(type=[
    app_commands.Choice(name='Overall', value='Overall'),
    app_commands.Choice(name='Factory', value='Factory'),
    app_commands.Choice(name='Skyscraper', value='Skyscraper'),
    app_commands.Choice(name='Hideout', value='Hideout'),
    app_commands.Choice(name='Ship', value='Ship'),
    app_commands.Choice(name='Arctic', value='Arctic'),
    app_commands.Choice(name='Dam', value='Dam'),
    app_commands.Choice(name='Mall', value='Mall'),
])
async def set_record(interaction: discord.Interaction, type: app_commands.Choice[str], wins: int, losses: int):
    channel = interaction.client.get_channel(RECORD_CHANNEL_ID)
    record_message = None
    async for message in channel.history(limit=50):
        if message.author == interaction.client.user and 'WICKED RECORD' in message.content:
            record_message = message
            break

    if not record_message:
        await interaction.response.send_message('No record found. Use /scrim-result first.', ephemeral=True)
        return

    content = record_message.content

    if type.value == 'Overall':
        lines = content.split('\n')
        overall_line = lines[1]
        win_rate_line = lines[2]
        total = wins + losses
        wr = round((wins / total) * 100) if total > 0 else 0
        content = content.replace(overall_line, f'**Overall:** {wins}W - {losses}L')
        content = content.replace(win_rate_line, f'**Win Rate:** {wr}%')
    else:
        lines = content.split('\n')
        for line in lines:
            if f'🗺️ {type.value}:' in line:
                total = wins + losses
                wr = round((wins / total) * 100) if total > 0 else 0
                content = content.replace(line, f'🗺️ {type.value}: {wins}W / {losses}L ({wr}% Win Rate)')
                break

    await record_message.edit(content=content)
    await interaction.response.send_message(f'{type.value} record set to {wins}W - {losses}L.', ephemeral=True)

@tree.command(name='weeklies', description='Post the weekly scrim schedule')
@app_commands.describe(
    monday_team='Monday team', monday_time='Monday time',
    tuesday_team='Tuesday team', tuesday_time='Tuesday time',
    wednesday_team='Wednesday team', wednesday_time='Wednesday time',
    thursday_team='Thursday team', thursday_time='Thursday time',
    friday_team='Friday team', friday_time='Friday time',
    saturday_team='Saturday team', saturday_time='Saturday time',
    sunday_team='Sunday team', sunday_time='Sunday time'
)
async def weeklies(
    interaction: discord.Interaction,
    monday_team: str = 'N/A', monday_time: str = 'N/A',
    tuesday_team: str = 'N/A', tuesday_time: str = 'N/A',
    wednesday_team: str = 'N/A', wednesday_time: str = 'N/A',
    thursday_team: str = 'N/A', thursday_time: str = 'N/A',
    friday_team: str = 'N/A', friday_time: str = 'N/A',
    saturday_team: str = 'N/A', saturday_time: str = 'N/A',
    sunday_team: str = 'N/A', sunday_time: str = 'N/A'
):
    days = [
        ('Monday', monday_team, monday_time),
        ('Tuesday', tuesday_team, tuesday_time),
        ('Wednesday', wednesday_team, wednesday_time),
        ('Thursday', thursday_team, thursday_time),
        ('Friday', friday_team, friday_time),
        ('Saturday', saturday_team, saturday_time),
        ('Sunday', sunday_team, sunday_time),
    ]

    embed = discord.Embed(
        title='WICKED WEEKLY SCHEDULE',
        color=0x9800FF,
        timestamp=discord.utils.utcnow()
    )

    for day, team, time in days:
        embed.add_field(
            name=day,
            value=f'Team - {team}\nTime - {time}',
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@tree.command(name='fist', description='Threaten someone with fists')
@app_commands.describe(user='The user to threaten')
async def fist(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f'{user.mention} will kill you with his fists')

@bot.event
async def on_ready():
    guild = discord.Object(id=1475257569231769690)
    tree.clear_commands(guild=guild)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f'Logged in as {bot.user}')


bot.run(TOKEN)