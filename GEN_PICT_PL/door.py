from PIL import Image, ImageDraw

# 建立 128×128 的透明畫布
size = (128, 128)
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# ----------------- 顏色定義 -----------------
sky_color     = (180, 210, 255, 255)   # 清新淡藍天空
ground_color  = (160, 180, 140, 255)   # 灰綠草地
pillar_color  = (200, 200, 200, 255)   # 淺灰石材柱
beam_color    = (80,  80,  80, 255)    # 深灰金屬橫梁
gate_color    = (250, 240, 230, 255)   # 奶白暖色校門
path_color    = (200, 200, 200, 255)   # 淡灰石板路

# ------------- 畫天空與地面 -------------
draw.rectangle([(0, 0), (128, 64)], fill=sky_color)      # 天空 (上半部)
draw.rectangle([(0, 64), (128, 128)], fill=ground_color) # 地面 (下半部)

# ---------- 畫校門柱子與橫梁 ----------
pillar_width  = 10
pillar_height = 48
left_px       = 28
right_px      = 90
pillar_py     = 40

# 左側柱子
draw.rectangle(
    [(left_px, pillar_py), (left_px + pillar_width, pillar_py + pillar_height)],
    fill=pillar_color
)
# 右側柱子
draw.rectangle(
    [(right_px, pillar_py), (right_px + pillar_width, pillar_py + pillar_height)],
    fill=pillar_color
)

# 橫梁
beam_height = 8
draw.rectangle(
    [(left_px, pillar_py), (right_px + pillar_width, pillar_py + beam_height)],
    fill=beam_color
)

# ------------- 畫校門門扇 -------------
gate_width  = 24
gate_height = 40
# 左側半開門扇
draw.polygon([
    (left_px + pillar_width, pillar_py + beam_height),
    (left_px + pillar_width + gate_width, pillar_py + beam_height),
    (left_px + pillar_width + gate_width, pillar_py + beam_height + gate_height),
    (left_px + pillar_width, pillar_py + beam_height + gate_height)
], fill=gate_color)
# 右側半開門扇
draw.polygon([
    (right_px, pillar_py + beam_height),
    (right_px - gate_width, pillar_py + beam_height),
    (right_px - gate_width, pillar_py + beam_height + gate_height),
    (right_px, pillar_py + beam_height + gate_height)
], fill=gate_color)

# ------------- 畫校門前的小路 -------------
path_start_y   = pillar_py + beam_height + gate_height
path_half_w    = gate_width
path_x_center  = (left_px + pillar_width + right_px) // 2

draw.polygon([
    (path_x_center - path_half_w, path_start_y),
    (path_x_center + path_half_w, path_start_y),
    (path_x_center + 2*path_half_w, 128),
    (path_x_center - 2*path_half_w, 128)
], fill=path_color)
# 顯示圖像
img.save('door.png', 'PNG')
