from PIL import Image, ImageDraw

# 設定小畫布大小（像素風格）
canvas_size = (50, 50)
# 建立淺藍色天空背景
img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))

draw = ImageDraw.Draw(img)

# 畫建築物本體（淺棕色）
building_body = [10, 20, 40, 49]  # [左, 上, 右, 下]
draw.rectangle(building_body, fill=(210, 180, 140))  # Light Brown

# 畫窗戶（黃色小方格，每層 6px 間隔，窗戶大小 4x4）
for y in range(22, 48, 6):
    for x in range(12, 40, 6):
        window_rect = [x, y, x+4, y+4]
        draw.rectangle(window_rect, fill=(255, 255, 0))  # Yellow 窗戶

# 畫大門（深棕色）
door_rect = [22, 40, 28, 49]
draw.rectangle(door_rect, fill=(101, 67, 33))  # Brown 大門

# 畫屋頂（深褐色）
roof_rect = [8, 16, 42, 20]
draw.rectangle(roof_rect, fill=(139, 69, 19))  # Dark Brown 屋頂

# 放大像素風格（最近鄰插值）
pixel_scale = 3
big_size = (canvas_size[0] * pixel_scale, canvas_size[1] * pixel_scale)
big = img.resize(big_size, resample=Image.NEAREST)

# 顯示結果
big.save("A_building.png")
print("已產生建築物圖片 A_building.png")
