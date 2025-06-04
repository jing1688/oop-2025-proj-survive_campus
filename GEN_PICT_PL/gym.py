from PIL import Image, ImageDraw

# 參數
W, H = 64, 64
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# -- 主體建築 --
draw.rectangle([(8, 24), (56, 56)], fill=(90, 90, 100, 255), outline=(30, 30, 35, 255), width=2)
draw.rectangle([(6, 20), (58, 28)], fill=(70, 70, 80, 255), outline=(40, 40, 50, 255), width=2) # 屋頂
draw.rectangle([(28, 44), (36, 56)], fill=(210, 210, 220, 255), outline=(80, 80, 80, 255), width=2) # 門
draw.rectangle([(14, 32), (26, 52)], fill=(90, 200, 255, 255), outline=(40, 120, 180, 255), width=2) # 左窗
draw.rectangle([(38, 32), (50, 52)], fill=(90, 200, 255, 255), outline=(40, 120, 180, 255), width=2) # 右窗

# -- 屋頂啞鈴招牌 --
# 槓鈴桿
draw.rectangle([(22, 12), (42, 16)], fill=(60, 60, 60, 255))
# 左片
draw.rectangle([(16, 10), (22, 18)], fill=(180, 180, 180, 255))
# 右片
draw.rectangle([(42, 10), (48, 18)], fill=(180, 180, 180, 255))
# 重量片小亮點
draw.rectangle([(18, 12), (19, 13)], fill=(255,255,255,255))
draw.rectangle([(44, 12), (45, 13)], fill=(255,255,255,255))
# 槓鈴小頭
draw.rectangle([(15, 13), (16, 15)], fill=(120, 120, 120, 255))
draw.rectangle([(48, 13), (49, 15)], fill=(120, 120, 120, 255))

# 儲存
img.save("gym_pixel.png")
img.show()
