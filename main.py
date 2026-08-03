import os
import random
import discord
from discord.ext import commands
import aiohttp
import asyncio
import datetime
import json
import re

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = 1531882555664629861
ROAST_URL = "https://raw.githubusercontent.com/vankhuongduong3-stack/DiscordBot/main/cau_chui.txt"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

roast_mode = False
roast_list = []
afk_users = {}
snipe_data = {}
command_usage = {}
bot_start_time = datetime.datetime.now()

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
    print(f"✅ Bot online: {bot.user} (ID: {bot.user.id})")
    print(f"📅 Đã online từ: {bot_start_time.strftime('%H:%M:%S %d/%m/%Y')}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!bothelp | 🦾"))

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    snipe_data[message.channel.id] = {
        "author": message.author,
        "content": message.content,
        "deleted_at": datetime.datetime.now()
    }

@bot.event
async def on_message(message):
    global roast_mode
    if message.author == bot.user:
        return

    if roast_mode and not message.content.startswith(bot.command_prefix):
        if roast_list:
            await message.channel.send(random.choice(roast_list))

    await bot.process_commands(message)

@bot.command()
async def bothelp(ctx):
    embed = discord.Embed(
        title="🤖 APEX BOT - DANH SÁCH LỆNH",
        description="Tổng hợp các lệnh tiện ích và giải trí",
        color=0x00ff88
    )
    embed.add_field(name="🛠️ CƠ BẢN", value="`!ping` - Độ trễ\n`!bothelp` - Trợ giúp\n`!uptime` - Thời gian hoạt động\n`!stats` - Thống kê bot", inline=False)
    embed.add_field(name="🔥 CHỬI & SPAM", value="`!spam @user` - Chửi + tag\n`!roastmode` - Bật/tắt auto roast (owner)\n`!reload` - Tải lại danh sách chửi (owner)", inline=False)
    embed.add_field(name="🎮 GIẢI TRÍ", value="`!8ball <câu hỏi>` - Bóng ma thuật\n`!flip` - Tung đồng xu\n`!roll` - Random 1-100\n`!rps <kéo/búa/bao>` - Oẳn tù tì\n`!meme` - Ảnh meme ngẫu nhiên", inline=False)
    embed.add_field(name="📁 TIỆN ÍCH", value="`!avatar @user` - Xem avatar\n`!serverinfo` - Thông tin server\n`!userinfo @user` - Thông tin user\n`!snipe` - Lấy tin nhắn bị xóa gần nhất\n`!afk <lý do>` - Đặt trạng thái AFK\n`!remind <thời gian> <nội dung>` - Nhắc nhở (vd: !remind 10s test)", inline=False)
    embed.add_field(name="🔒 ADMIN (Owner)", value="`!clear <số>` - Xóa tin nhắn\n`!say <nội dung>` - Bot nói\n`!embed <title>|<desc>` - Gửi embed", inline=False)
    embed.set_footer(text=f"📦 {len(bot.commands)} lệnh • Chạy bởi APEX")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command()
async def uptime(ctx):
    delta = datetime.datetime.now() - bot_start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f"⏰ Bot đã hoạt động: `{hours}h {minutes}m {seconds}s`")

@bot.command()
async def stats(ctx):
    total_commands = sum(command_usage.values())
    embed = discord.Embed(title="📊 THỐNG KÊ BOT", color=0x00aaff)
    embed.add_field(name="📦 Tổng lệnh", value=str(len(bot.commands)), inline=True)
    embed.add_field(name="🔢 Lệnh đã dùng", value=str(total_commands), inline=True)
    embed.add_field(name="👥 Server", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="👤 Người dùng", value=str(len(bot.users)), inline=True)
    embed.add_field(name="📅 Thời gian chạy", value=f"{datetime.datetime.now() - bot_start_time}", inline=False)
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

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    embed = discord.Embed(title=f"Avatar của {member.display_name}", color=0x00aaff)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📋 Thông tin Server: {guild.name}", color=0x00ffaa)
    embed.add_field(name="👑 Chủ sở hữu", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 Thành viên", value=str(guild.member_count), inline=True)
    embed.add_field(name="📅 Ngày tạo", value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="📁 Kênh", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="🎭 Vai trò", value=str(len(guild.roles)), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    embed = discord.Embed(title=f"👤 Thông tin {member.display_name}", color=0x00aaff)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="📛 Tên", value=member.name, inline=True)
    embed.add_field(name="📅 Ngày tham gia", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="📅 Ngày tạo", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="🎭 Vai trò cao nhất", value=member.top_role.mention, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount: int = 5):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    if amount < 1:
        await ctx.send("❌ Số lượng phải lớn hơn 0")
        return
    deleted = await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🗑️ Đã xóa {len(deleted)-1} tin nhắn", delete_after=3)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("❌ Vui lòng nhập số lượng hợp lệ")

@bot.command()
async def say(ctx, *, content):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    await ctx.send(content)

@bot.command()
async def embed(ctx, *, args):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    try:
        title, desc = args.split("|", 1)
        embed = discord.Embed(title=title.strip(), description=desc.strip(), color=0x00ff88)
        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("❌ Cú pháp: !embed Tiêu đề | Nội dung")

@bot.command()
async def snipe(ctx):
    data = snipe_data.get(ctx.channel.id)
    if not data:
        await ctx.send("📭 Không có tin nhắn bị xóa nào.")
        return
    embed = discord.Embed(title="📌 Tin nhắn bị xóa", color=0xffaa00)
    embed.add_field(name="Người gửi", value=data["author"].mention, inline=False)
    embed.add_field(name="Nội dung", value=data["content"] or "Không có nội dung", inline=False)
    embed.set_footer(text=f"Xóa lúc {data['deleted_at'].strftime('%H:%M:%S %d/%m/%Y')}")
    await ctx.send(embed=embed)

@bot.command()
async def afk(ctx, *, reason="Không có lý do"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"😴 {ctx.author.mention} đã đặt AFK: {reason}")

@bot.event
async def on_message_afk(message):
    if message.mentions:
        for user in message.mentions:
            if user.id in afk_users:
                await message.channel.send(f"⏳ {user.mention} đang AFK: {afk_users[user.id]}")

@bot.command()
async def remind(ctx, time_str, *, content):
    try:
        if time_str.endswith("s"):
            seconds = int(time_str[:-1])
        elif time_str.endswith("m"):
            seconds = int(time_str[:-1]) * 60
        elif time_str.endswith("h"):
            seconds = int(time_str[:-1]) * 3600
        else:
            seconds = int(time_str)
        if seconds <= 0:
            await ctx.send("❌ Thời gian phải lớn hơn 0")
            return
        await ctx.send(f"⏰ Đã đặt nhắc nhở: `{content}` trong `{seconds}` giây")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 {ctx.author.mention} Nhắc nhở: {content}")
    except ValueError:
        await ctx.send("❌ Thời gian không hợp lệ. Ví dụ: !remind 10s text")

@bot.command()
async def eightball(ctx, *, question):
    responses = ["Có", "Không", "Có thể", "Chắc chắn", "Không đời nào", "Hỏi lại sau", "Có lẽ", "Tôi không biết", "Chắc chắn rồi", "Đừng hy vọng"]
    await ctx.send(f"🎱 Câu hỏi: {question}\n📦 Trả lời: {random.choice(responses)}")

@bot.command()
async def flip(ctx):
    await ctx.send(f"🪙 Tung đồng xu: **{random.choice(['Mặt ngửa', 'Mặt sấp'])}**")

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 Con số của bạn: **{random.randint(1, 100)}**")

@bot.command()
async def rps(ctx, choice: str):
    choices = ["kéo", "búa", "bao"]
    if choice.lower() not in choices:
        await ctx.send("❌ Chọn: kéo, búa, bao")
        return
    bot_choice = random.choice(choices)
    result = ""
    if choice.lower() == bot_choice:
        result = "Hòa!"
    elif (choice.lower() == "kéo" and bot_choice == "bao") or \
         (choice.lower() == "búa" and bot_choice == "kéo") or \
         (choice.lower() == "bao" and bot_choice == "búa"):
        result = "Bạn thắng! 🎉"
    else:
        result = "Bạn thua! 😢"
    await ctx.send(f"🤖 Bot chọn: **{bot_choice}**\n{result}")

@bot.command()
async def meme(ctx):
    memes = [
        "https://i.pinimg.com/736x/61/45/8d/61458d8ccd8228fea72a9d684a54ae20.jpg",
        "https://i.pinimg.com/736x/f8/8c/21/f88c217a209ce109603f2f29c7d10221.jpg",
        "https://i.pinimg.com/736x/38/b1/98/38b198c64648b8fac98bc80397db28b9.jpg",
        "https://i.pinimg.com/736x/e5/89/5c/e5895c3f96e37e230e49e2f89885b7b6.jpg",
        "https://i.pinimg.com/736x/9e/47/b9/9e47b99eabb1eff14ac37e9d45f72cb4.jpg"
    ]
    await ctx.send(random.choice(memes))

if __name__ == "__main__":
    if TOKEN:
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ Token không hợp lệ! Kiểm tra lại DISCORD_TOKEN.")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    else:
        print("❌ Chưa cấu hình DISCORD_TOKEN!")
