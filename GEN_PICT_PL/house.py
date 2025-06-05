from PIL import Image, ImageDraw

# 建立 128x128 的透明畫布
size = (128, 128)
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 顏色定義
wall_color = (220, 220, 200, 255)    # 柔和米色牆
floor_color = (180, 140, 100, 255)   # 溫暖木地板
bed_frame = (139, 69, 19, 255)       # 深棕床架
bed_sheet = (240, 230, 255, 255)     # 淡紫床單
pillow_color = (255, 240, 245, 255)  # 奶油粉枕頭
blanket_color = (200, 180, 220, 255) # 淡紫毯子
desk_color = (139, 69, 19, 255)      # 栗棕書桌
chair_color = (124, 104, 84, 255)    # 暗灰椅子
bookshelf_color = (139, 69, 19, 255) # 栗棕書架
book_colors = [(200, 50, 50, 255), (50, 100, 200, 255), (50, 200, 100, 255)]
plant_pot = (150, 75, 0, 255)        # 瓷磚盆栽
plant_green = (50, 150, 50, 255)     # 綠色植物

# 畫牆與地板
draw.rectangle([(0, 0), (128, 80)], fill=wall_color)
draw.rectangle([(0, 80), (128, 128)], fill=floor_color)

# 畫床 (左側)，加粗床邊輪廓，讓床更明顯
bed_x0, bed_y0 = 12, 48
bed_x1, bed_y1 = 76, 96
# 床架：沿外框描邊先畫深棕輪廓，再畫床內
draw.rectangle([(bed_x0, bed_y0), (bed_x1, bed_y1)], fill=bed_frame)
# 床單範圍：稍縮小畫淡紫
draw.rectangle([(bed_x0 + 4, bed_y0 + 4), (bed_x1 - 4, bed_y1 - 4)], fill=bed_sheet)
# 毯子，折疊在床尾
draw.rectangle([(bed_x0 + 4, bed_y0 + 4), (bed_x1 - 4, bed_y0 + 20)], fill=blanket_color)
# 枕頭
draw.rectangle([(bed_x0 + 40, bed_y0 + 4), (bed_x1 - 4, bed_y0 + 20)], fill=pillow_color)

# 畫書桌與椅子 (右下)
draw.rectangle([(80, 72), (124, 96)], fill=desk_color)  # 桌面
draw.rectangle([(88, 96), (112, 112)], fill=chair_color) # 椅子

# 縮小書架 (右側牆上)
bookshelf_x0, bookshelf_y0 = 100, 8
bookshelf_x1, bookshelf_y1 = 120, 52  # 原高度 52，寬度 20
# 縮小為寬度 16, 高度 40
bookshelf_x0, bookshelf_y0 = 102, 12
bookshelf_x1, bookshelf_y1 = 118, 52
draw.rectangle([(bookshelf_x0, bookshelf_y0), (bookshelf_x1, bookshelf_y1)], fill=bookshelf_color)
# 書本，三本
for i, color in enumerate(book_colors):
    x0 = bookshelf_x0 + 2 + (i * 5)
    draw.rectangle([(x0, bookshelf_y0 + 4), (x0 + 4, bookshelf_y0 + 24)], fill=color)

# 畫盆栽 (書桌上)
draw.rectangle([(84, 56), (92, 64)], fill=plant_pot)
draw.ellipse([(80, 48), (96, 56)], fill=plant_green)

# 畫窗戶 (牆上左側)
draw.rectangle([(12, 10), (52, 40)], outline=(150, 150, 180, 255), width=2)
draw.rectangle([(14, 12), (36, 38)], fill=(180, 220, 240, 180))
draw.rectangle([(30, 12), (48, 38)], fill=(180, 220, 240, 180))
draw.line([(14, 24), (50, 24)], fill=(150, 150, 180, 255), width=1)
draw.line([(32, 12), (32, 38)], fill=(150, 150, 180, 255), width=1)

# 顯示圖像
img.save("house.png")
