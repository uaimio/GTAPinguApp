#!.venv/bin/python3
# -*- coding: utf-8 -*-

# bot.py

"""
GTAPinguApp, bot del canale Discord GTA PINGU.

@author: uaimio
"""

import discord
from discord import app_commands

import asyncio
import json
import yt_dlp 

from random import randint, choice
from time import localtime, strftime

########################## AUDIO CLASS DEFINITION #######################
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_settings = json.load(open('settings/ytdl_format_options.json'))

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_settings)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.2):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, volume, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data, volume=volume)

########################## CONSTANTS DEFINITION #########################

CONSTANTS = json.load(open("settings/constants.json"))

# GTAPinguApp Id
MY_GUILD = discord.Object(id=CONSTANTS.get("MY_GUILD_ID"))

########################## CLIENT CLASS DEFINITION ######################
class CustomCommandTree(discord.app_commands.CommandTree):
    def __init__(self, client: discord.Client, *, fallback_to_global: bool = True):
        super().__init__(client, fallback_to_global=fallback_to_global)

    global CONSTANTS
    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.channel_id != CONSTANTS.get("CHANNEL_ID"):
            await interaction.response.send_message('I comandi vanno scritti nel canale apposito.', ephemeral=True)
            return False
        elif interaction.channel_id == CONSTANTS.get("CHANNEL_ID"):
            return True
        

class GTAPinguAppBot(discord.Client):
    """ GTAPinguAppBot implementation of a discord Client. """

    def __init__(self, *, intents: discord.Intents, **options) -> None:
        super().__init__(intents=intents, **options)
        self.volume = 30.0
        self.tree = CustomCommandTree(self)
        self.morio_cho_playing = None

    async def play_morio_cho(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """ Task for Morio-Cho play """
        await self.wait_until_ready()
        global CONSTANTS
        CONSTANTS['MORIO_CHO_DAILY_DONE'] = True

        await asyncio.sleep(5)
        mentions = ', '.join([user.mention for user in after.channel.members])
        await member.guild.text_channels[3].send(f'{mentions} Good morning Morioh Cho!')
        
        voice_client = await after.channel.connect() if not client.voice_clients else client.voice_clients[0]
        if voice_client.is_playing():
            voice_client.stop()

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('media/good_morning_morioh_cho.mp3'))
        voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        await asyncio.sleep(15)
        await self.voice_clients.pop().disconnect()

    async def setup_hook(self):

        # this copies the global commands over to your guild
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

        # create the background task and run it in the background
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord! ID: {self.user.id}.')
        await self.change_presence(activity=discord.Game(name=choice(CONSTANTS.get("ACTIVITIES"))))

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """ Voice event handler """

        # automatic disconnect the bot if it's alone in a voice channel
        if self.voice_clients and self.voice_clients[0].channel.members == [self.user]:
            await self.voice_clients.pop().disconnect()
            return

        # return if the update refers to the bot itself
        if self.user.id == member._user.id:
            return
        
        global CONSTANTS
        # random autokick from a voice channel
        if member.id in CONSTANTS.get("USER_AUTOKICK") and after.channel is not None:
            if randint(100, 105) == 104:
                await member.move_to(None)
                await member.guild.text_channels[3].send(f'{member.mention} SEI STATO SCAMMATO DA PEPPINO \'O MALAVITOSO',
                    allowed_mentions=discord.AllowedMentions(everyone=True, users=True, roles=True))
                
            return

        # play a good morning if it has not been already done and if it is enabled
        if before.channel is None and after.channel is not None and not CONSTANTS.get("MORIO_CHO_DAILY_DONE") and CONSTANTS.get("MORIO_CHO_ACTIVATION_STATUS"):
            hour = int(strftime("%H", localtime()))
            # do it only between 6 AM to 12 AM
            if hour >= 6 and hour < 12:
                self.morio_cho_playing = self.loop.create_task(self.play_morio_cho(member, before, after))
                await self.morio_cho_playing
            
            return
        
    async def on_message(self, message):
        pass


########################## CLIENT AND BASIC COMMANDS DEFINITION ##########################

intents = discord.Intents.default()
intents.message_content = True
client = GTAPinguAppBot(intents=intents)

@client.tree.command()
async def help(interaction: discord.Interaction):
    """ Funziona? """
    if interaction.channel_id == CONSTANTS.get("CHANNEL_ID"):
        await interaction.response.send_message(f'Peffò')
        

@client.tree.command()
async def pls(interaction: discord.Interaction):
    """ Nice ____? """
    if interaction.channel_id == CONSTANTS.get("CHANNEL_ID"):
        await interaction.response.send_message(eval(CRYPTOSTRING))


@client.tree.command()
async def buondi(interaction: discord.Interaction):
    """ Sognando un'intervista così. """
    await interaction.response.send_message(f'https://www.youtube.com/watch?v=E3EsZodN4MI')


@client.tree.command()
async def insegnaci(interaction: discord.Interaction):
    await interaction.response.send_message(f'https://www.youtube.com/watch?v=J4XqW26X3qc')


@client.tree.command()
async def diciotto(interaction: discord.Interaction):
    await interaction.response.send_message(f'https://www.youtube.com/watch?v=_IXfPxe7j6o')

@client.tree.command()
async def statusmoriocho(interaction: discord.Interaction):
    """ Indica lo stato (attivo o non attivo) di Good Morning Morio Cho """
    global CONSTANTS
    await interaction.response.send_message(f'Good morning Morio-Cho {"è attivo" if CONSTANTS.get("MORIO_CHO_ACTIVATION_STATUS") else "non è attivo"}')

@client.tree.command()
async def togglemoriocho(interaction: discord.Interaction):
    """ Attiva e disattiva Good Morning Morio Cho """
    global CONSTANTS
    await interaction.response.send_message(f'Good morning Morio-Cho ora è {"attivo" if CONSTANTS.get("MORIO_CHO_ACTIVATION_STATUS") else "non attivo"}')

@client.tree.command()
async def skin(interaction: discord.Interaction):
    """ La prova che cerchi. """
    await interaction.response.send_message('', file=discord.File('media/male01.png'))


########################## VOICE COMMANDS DEFINITION ################################


@client.tree.command()
@app_commands.describe(url='URL della canzone', volume='volume del bot con valori da 1 a 100')
async def play(interaction: discord.Interaction, url: str, volume: str = ''):
    """ Suona la musica! """
    if volume:
        try:
            client.volume = float(volume)
        except ValueError:
            await interaction.response.send_message('Valore del volume non valido.')
            return

    if not 1 <= client.volume <= 100: # volume < 0.1 or volume > 1:
        await interaction.response.send_message('Valore del volume non compreso tra 1 e 100.')

    elif not interaction.user.voice:
        await interaction.response.send_message('Non sei connesso ad un canale vocale.')

    elif client.voice_clients and client.voice_clients[0].channel != interaction.user.voice.channel:
        await interaction.response.send_message('Il bot è già attivo in un altro canale vocale.')

    elif client.morio_cho_playing is not None and not client.morio_cho_playing.done():
        await interaction.response.send_message('Non è possibile riprodurre ora.')

    else:
        await interaction.response.defer(ephemeral=False, thinking=True)
        player = await YTDLSource.from_url(url, volume=client.volume/100, loop=client.loop, stream=False)

        voice_client = await interaction.user.voice.channel.connect() if not client.voice_clients else client.voice_clients[0]
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.followup.send(f'In riproduzione {player.title}\nhttps://youtu.be/{player.data.get("id")}')


@client.tree.command()
@app_commands.describe(volume='volume del bot con valori tra 1 e 100')
async def volume(interaction: discord.Interaction, volume: str):
    """ Setta il volume della musica! """
    try:
        client.volume = float(volume)
    except ValueError:
        await interaction.response.send_message('Valore del volume non valido.')
        return
    
    if not 1 <= client.volume <= 100: # volume < 0.1 or volume > 1:
        await interaction.response.send_message('Valore del volume non compreso tra 1 e 100.')
    
    elif not interaction.user.voice:
        await interaction.response.send_message('Non sei connesso ad un canale vocale.')

    elif not client.voice_clients:
        await interaction.response.send_message('Il bot non è connesso ad alcun canale vocale.')

    elif client.voice_clients[0].channel == interaction.user.voice.channel:  # and client.voice_clients[0].is_playing():
        client.voice_clients[0].source.volume = client.volume / 100
        await interaction.response.send_message(f'Volume della musica settato a {client.volume:0.0f}!')


@client.tree.command()
async def pause(interaction: discord.Interaction):
    """ Mette in pausa la musica! """
    if interaction.user.voice is None:
        await interaction.response.send_message('Non sei connesso ad un canale vocale.')

    elif not client.voice_clients:
        await interaction.response.send_message('Il bot non è connesso ad alcun canale vocale.')

    elif client.voice_clients[0].channel == interaction.user.voice.channel and client.voice_clients[0].is_playing():
        client.voice_clients[0].pause()
        await interaction.response.send_message('Musica messa in pausa!')


@client.tree.command()
async def resume(interaction: discord.Interaction):
    """ Riparte la musica! """
    if interaction.user.voice is None:
        await interaction.response.send_message('Non sei connesso ad un canale vocale.')

    elif not interaction.client.voice_clients:
        await interaction.response.send_message('Il bot non è connesso ad alcun canale vocale.')

    elif interaction.client.voice_clients[0].channel == interaction.user.voice.channel and interaction.client.voice_clients[0].is_paused():
        interaction.client.voice_clients[0].resume()
        await interaction.response.send_message('Musica ripartita!')


@client.tree.command()
async def stop(interaction: discord.Interaction):
    """ Stoppa la musica e disconnette il bot! """
    if not interaction.client.voice_clients:
        await interaction.response.send_message('Il bot non è connesso ad alcun canale vocale.')
    else:
        await interaction.client.voice_clients.pop().disconnect()
        await interaction.response.send_message('Riproduzione interrotta!')

################################ DAILY SIGNAL HANDLER ###################################
def daily_operations_handler(signum, frame):
    print(signum)
    global CONSTANTS
    CONSTANTS["MORIO_CHO_DAILY_DONE"] = False

################################ TOKEN RETRIEVING AND RUN ###############################
if __name__ == '__main__':
    from os import getenv
    from base64 import b64decode

    TOKEN = getenv('GTPTOKEN')
    CRYPTOSTRING = b64decode(getenv('PLS_STRING')).decode() if getenv('PLS_STRING') is not None else None

    if TOKEN is not None and CRYPTOSTRING is not None:
        import signal
        signal.signal(signal.SIGUSR1, daily_operations_handler)

    else:
        try:
            local_settings = json.load(open('local_settings.json', 'r'))
            TOKEN = local_settings.get('GTPTOKEN')
            CRYPTOSTRING = b64decode(local_settings.get('PLS_STRING')).decode()
        except IOError as e:
            print("TOKEN E CRYPTOSTRING NON DEFINITE")
            print(e)
            exit(1)

    client.run(TOKEN)
    