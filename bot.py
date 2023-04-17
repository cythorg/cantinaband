import discord
import logging

secret = r'./private.key'
with open(secret, 'r') as f:
    private_key = f.readline()
if private_key == "": raise ValueError("private key not set in 'private.key' file")

guild_id = 304753061346410499 # Pamea's New Empire
channel_id = 315180082765496320 # Chalmun's Cantina

log = logging.getLogger(__name__)
discord.utils.setup_logging()
logging.getLogger("discord.player").setLevel(logging.ERROR) # Prevent log-spam caused by looping ffmpeg

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    log.info("logged in as %s", client.user)
    await tree.sync()
    game = discord.Game("groovy rhythms!")
    await client.change_presence(activity=game)
    guild = await client.fetch_guild(guild_id)
    cantina = await guild.fetch_channel(channel_id)
    voice = await cantina.connect()
    voice.play(discord.FFmpegPCMAudio("cantinabandloop.opus", before_options="-stream_loop -1"))

@tree.command(
    name = "ping",
    description = "pingpong",
    guild=discord.Object(id=guild_id))
async def ping(interaction):
    await interaction.response.send_message("pong")

client.run(private_key, log_handler=None)