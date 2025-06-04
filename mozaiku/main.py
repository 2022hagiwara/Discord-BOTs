
from discord.ext import commands

import discord
import cv2


TOKEN = ""

intents=discord.Intents.all()
bot = commands.Bot(command_prefix="/", case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print('ok')


@bot.command()
async def hello(ctx):
    """helloと返すコマンド"""
    await ctx.send(f"Hello {ctx.author.name}")

@bot.command()
async def mozaiku(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save("image/a.png")
            await ctx.message.delete()
            img = cv2.imread("image/a.png")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier("opencvF/haarcascade_frontalface_default.xml")
            face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
            def mosaic(src, ratio=0.1):
                small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
                return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
            def mosaic_area(src, x, y, width, height, ratio=0.1):
                dst = src.copy()
                dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
                return dst
            for (x, y, w, h) in face:
                img = mosaic_area(img, x,y,w,h)
            cv2.imwrite("image/a.png",img)
            await ctx.send(file=discord.File("image/a.png"))

bot.run(TOKEN)
