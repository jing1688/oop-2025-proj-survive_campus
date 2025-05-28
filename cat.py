from PIL import Image, ImageDraw

# 建立60x60像素，透明背景
img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 主體顏色
body = (255, 204, 102, 255)
ear  = (230, 160, 90, 255)
face = (255, 230, 180, 255)
eye  = (70, 50, 20, 255)
nose = (180, 80, 80, 255)

# 身體
draw.rectangle([14, 30, 45, 57], fill=body)
# 臉
draw.rectangle([11, 14, 48, 38], fill=face)
# 耳朵
draw.polygon([(14,16),(20,4),(26,18)], fill=ear)
draw.polygon([(41,4),(47,16),(35,18)], fill=ear)
# 眼睛
draw.rectangle([21,25,25,29], fill=eye)
draw.rectangle([35,25,39,29], fill=eye)
# 鼻子
draw.rectangle([29,32,32,34], fill=nose)
# 嘴
draw.line([29,36,30,39,32,39,33,36], fill=nose, width=1)

# 尾巴
draw.rectangle([45,45,53,49], fill=body)
draw.rectangle([50,48,55,53], fill=body)

# 存檔
img.save("cat.png")
print("已產生貓咪圖片 cat.png")