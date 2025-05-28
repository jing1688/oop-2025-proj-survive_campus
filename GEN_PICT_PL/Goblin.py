from PIL import Image, ImageDraw

def generate_goblin(
    size=(60, 60),
    skin_color=(50, 205, 50, 255),
    ear_color=(34, 139, 34, 255),
    face_color=(144, 238, 144, 255),
    eye_color=(0, 0, 0, 255),
    nose_color=(0, 100, 0, 255),
    mouth_color=(139, 69, 19, 255),
    horn=False,
    horn_color=(200, 200, 200, 255),
    foot_color=(100, 130, 230, 255)  # 小腳顏色
):
    """
    生成一隻像素風格的 Goblin。
    參數:
      size: (寬, 高) 元組
      *_color: RGBA 顏色
      horn: 是否加上角
    """
    w, h = size
    img = Image.new('RGBA', size, (0,0,0,0))
    draw = ImageDraw.Draw(img)

    # 頭部
    head = [ (w*0.15, h*0.20), (w*0.85, h*0.60) ]
    draw.rectangle(head, fill=skin_color)

    # 臉部貼色
    face = [ (w*0.12, h*0.18), (w*0.88, h*0.40) ]
    draw.rectangle(face, fill=face_color)

    # 耳朵（三角形）
    left_ear  = [(w*0.15, h*0.20), (w*0.05, h*0.40), (w*0.25, h*0.35)]
    right_ear = [(w*0.85, h*0.20), (w*0.95, h*0.40), (w*0.75, h*0.35)]
    draw.polygon(left_ear, fill=ear_color)
    draw.polygon(right_ear, fill=ear_color)

    # 眼睛（橢圓）
    eye_w, eye_h = w*0.08, h*0.06
    left_eye_box  = [ (w*0.30, h*0.32), (w*0.30+eye_w, h*0.32+eye_h) ]
    right_eye_box = [ (w*0.60, h*0.32), (w*0.60+eye_w, h*0.32+eye_h) ]
    draw.ellipse(left_eye_box, fill=eye_color)
    draw.ellipse(right_eye_box, fill=eye_color)

    # 鼻子（三角形）
    nose = [(w*0.50, h*0.42), (w*0.46, h*0.50), (w*0.54, h*0.50)]
    draw.polygon(nose, fill=nose_color)

    # 嘴巴（線段）
    mouth = [(w*0.46, h*0.55), (w*0.54, h*0.55)]
    draw.line(mouth, fill=mouth_color, width=1)

    # 身體
    body = [ (w*0.25, h*0.60), (w*0.75, h*0.95) ]
    draw.rectangle(body, fill=skin_color)

     # 小腳 (左右兩隻)
    foot_width, foot_height = w*0.10, h*0.07
    left_foot  = [ (w*0.30, h*0.90), (w*0.30+foot_width, h*0.90+foot_height) ]
    right_foot = [ (w*0.60, h*0.90), (w*0.60+foot_width, h*0.90+foot_height) ]
    draw.rectangle(left_foot, fill=foot_color)
    draw.rectangle(right_foot, fill=foot_color)
    # 可選：角
    if horn:
        horn_left  = [(w*0.30, h*0.18), (w*0.28, h*0.05), (w*0.35, h*0.15)]
        horn_right = [(w*0.70, h*0.18), (w*0.72, h*0.05), (w*0.65, h*0.15)]
        draw.polygon(horn_left, fill=horn_color)
        draw.polygon(horn_right, fill=horn_color)

    return img

# 範例：產生一隻有角的綠皮哥布林
if __name__ == "__main__":
    goblin = generate_goblin(
        size=(60,60),
        skin_color=(30,180,30,255),
        horn=True
    )
    goblin.save("goblin.png")
    print("已產生 goblin.png")
