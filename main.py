import os
import random
import discord
from discord.ext import commands

# Lấy Token từ biến môi trường (DISCORD_TOKEN)
TOKEN = os.getenv("DISCORD_TOKEN")

# ID quản trị viên
OWNER_ID = 1531882555664629861

# Khởi tạo Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None  # Tắt lệnh help mặc định của discord.py
)

# Biến trạng thái
roast_mode = False

# Danh sách tin nhắn
ROAST_LIST = [
    "ĐỊT MẸ THG ĐĨ SÚC VẬT CON MẸ M BỊ CHO NHÀ T CẮN NÁT LỒN R KÌA=))).",
    "tao đẩy bay mày vào cối xay người trong địa ngục cho nó nghiến nát cái thứ súc sinh chó đẻ mày nha con đĩ 👊😋",
    "ĐĨ MẸ MÀY MẶT MÀY NHƯ LỒN VỪA BỊ ĐỊT XONG Á=)))",
    "THẰNG ÓC LỒN MÀY SỐNG LÀM ĐỊT GÌ CHO XÃ HỘI????",
    "con mẹ m nghe tin m loạn luân vs bố m nên lấy dao cắt cổ tự tử r kìa con ngu =))",
    "con đĩ bố mày đụ liệt cả tinh hoàn bắn nát cặc ra tinh mới đẻ được thằng mặt đĩ chó đẻ như mày hả thằng bất hiếu rách 😂🤣🤣👆👆",
    "thằng脑chó súc sinh cụ tổ con đĩ mẹ mày bị chôn dưới 18 tầng địa ngục nè thằng bất hiếu chó đẻ vô dụng bất tài 😂😂🤣🤣",
    "t đụ con mẹ m đến mức con mẹ m hóa thành ma da nhảy xuống nước để rồi đéo siêu thoát được khỏi nhân gian =))",
    "thằng cha dượng m bị t sử dụng tuyệt kĩ liên hoàn cước t sút cho cha m xuống âm phủ quỳ lạy diêm vương tha mạng vì kiếp trước lỡ chém chết con gái mẹ á =))",
    "đĩ mẹ thk ngu bị anh chửi nhớ cha nhớ mẹ nhớ kiếp trước kìa😹😹😹",
    "Cha mày hóa thân thành hắc bạch vô thường cha mày bắt hồn đĩ mẹ mày xuống chầu diêm vương",
    "cả gia đình m bị t sỉ vả cho đến mức thắt cổ tự tử mà =))=))=))",
    "MẶT DÀY NHƯ LỒN MẸ MÀY=)))",
    "bố của mày là 1 con chó ngao tây tạng đó thằng óc chó 🫵😂",
    "ĐỊT MẸ THẰNG KHỐN NẠN ĐÁNG GHÉT.",
    "con mẹ m tái sinh chỉ để được t đụ tiếp vì t đụ quá phê =))",
    "tội nghiệp con chó hoang đang cố phản kháng trong vô vọng 🥺👌",
    "ĐĨ MẸ MÀY BỊ ĐA NGƯỜI ĐỤ=)))",
    "mồ côi không cha không mẹ sủa tiếng của con mẹ nó trước khi chết đã để lại cho nó =))=))",
    "ĐỤ BÀ NỘI MÀY TỪ XƯA ĐẾN NAY.",
    "TAO ĐẨY MÀY VÀO CỐI XAY NGƯỜI ĐỊA NGỤC NGHIẾN NÁT XƯƠNG THỊT MÀY THÀNH BỘT!!!",
    "THẰNG ÓC LỒN MÀY SỐNG CHỈ ĐỂ LÀM TỘI LỖI CHO XÃ HỘI, CHẾT MẸ ĐI!!!",
    "THẰNG BẤT HIẾU CHÓ ĐẺ, BỐ MÀY ĐANG BỊ TAO BẮT HỒN LÊN ĐÁNH ĐẬP LIÊN HOÀN Ở ÂM PHỦ!!!",
    "CẢ DÒNG HỌ MÀY SẼ BỊ TAO ĐỊT ĐẾN TỰ TỬ HẾT MỚI THÔI!!!",
    "TAO ĐẨY HỒN MÀY XUỐNG 18 TẦNG ĐỊA NGỤC ĐỂ BỊ QUỶ ĐỤ LIÊN TỤC 1000 NĂM!!!",
    "THẰNG KHỐN NẠN, CHA DƯỢNG MÀY BỊ TAO SÚT VỠ HỘP SỌ RỒI VÔ ĐỊA NGỤC!!!",
    "THẰNG ÓC CỨT, TAO SẼ BẮT MÀY ĂN CỨT CỦA CHÍNH MẸ MÀY!!!",
    "TAO SẼ ĐỐT SỐNG MÀY RỒI ĐÁNH THỨC DẬY ĐỂ ĐỤ TIẾP!!!",
    "THẰNG BẤT HIẾU, MẸ MÀY ĐANG KHÓC DƯỚI ÂM PHỦ VÌ SINH RA MÀY!!!",
    "THẰNG CHÓ ĐẺ VÔ DỤNG, TAO SẼ LÀM MÀY CHẾT TRONG ĐAU ĐỚN DÀI DÀI!!!",
    "TAO SẼ XÉ XÁC MÀY THÀNH 1000 MẢNH RỒI VỨT XUỐNG SÔNG!!!",
    "THẰNG SÚC VẬT, KIẾP SAU MÀY LÀM CON GIUN BỊ QUỶ ĐỤ!!!",
    "MÀY LÀ ĐỒ TỐN ĐẤT, TAO MUỐN ĐÁP VỠ SỌ MÀY BẰNG BÚA!!!",
    "THẰNG KHỐN KIẾP, CẢ NHÀ MÀY SẼ BỊ TAO NGUYỀN RỦA ĐẾN HẾT ĐỜI!!!",
    "TAO ĐẨY MÀY VÀO LÒ THIÊU SỐNG RỒI NGHE MÀY KÊU LA!!!",
    "THẰNG VÔ DỤNG, TAO SẼ LÀM MÀY CHẾT MÀ KHÔNG CÓ AI KHÓC!!!",
    "TAO MUỐN CẮT CẶC MÀY RA RỒI NHỒI VÀO MIỆNG MÀY!!!",
    "THẰNG CHÓ NGU, MÀY CHỈ ĐÁNG BỊ ĐÁP VÀO ĐẦU!!!",
    "MÀY LÀ THỨ RÁC THẢI ĐỘC HẠI, TAO MUỐN ĐỐT SỐNG MÀY!!!",
    "THẰNG ÓC LỒN, MÀY SỐNG CHỈ ĐỂ BỊ CHẾT NHỤC NHÃ!!!",
    "THẰNG ĐÁNG GHÉT, TAO SẼ LÀM MÀY ĂN PHÂN CỦA CHÍNH MÌNH!!!",
    "TAO NGUYỀN MÀY CHẾT TRONG ĐAU ĐỚN VÀ CÔ ĐƠN!!!",
    "MÀY LÀ ĐỒ TẠI HẠI, CẢ DÒNG HỌ MÀY SẼ BỊ DIỆT!!!",
    "THẰNG KHỐN NẠN NHẤT HÀNH TINH, CHẾT MẸ ĐI!!!",
    "THẰNG VÔ HỒN, TAO SẼ LÀM MÀY HỐI HẬN KHI SINH RA!!!",
    "THẰNG CHÓ ĐẺ BẤT HIẾU, CẢ NHÀ MÀY SẼ CHẾT THẢM!!!",
    "TAO SẼ ĐỐT NHÀ MÀY RỒI NHỐT CẢ NHÀ VÀO!!!",
    "THẰNG RÁC RƯỞI, MÀY SỐNG LÀ TỘI LỖI!!!",
    "THẰNG ĐẦN ĐỘN, TAO MUỐN ĐÁP MÀY VỠ MẶT!!!",
    "MÀY LÀ THỨ TỐN ĐẤT, CHẾT ĐI CHO RỒI!!!",
    "THẰNG ÓC CỨT, CẢ DÒNG HỌ MÀY SẼ BỊ DIỆT!!!",
    "TAO SẼ LÀM MÀY ĂN PHÂN VÀ UỐNG NƯỚC TIỂU!!!",
    "THẰNG KHỐN KIẾP, MÀY SẼ CHẾT MỘT CÁCH NHỤC NHÃ!!!",
    "TAO ĐẨY MÀY XUỐNG ĐỊA NGỤC LÀM ĐỒ CHƠI CHO QUỶ!!!",
    "THẰNG VÔ DỤNG, TAO MUỐN THẤY MÀY CHẾT!!!",
    "TAO SẼ ĐÁP VỠ TOÀN BỘ XƯƠNG CỦA MÀY!!!",
    "THẰNG SÚC VẬT, MÀY KHÔNG ĐÁNG SỐNG!!!",
    "TAO MUỐN LÀM MÀY ĐAU ĐỚN ĐẾN MỨC CẦU XIN CHẾT!!!",
    "THẰNG BẤT HIẾU CHÓ ĐẺ, CHẾT MẸ ĐI!!!",
    "THẰNG NAO LỒN, MÀY SỐNG CHỈ ĐỂ BỊ CHỬI!!!",
    "TAO NGUYỀN MÀY BỊ ĐỊA NGỤC TRA TẤN VĨNH VIỄN!!!",
    "THẰNG KHỐN NẠN NHẤT, TAO MUỐN MÀY BIẾN MẤT!!!",
    "MÀY LÀ ĐỒ TẠI HẠI, CHẾT ĐI CHO XÃ HỘI THOÁT!!!",
    "TAO SẼ LÀM MÀY HỐI HẬN KHI ĐÃ SINH RA!!!"
]


@bot.event
async def on_ready():
    print(f"✅ Bot đã online thành công dưới tên: {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def helpbot(ctx):
    embed_help = """
🤖 **DANH SÁCH LỆNH BOT**

🏓 `!ping` 
└ Kiểm tra độ độ trễ kết nối của bot

🔥 `!roastmode`
└ Bật hoặc tắt chế độ Auto Roast (Chỉ Chủ sở hữu)

📜 `!helpbot`
└ Hiển thị menu trợ giúp này
"""
    await ctx.send(embed_help)


@bot.command()
async def roastmode(ctx):
    global roast_mode

    # Kiểm tra quyền chủ sở hữu
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Bạn không có quyền sử dụng lệnh này!")
        return

    roast_mode = not roast_mode

    if roast_mode:
        await ctx.send("🔥 **Đã BẬT chế độ AUTO ROAST!**")
    else:
        await ctx.send("🛑 **Đã TẮT chế độ AUTO ROAST!**")


@bot.event
async def on_message(message):
    global roast_mode

    # Bỏ qua tin nhắn từ chính bot để tránh lặp vô hạn
    if message.author == bot.user:
        return

    # Nếu bật roast_mode và tin nhắn KHÔNG phải lệnh (không bắt đầu bằng !)
    if roast_mode and not message.content.startswith(bot.command_prefix):
        await message.channel.send(random.choice(ROAST_LIST))

    # Xử lý các lệnh prefix như bình thường
    await bot.process_commands(message)


# Khởi chạy bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Lỗi: Chưa cấu hình DISCORD_TOKEN trong Environment Variables!")
