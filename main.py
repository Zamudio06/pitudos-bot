import youtube_dl
import pafy
import discord
import time
from webserver import keep_alive
from discord.ext import commands

bot = commands.Bot(command_prefix="%", description="Bot mamalon")


@bot.event
async def on_ready():
    print(f"{bot.user.name} esta listo.")


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []
        self.inside = False

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue = []

    async def check_queue(self, ctx):
        time.sleep(5)
        self.song_queue.pop(0)
        if len(self.song_queue) == 0:
            await ctx.send(embed=discord.Embed(title="Agregueme mas rolitas culo"))
        else:
            await self.play_song(ctx, self.song_queue[0])

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(
            {"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False,
                                                                 ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)),
                              after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send(embed=discord.Embed(title="Conectese a un chat de voz, culo"))

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()
        self.inside = True

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            self.inside = False
            await ctx.send(embed=discord.Embed(title="Hasta la proxima \nGracias por utilizarme, culo"))
            return await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send(embed=discord.Embed(title="Debes incluir una rola, culo"))

        if not self.inside:
            return await ctx.send(embed=discord.Embed(title="Error", description="Metame al chat de voz, culo"))

        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Estoy buscando tu rolita wei, esperate poquito")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Perdona, no encontre la rolita :c")

            song = result[0]

        queue_len = len(self.song_queue)

        if queue_len >= 10:
            return await ctx.send(
                "Solo puedo tener 10 rolitas")

        self.song_queue.append(song)

        if len(self.song_queue) == 1:
            await self.play_song(ctx, song)
            await ctx.send(f"Reproduciendo: {song}")
        else:
            return await ctx.send(
                f"Estoy reproduciendo una rolita, pero te pongo en mi colita ;) \n Posicion {queue_len + 1}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("Olvidaste agregar la rola")

        await ctx.send("Buscando tu rolita, esperame puto")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Resultados de '{song}':",
                              description="*Puedes copiar el URL y usarlo con #play*\n",
                              colour=discord.Colour.red())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Mostrando {amount} resultados.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):  # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("No hay rolitas en la cola")

        embed = discord.Embed(title="Cola", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("No estoy reproduciendo nada, pendejo")

        if ctx.author.voice is None:
            return await ctx.send("No estas en un canal wei")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("No se robe al bot, culero")

        skip = True

        if skip:
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("Estoy pausado puto")

        ctx.voice_client.pause()
        await ctx.send("Pausa")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Conecteme a un Chat de voz, culo")

        if not ctx.voice_client.is_paused():
            return await ctx.send("No estoy pausado, pendejo")

        ctx.voice_client.resume()
        await ctx.send("Resumiendo")


async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))


bot.loop.create_task(setup())
keep_alive()
bot.run('ODkzMzM2NjE0ODM3ODQ2MDM3.YVZ-jg.5vEMctEzZQFbriIBqECbjfnfVH4')