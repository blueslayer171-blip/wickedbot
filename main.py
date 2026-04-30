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


@bot.event
async def on_ready():
    guild = discord.Object(id=1475257569231769690)
    tree.clear_commands(guild=guild)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f'Logged in as {bot.user}')


bot.run(TOKEN)