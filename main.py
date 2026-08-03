import os
import random
import discord
from discord.ext import commands
import aiohttp
import asyncio
import datetime
import json
import re
import math
from collections import defaultdict

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = 1531882555664629861
ROAST_URL = "https://raw.githubusercontent.com/vankhuongduong3-stack/DiscordBot/main/cau_chui.txt"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

roast_mode = False
roast_list = []
afk_users = {}
snipe_data = {}
command_usage = defaultdict(int)
bot_start_time = datetime.datetime.now()
warns = defaultdict(list)
user_levels = defaultdict(int)
user_xp = defaultdict(int)
daily_cooldown = {}

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

    if message.mentions:
        for user in message.mentions:
            if user.id in afk_users:
                await message.channel.send(f"⏳ {user.mention} đang AFK: {afk_users[user.id]}")

    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    command_usage[ctx.command.name] += 1

@bot.command()
async def bothelp(ctx):
    embed = discord.Embed(
        title="🤖 APEX BOT - DANH SÁCH LỆNH",
        description="Tổng hợp các lệnh tiện ích và giải trí",
        color=0x00ff88
    )
    embed.add_field(name="🛠️ CƠ BẢN", value="`!ping` - Độ trễ\n`!bothelp` - Trợ giúp\n`!uptime` - Thời gian hoạt động\n`!stats` - Thống kê bot", inline=False)
    embed.add_field(name="🔥 CHỬI & SPAM", value="`!spam @user [số lần]` - Chửi + tag (mặc định 1000)\n`!roastmode` - Bật/tắt auto roast (owner)\n`!reload` - Tải lại danh sách chửi (owner)", inline=False)
    embed.add_field(name="🎮 GIẢI TRÍ", value="`!8ball <câu hỏi>` - Bóng ma thuật\n`!flip` - Tung đồng xu\n`!roll` - Random 1-100\n`!rps <kéo/búa/bao>` - Oẳn tù tì\n`!meme` - Ảnh meme ngẫu nhiên", inline=False)
    embed.add_field(name="📁 TIỆN ÍCH", value="`!avatar @user` - Xem avatar\n`!serverinfo` - Thông tin server\n`!userinfo @user` - Thông tin user\n`!snipe` - Lấy tin nhắn bị xóa\n`!afk <lý do>` - Đặt AFK\n`!remind <time> <msg>` - Nhắc nhở\n`!poll <câu hỏi>` - Tạo poll\n`!slowmode <giây>` - Đặt slowmode", inline=False)
    embed.add_field(name="🔒 ADMIN (Owner)", value="`!clear <số>` - Xóa tin nhắn\n`!say <nội dung>` - Bot nói\n`!embed <title>|<desc>` - Gửi embed\n`!kick @user` - Kick\n`!ban @user` - Ban\n`!lock` - Khóa kênh\n`!unlock` - Mở khóa\n`!warn @user <lý do>` - Cảnh cáo\n`!warns @user` - Xem cảnh cáo", inline=False)
    embed.add_field(name="📊 HỆ THỐNG", value="`!level` - Xem level\n`!daily` - Nhận thưởng ngày\n`!profile @user` - Xem profile\n`!leaderboard` - Bảng xếp hạng", inline=False)
    embed.add_field(name="🌐 KHÁC", value="`!calc <biểu thức>` - Máy tính\n`!random <min> <max>` - Random số\n`!choose <a,b,c>` - Chọn ngẫu nhiên\n`!invite` - Link mời bot\n`!support` - Link hỗ trợ", inline=False)
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
async def spam(ctx, member: discord.Member = None, count: int = 1000):
    if not member:
        await ctx.send("❌ Cần tag người dùng! Ví dụ: !spam @user 500")
        return
    if count < 1:
        await ctx.send("❌ Số lần spam phải >= 1")
        return
    if count > 1000:
        await ctx.send("❌ Số lần spam tối đa là 1000!")
        return
    if not roast_list:
        await ctx.send("❌ Chưa có câu chửi nào, dùng !reload để tải")
        return

    await ctx.send(f"🔥 Bắt đầu spam {count} lần cho {member.mention}...")
    batch_size = 10
    for i in range(0, count, batch_size):
        batch = min(batch_size, count - i)
        for _ in range(batch):
            insult = random.choice(roast_list)
            await ctx.send(f"{insult} {member.mention}")
        await asyncio.sleep(1)

    await ctx.send(f"✅ Đã spam {count} lần cho {member.mention}!")

@spam.error
async def spam_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("❌ Lỗi cú pháp: !spam @user [số lần]")

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
async def poll(ctx, *, question):
    if not question:
        await ctx.send("❌ Vui lòng nhập câu hỏi.")
        return
    embed = discord.Embed(title="📊 POLL", description=question, color=0x00ffaa)
    embed.set_footer(text=f"Được tạo bởi {ctx.author.display_name}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("🤷")

@bot.command()
async def slowmode(ctx, seconds: int = 0):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    if seconds < 0:
        await ctx.send("❌ Số giây phải >= 0")
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"✅ Đã đặt slowmode thành {seconds} giây.")

@bot.command()
async def lock(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kênh đã bị khóa.")

@bot.command()
async def unlock(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kênh đã được mở khóa.")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    if member == ctx.author:
        await ctx.send("❌ Không thể kick chính mình!")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ Đã kick {member.mention} với lý do: {reason or 'Không có lý do'}")
    except discord.Forbidden:
        await ctx.send("❌ Bot không có quyền kick thành viên này.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    if member == ctx.author:
        await ctx.send("❌ Không thể ban chính mình!")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ Đã ban {member.mention} với lý do: {reason or 'Không có lý do'}")
    except discord.Forbidden:
        await ctx.send("❌ Bot không có quyền ban thành viên này.")

@bot.command()
async def warn(ctx, member: discord.Member, *, reason="Không có lý do"):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Không có quyền!")
        return
    warns[member.id].append({"reason": reason, "by": ctx.author.id, "time": datetime.datetime.now()})
    await ctx.send(f"⚠️ Đã cảnh cáo {member.mention} với lý do: {reason}")

@bot.command()
async def warns(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    data = warns.get(member.id, [])
    if not data:
        await ctx.send(f"📭 {member.mention} không có cảnh cáo nào.")
        return
    embed = discord.Embed(title=f"⚠️ Cảnh cáo của {member.display_name}", color=0xffaa00)
    for i, w in enumerate(data, 1):
        embed.add_field(name=f"Lần {i}", value=f"Lý do: {w['reason']}\nNgười cảnh cáo: <@{w['by']}>\nThời gian: {w['time'].strftime('%H:%M %d/%m/%Y')}", inline=False)
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
async def level(ctx):
    user = ctx.author
    xp = user_xp[user.id]
    level = user_levels[user.id]
    xp_needed = 100 * (level + 1)
    embed = discord.Embed(title=f"📊 Level của {user.display_name}", color=0x00ffaa)
    embed.add_field(name="Level", value=str(level), inline=True)
    embed.add_field(name="XP", value=f"{xp}/{xp_needed}", inline=True)
    embed.set_thumbnail(url=user.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def daily(ctx):
    if ctx.author.id in daily_cooldown:
        remaining = daily_cooldown[ctx.author.id] - datetime.datetime.now()
        if remaining.total_seconds() > 0:
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.send(f"⏳ Bạn đã nhận thưởng rồi, chờ {hours}h {minutes}m {seconds}s nữa!")
            return
    reward = random.randint(100, 500)
    user_xp[ctx.author.id] += reward
    user_levels[ctx.author.id] = math.floor(user_xp[ctx.author.id] / 100)
    daily_cooldown[ctx.author.id] = datetime.datetime.now() + datetime.timedelta(hours=24)
    await ctx.send(f"🎁 Bạn đã nhận {reward} XP! Tổng XP: {user_xp[ctx.author.id]}")

@bot.command()
async def profile(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    xp = user_xp[member.id]
    level = user_levels[member.id]
    embed = discord.Embed(title=f"👤 Profile của {member.display_name}", color=0x00aaff)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Level", value=str(level), inline=True)
    embed.add_field(name="XP", value=str(xp), inline=True)
    embed.add_field(name="Cảnh cáo", value=str(len(warns.get(member.id, []))), inline=True)
    embed.add_field(name="Ngày tham gia", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    sorted_users = sorted(user_xp.items(), key=lambda x: x[1], reverse=True)[:10]
    if not sorted_users:
        await ctx.send("📭 Chưa có dữ liệu leaderboard.")
        return
    embed = discord.Embed(title="🏆 Bảng xếp hạng XP", color=0x00ffaa)
    for i, (user_id, xp) in enumerate(sorted_users, 1):
        user = bot.get_user(user_id)
        if user:
            name = user.display_name
        else:
            name = f"User {user_id}"
        embed.add_field(name=f"#{i} {name}", value=f"Level {user_levels[user_id]} • {xp} XP", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def calc(ctx, *, expression):
    try:
        expression = re.sub(r'[^0-9+\-*/().%\s]', '', expression)
        result = eval(expression)
        await ctx.send(f"🧮 Kết quả: `{result}`")
    except Exception:
        await ctx.send("❌ Biểu thức không hợp lệ!")

@bot.command()
async def randomnum(ctx, min_num: int = 1, max_num: int = 100):
    if min_num > max_num:
        await ctx.send("❌ Số min phải nhỏ hơn số max.")
        return
    await ctx.send(f"🎲 Số ngẫu nhiên: **{random.randint(min_num, max_num)}**")

@bot.command()
async def choose(ctx, *, options):
    choices = [opt.strip() for opt in options.split(",")]
    if len(choices) < 2:
        await ctx.send("❌ Cần ít nhất 2 lựa chọn, phân cách bằng dấu phẩy.")
        return
    await ctx.send(f"🤔 Tôi chọn: **{random.choice(choices)}**")

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="📨 Mời bot APEX", description="Mời bot vào server của bạn!", color=0x00ff88)
    embed.add_field(name="Link mời", value="[Click để mời](https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def support(ctx):
    embed = discord.Embed(title="🆘 Hỗ trợ", description="Cần giúp đỡ? Liên hệ admin!", color=0x00aaff)
    embed.add_field(name="Server hỗ trợ", value="[Link Discord](https://discord.gg/your_server)", inline=False)
    await ctx.send(embed=embed)

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
