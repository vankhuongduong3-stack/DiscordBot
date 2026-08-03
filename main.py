
import discord
from discord.ext import commands
import random


import os

TOKEN = os.getenv("DISCORD_TOKE")

OWNER_ID = 1531882555664629861


intents = discord.Intents.default()

intents.message_content = True

intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


roast_mode = False




ROAST_LIST = [
    "ĐỊT MẸ THG ĐĨ SÚC VẬT CON MẸ M BỊ CHO NHÀ T CẮN NÁT LỒN R KÌA=))).",
    "tao đẩy bay mày vào cối xay người trong địa ngục cho nó nghiến nát cái thứ súc sinh chó đẻ mày nha con đĩ 👊😋",
    "ĐĨ MẸ MÀY MẶT MÀY NHƯ LỒN VỪA BỊ ĐỊT XONG Á=)))",
    "THẰNG ÓC LỒN MÀY SỐNG LÀM ĐỊT GÌ CHO XÃ HỘI????",
    "con mẹ m nghe tin m loạn luân vs bố m nên lấy dao cắt cổ tự tử r kìa con ngu =))",
    "con đĩ bố mày địt liệt cả tinh hoàn bắn nát cặc ra tinh mới đẻ được thằng mặt đĩ chó đẻ như mày hả thằng bất hiếu rách 😂🤣🤣👆👆",
    "thằng não chó súc sinh cụ tổ con đĩ mẹ mày bị chôn dưới 18 tầng địa ngục nè thằng bất hiếu chó đẻ vô dụng bất tài 😂😂🤣🤣",
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
    "con mẹ m nghe tin m loạn luân vs bố m nên lấy dao cắt cổ tự tử r kìa con ngu =))",
    "mồ côi không cha không mẹ sủa tiếng của con mẹ nó trước khi chết đã để lại cho nó =))=))",
    "ĐỤ BÀ NỘI MÀY TỪ XƯA ĐẾN NAY.",
    "ĐỊT MẸ THẰNG ĐĨ SÚC VẬT CON MẸ M BỊ TAO ĐỤ NÁT LỒN RỒI MÀ CÒN GÁY HẢ???",
    "TAO ĐẨY MÀY VÀO CỐI XAY NGƯỜI ĐỊA NGỤC NGHIẾN NÁT XƯƠNG THỊT MÀY THÀNH BỘT!!!",
    "ĐĨ MẸ MÀY MẶT MÀY NHƯ LỒN VỪA BỊ 10 THẰNG ĐỤ XONG RÒN RỎ NƯỚC=)))",
    "THẰNG ÓC LỒN MÀY SỐNG CHỈ ĐỂ LÀM TỔI LỖI CHO XÃ HỘI, CHẾT MẸ ĐI!!!",
    "CON MẸ M BỊ TAO ĐỤ ĐẾN MÁU ÂM ĐẠO PHUN RA MÀ VẪN CHƯA CHẾT HẢ THẰNG CHÓ???",
    "THẰNG BẤT HIẾU CHÓ ĐẺ, BỐ MÀY ĐANG BỊ TAO BẮT HỒN LÊN ĐÁNH ĐẬP LIÊN HOÀN Ở ÂM PHỦ!!!",
    "ĐĨ MẸ MÀY TỰ CẮT CỔ VÌ NHỤC NHÃ KHI SINH RA ĐƯỢC MÀY=)))",
    "TAO ĐỤ CON MẸ M ĐẾN NÁT RUỘT RỒI ĐẨY NÓ XUỐNG ĐỊA NGỤC LÀM NÔ LỆ TÌNH DỤC!!!",
    "THẰNG SÚC SINH, TAO SẼ XÉO LỒN MẸ MÀY RA RỒI NHỒI CỨT VÀO=)))",
    "CẢ DÒNG HỌ MÀY SẼ BỊ TAO ĐỊT ĐẾN TỰ TỬ HẾT MỚI THÔI!!!",
    "MÀY LÀ SẢN PHẨM LỖI TỪ LẦN ĐỤ NHẦM CỦA BỐ MÀY VỚI CON CHÓ!!!",
    "TAO ĐẨY HỒN MÀY XUỐNG 18 TẦNG ĐỊA NGỤC ĐỂ BỊ QUỶ ĐỤ LIÊN TỤC 1000 NĂM!!!",
    "ĐĨ MẸ MÀY BỊ TAO ĐỤ ĐẾN LỒN BỊ XÉ TOANG MÀ VẪN KÊU ÍT=)))",
    "THẰNG KHỐN NẠN, CHA DƯỢNG MÀY BỊ TAO SÚT VỠ HỘP SỌ RỒI VÔ ĐỊA NGỤC!!!",
    "CON MẸ M ĐANG LÀM MA DA VÌ BỊ TAO ĐỤ QUÁ MẠNH=)))",
    "THẰNG ÓC CỨT, TAO SẼ BẮT MÀY ĂN CỨT CỦA CHÍNH MẸ MÀY!!!",
    "ĐỤ MẸ MÀY ĐẾN NÁT BỤNG ĐẺ RA ĐƯỢC THẰNG ĐẦN ĐỘN NHƯ MÀY!!!",
    "TAO SẼ ĐỐT SỐNG MÀY RỒI ĐÁNH THỨC DẬY ĐỂ ĐỤ TIẾP!!!",
    "MẶT MÀY NHƯ LỒN GIÀ BỊ 100 THẰNG XỎ QUE=)))",
    "THẰNG BẤT HIẾU, MẸ MÀY ĐANG KHÓC DƯỚI ÂM PHỦ VÌ SINH RA MÀY!!!",
    "TAO ĐỤ HẾT PHỤ NỮ NHÀ MÀY RỒI BẮT HỌ TỰ TỬ TRƯỚC MẶT MÀY!!!",
    "ĐĨ MẸ MÀY BỊ TAO DÙNG DAO CẮT LỒN RỒI NHỒI TIÊU=)))",
    "THẰNG CHÓ ĐẺ VÔ DỤNG, TAO SẼ LÀM MÀY CHẾT TRONG ĐAU ĐỚN DÀI DÀI!!!",
    "CON MẸ M BỊ BỐ MÀY BÁN CHO ĐÀN ÔNG ĐỤ ĐẾN CHẾT=)))",
    "TAO SẼ XÉ XÁC MÀY THÀNH 1000 MẢNH RỒI VỨT XUỐNG SÔNG!!!",
    "THẰNG SÚC VẬT, KIẾP SAU MÀY LÀM CON GIUN BỊ QUỶ ĐỤ!!!",
    "ĐỤ MẸ MÀY ĐẾN MÁU CHẢY RỒI VẪN KHÔNG DỪNG=)))",
    "MÀY LÀ ĐỒ TỐN ĐẤT, TAO MUỐN ĐÁP VỠ SỌ MÀY BẰNG BÚA!!!",
    "THẰNG NAO CHÓ, BỐ MÀY ĐANG BỊ TAO BẮT LÀM NÔ LỆ TÌNH DỤC Ở ĐỊA NGỤC!!!",
    "ĐĨ MẸ MÀY TỰ THẮT CỔ VÌ XẤU HỔ KHI CÓ MÀY!!!",
    "TAO SẼ ĐỤ LỒN MẸ MÀY ĐẾN NÁT RỒI DÙNG NÓ LÀM KHĂN LAU CẶC!!!",
    "THẰNG KHỐN KIẾP, CẢ NHÀ MÀY SẼ BỊ TAO NGUYỀN RỦA ĐẾN HẾT ĐỜI!!!",
    "MẶT MÀY NHƯ CẶC BỊ CHẶT ĐỨT=)))",
    "TAO ĐẨY MÀY VÀO LÒ THIÊU SỐNG RỒI NGHE MÀY KÊU LA!!!",
    "ĐĨ MẸ MÀY BỊ ĐỤ ĐẾN PHẢI ĂN CỨT ĐỂ SỐNG!!!",
    "THẰNG VÔ DỤNG, TAO SẼ LÀM MÀY CHẾT MÀ KHÔNG CÓ AI KHÓC!!!",
    "CON MẸ M ĐANG BỊ QUỶ DÙNG CỤ TRA TẤN TÌNH DỤC VĨNH VIỄN!!!",
    "TAO MUỐN CẮT CẶC MÀY RA RỒI NHỒI VÀO MIỆNG MÀY!!!",
    "THẰNG CHÓ NGU, MÀY CHỈ ĐÁNG BỊ ĐÁP VÀO ĐẦU!!!",
    "ĐỤ TỔ TIÊN MÀY TỪNG ĐỜI ĐẾN NÁT BỤNG=)))",
    "MÀY LÀ THỨ RÁC THẢI ĐỘC HẠI, TAO MUỐN ĐỐT SỐNG MÀY!!!",
    "THẰNG BỆNH HOẠN, TAO SẼ LÀM MẸ MÀY PHẢI XEM TAO ĐỤ MÀY!!!",
    "ĐĨ MẸ MÀY BỊ TAO ĐỤ ĐẾN LỒN BỊ THỦNG=)))",
    "TAO SẼ BẮT HỒN CẢ NHÀ MÀY XUỐNG ĐỊA NGỤC LÀM ĐỒ CHƠI TÌNH DỤC!!!",
    "THẰNG ÓC LỒN, MÀY SỐNG CHỈ ĐỂ BỊ CHẾT NHỤC NHÃ!!!",
    "CON MẸ M TỰ CẮT CỔ VÌ KHÔNG CHỊU NỔI KHI SINH RA MÀY!!!",
    "TAO ĐỤ MẸ MÀY ĐẾN NÁT RUỘT RỒI VỨT XÁC VÀO RỪNG!!!",
    "THẰNG ĐÁNG GHÉT, TAO SẼ LÀM MÀY ĂN PHÂN CỦA CHÍNH MÌNH!!!",
    "MẶT MÀY NHƯ LỒN BỊ ĐÁNH BẰNG GẬY=)))",
    "TAO NGUYỀN MÀY CHẾT TRONG ĐAU ĐỚN VÀ CÔ ĐƠN!!!",
    "ĐĨ MẸ MÀY BỊ TAO DÙNG DAO KÉO LỒN DÀI=)))",
    "THẰNG SÚC SINH, BỐ MÀY ĐANG QUỲ LIỆM CẶC QUỶ Ở ĐỊA NGỤC!!!",
    "TAO SẼ XÉO MẮT MÀY RỒI ÉP MÀY NHÌN TAO ĐỤ MẸ MÀY!!!",
    "MÀY LÀ ĐỒ TẠI HẠI, CẢ DÒNG HỌ MÀY SẼ BỊ DIỆT!!!",
    "THẰNG NAO NGẮN, TAO MUỐN ĐÁP VỠ HỘP SỌ MÀY!!!",
    "ĐỤ MẸ MÀY ĐẾN CHẢY MÁU LIÊN TỤC=)))",
    "TAO SẼ LÀM MÀY SỐNG MÀ KHÔNG CÓ LỖI THOÁT!!!",
    "CON ĐĨ HOANG, MẸ MÀY ĐANG BỊ TRA TẤN VĨNH VIỄN!!!",
    "THẰNG KHỐN NẠN NHẤT HÀNH TINH, CHẾT MẸ ĐI!!!",
    "TAO ĐỤ HẾT HỌ NHÀ MÀY RỒI BẮT TỰ TỬ HẾT!!!",
    "MẶT MÀY NHƯ CỨT NGƯỜI VỪA ĐIỀU=)))",
    "THẰNG VÔ HỒN, TAO SẼ LÀM MÀY HỐI HẬN KHI SINH RA!!!",
    "ĐĨ MẸ MÀY BỊ ĐỤ ĐẾN PHẢI LÀM ĐỒ CHƠI TÌNH DỤC!!!",
    "TAO MUỐN CẮT CỔ MÀY RỒI DÙNG MÁU MÀY TẮM!!!",
    "THẰNG CHÓ ĐẺ BẤT HIẾU, CẢ NHÀ MÀY SẼ CHẾT THẢM!!!",
    "MÀY CHỈ ĐÁNG BỊ QUỶ DÙNG LÀM NÔ LỆ TÌNH DỤC!!!",
    "ĐỤ MẸ MÀY TỪ TRONG QUÁ KHỨ ĐẾN TƯƠNG LAI=)))",
    "TAO SẼ ĐỐT NHÀ MÀY RỒI NHỐT CẢ NHÀ VÀO!!!",
    "THẰNG RÁC RƯỞI, MÀY SỐNG LÀ TỘI LỖI!!!",
    "CON MẸ M ĐANG KHÓC DƯỚI ĐỊA NGỤC VÌ MÀY!!!",
    "TAO SẼ XÉ LỒN MẸ MÀY RA LÀM HAI MIẾNG!!!",
    "THẰNG ĐẦN ĐỘN, TAO MUỐN ĐÁP MÀY VỠ MẶT!!!",
    "ĐĨ MẸ MÀY BỊ TAO ĐỤ ĐẾN MẤT TRÍ=)))",
    "MÀY LÀ THỨ TỐN ĐẤT, CHẾT ĐI CHO RỒI!!!",
    "TAO NGUYỀN MÀY BỊ ĐỤ ĐẾN CHẾT TRONG ĐAU ĐỚN!!!",
    "THẰNG ÓC CỨT, CẢ DÒNG HỌ MÀY SẼ BỊ DIỆT!!!",
    "ĐỤ BÀ NỘI MÀY ĐẾN NÁT BỤNG=)))",
    "TAO SẼ LÀM MÀY ĂN PHÂN VÀ UỐNG NƯỚC TIỂU!!!",
    "MẶT MÀY NHƯ LỒN BỊ XÉ TOANG=)))",
    "THẰNG KHỐN KIẾP, MÀY SẼ CHẾT MỘT CÁCH NHỤC NHÃ!!!",
    "TAO ĐẨY MÀY XUỐNG ĐỊA NGỤC LÀM ĐỒ CHƠI CHO QUỶ!!!",
    "ĐĨ MẸ MÀY BỊ ĐỤ LIÊN TỤC KHÔNG NGỪNG=)))",
    "THẰNG VÔ DỤNG, TAO MUỐN THẤY MÀY CHẾT!!!",
    "CON MẸ M TỰ TỬ VÌ KHÔNG CHỊU ĐỰNG NỔI MÀY!!!",
    "TAO SẼ ĐÁP VỠ TOÀN BỘ XƯƠNG CỦA MÀY!!!",
    "THẰNG SÚC VẬT, MÀY KHÔNG ĐÁNG SỐNG!!!",
    "ĐỤ HẾT TỔ TIÊN MÀY=)))",
    "TAO MUỐN LÀM MÀY ĐAU ĐỚN ĐẾN MỨC CẦU XIN CHẾT!!!",
    "MẶT MÀY NHƯ CẶC BỊ THỐI=)))",
    "THẰNG BẤT HIẾU CHÓ ĐẺ, CHẾT MẸ ĐI!!!",
    "TAO SẼ LÀM CẢ NHÀ MÀY PHẢI QUỲ LIỆM CẶC TAO!!!",
    "ĐĨ MẸ MÀY BỊ TAO DÙNG LÀM ĐỒ CHƠI=)))",
    "THẰNG NAO LỒN, MÀY SỐNG CHỈ ĐỂ BỊ CHỬI!!!",
    "TAO NGUYỀN MÀY BỊ ĐỊA NGỤC TRA TẤN VĨNH VIỄN!!!",
    "CON MẸ M ĐANG BỊ QUỶ ĐỤ ĐẾN RÁCH LỒN!!!",
    "THẰNG KHỐN NẠN NHẤT, TAO MUỐN MÀY BIẾN MẤT!!!",
    "ĐỤ MẸ MÀY ĐẾN NÁT HẾT=)))",
    "MÀY LÀ ĐỒ TẠI HẠI, CHẾT ĐI CHO XÃ HỘI THOÁT!!!",
    "TAO SẼ LÀM MÀY HỐI HẬN KHI ĐÃ SINH RA!!!",
    "ĐỊT MẸ MÀY THẰNG ĐĨ SÚC VẬT KHỐN NẠN NHẤT QUẢ ĐẤT, CHẾT MẸ ĐI CHO RỒI!!!"
]




@bot.event
async def on_ready():

    print(
        f"✅ Bot đã online: {bot.user}"
    )



@bot.command()
async def ping(ctx):

    await ctx.send(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )



@bot.command()
async def helpbot(ctx):

    await ctx.send(
"""
🤖 DANH SÁCH LỆNH

🏓 !ping
→ Kiểm tra bot

🔥 !roastmode
→ Bật/tắt chế độ roast

📜 !helpbot
→ Xem lệnh
"""
    )



@bot.command()
async def roastmode(ctx):

    global roast_mode


    if ctx.author.id != OWNER_ID:

        await ctx.send(
            "❌ Bạn không có quyền bật chế độ này!"
        )

        return



    roast_mode = not roast_mode


    if roast_mode:

        await ctx.send(
            "🔥 Đã bật chế độ AUTO ROAST!"
        )

    else:

        await ctx.send(
            "🛑 Đã tắt chế độ AUTO ROAST!"
        )



@bot.event
async def on_message(message):

    global roast_mode


    if message.author == bot.user:

        return



    if roast_mode:

        await message.channel.send(
            random.choice(ROAST_LIST)
        )



    await bot.process_commands(message)



bot.run(TOKEN)
