from PIL import Image, ImageDraw

cell_size = 4

# 繪製單一人物（不變）
def draw_person(draw, top_left_x, top_left_y, skin_color, shirt_color):
    # 頭部：格子 (1,0),(2,0),(1,1),(2,1)
    head_cells = [(1,0), (2,0), (1,1), (2,1)]
    for cx, cy in head_cells:
        x0 = top_left_x + cx * cell_size
        y0 = top_left_y + cy * cell_size
        draw.rectangle([(x0, y0), (x0 + cell_size, y0 + cell_size)],
                       fill=skin_color)
    # 身體：格子 (1,2),(2,2),(1,3),(2,3)
    body_cells = [(1,2), (2,2), (1,3), (2,3)]
    for cx, cy in body_cells:
        x0 = top_left_x + cx * cell_size
        y0 = top_left_y + cy * cell_size
        draw.rectangle([(x0, y0), (x0 + cell_size, y0 + cell_size)],
                       fill=shirt_color)
    # 腿：格子 (1,4),(2,4),(1,5),(2,5)，深灰色表示褲子
    leg_color = (50, 50, 50)
    leg_cells = [(1,4), (2,4), (1,5), (2,5)]
    for cx, cy in leg_cells:
        x0 = top_left_x + cx * cell_size
        y0 = top_left_y + cy * cell_size
        draw.rectangle([(x0, y0), (x0 + cell_size, y0 + cell_size)],
                       fill=leg_color)
    # 手臂：格子 (0,2),(3,2)
    arm_cells = [(0,2), (3,2)]
    for cx, cy in arm_cells:
        x0 = top_left_x + cx * cell_size
        y0 = top_left_y + cy * cell_size
        draw.rectangle([(x0, y0), (x0 + cell_size, y0 + cell_size)],
                       fill=skin_color)

# 畫布大小設為 100×80，背景透明
canvas_width = 100
canvas_height = 80
img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 定義 5 種顏色組合 (膚色, 襯衫顏色)
color_schemes = [
    ((255, 224, 189), (255, 100, 100)),   # 膚色 + 紅襯衫
    ((255, 205, 148), (100, 180, 255)),   # 膚色 + 藍襯衫
    ((226, 188, 156), (180, 255, 100)),   # 深膚色 + 綠襯衫
    ((255, 224, 189), (255, 240, 100)),   # 膚色 + 黃襯衫
    ((255, 205, 148), (180, 100, 255)),   # 膚色 + 紫襯衫
]

# 每個角色橫向的間隔 = 角色本身寬度（4格 × cell_size） + 一格間距（1 × cell_size）
person_width = 4 * cell_size        # 16 像素
gap_width = 1 * cell_size           #  4 像素
step_x = (person_width + gap_width)*1.5   # 20 像素

# 設定三角形聚集時的基準起點
# 這裡讓後排最左邊的人在 x = 20, y = 24
base_back_x = 20
base_back_y = 24
base_front_y = 36

# 計算後排三人 (從左到右)
back_positions = [
    (base_back_x + step_x * 0, base_back_y),  # 後排左
    (base_back_x + step_x * 1, base_back_y),  # 後排中
    (base_back_x + step_x * 2, base_back_y),  # 後排右
]

# 計算前排兩人 (往下、往右各偏移 step_x/2，形成三角形)
front_positions = [
    (base_back_x + step_x * 0 + step_x//2, base_front_y),  # 前排左
    (base_back_x + step_x * 1 + step_x//2, base_front_y),  # 前排右
]

# 先繪製後排三人
for idx in range(len(back_positions)):
    x, y = back_positions[idx]
    skin, shirt = color_schemes[idx]
    draw_person(draw, x, y, skin, shirt)

# 再繪製前排兩人（蓋在後排之上）
for idx in range(len(front_positions)):
    x, y = front_positions[idx]
    skin, shirt = color_schemes[idx + len(back_positions)]
    draw_person(draw, x, y, skin, shirt)

# 將結果存檔或顯示
img.save('club.png', 'PNG')
img.show()
