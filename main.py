import os
import random
import discord
from discord.ext import commands
import aiohttp

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = 1531882555664629861
ROAST_URL = "https://raw.githubusercontent.com/vankhuongduong3-stack/DiscordBot/main/cau_chui.txt"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

roast_mode = False
roast_list = []

async def load_roasts():
    global roast_list
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ROAST_URL) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    roast_list = [line.strip() for line in text.splitlines() if line.strip()]
                else:
                    roast_list = ["Mày ngu vãi", "Đồ óc chó", "Ngu như bò"]
    except:
        roast_list = ["Mày ngu vãi", "Đồ óc chó", "Ngu như bò"]

@bot.event
async def on_ready():
    await load_roasts()
    print(f"✅ Bot online: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def cuu(ctx):
    embed = discord.Embed(
        title="🆘 DANH SÁCH LỆNH CỨU RỖI",
        description="Dùng !cuu để hiển thị trợ giúp này",
        color=0x00ff88
    )
    embed.add_field(name="!ping", value="Kiểm tra độ trễ bot", inline=False)
    embed.add_field(name="!roastmode", value="Bật/tắt auto roast (chỉ owner)", inline=False)
    embed.add_field(name="!spam @user", value="Chửi + tag người dùng", inline=False)
    embed.add_field(name="!reload", value="Tải lại danh sách chửi từ GitHub (owner)", inline=False)
    embed.set_footer(text="Made with ❤️")
    await ctx.send(embed=embed)

@bot.command()
async def reload(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    await load_roasts()
    await ctx.send(f"✅ Đã tải lại {len(roast_list)} câu chửi từ GitHub!")

@bot.command()
async def roastmode(ctx):
    global roast_mode
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    roast_mode = not roast_mode
    await ctx.send(f"🔥 Chế độ auto roast: {'BẬT' if roast_mode else 'TẮT'}")

@bot.command()
async def spam(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("❌ Cần tag người dùng! Ví dụ: !spam @user")
        return
    if not roast_list:
        await ctx.send("❌ Chưa có câu chửi nào, dùng !reload để tải")
        return
    insult = random.choice(roast_list)
    await ctx.send(f"{insult} {member.mention}")

@spam.error
async def spam_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Cần tag người dùng! Ví dụ: !spam @user")

@bot.event
async def on_message(message):
    global roast_mode
    if message.author == bot.user:
        return
    if roast_mode and not message.content.startswith(bot.command_prefix):
        if roast_list:
            await message.channel.send(random.choice(roast_list))
    await bot.process_commands(message)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Chưa cấu hình DISCORD_TOKEN!")
