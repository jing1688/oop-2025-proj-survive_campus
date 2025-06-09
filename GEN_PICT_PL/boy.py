from PIL import Image, ImageDraw

# --- base pixel art size ---
w, h = 16, 24
img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# palette
SKIN  = (255, 205, 148, 255)
HAIR  = (60, 40, 30, 255)
EYE   = (20, 20, 20, 255)
SHIRT = (50, 100, 200, 255)
PANTS = (40, 40, 40, 255)
SHOES = (25, 25, 25, 255)

# helper
def px(x, y, color):
    draw.point((x, y), fill=color)

# --- draw head & hair ---
for x in range(4, 12):
    px(x, 0, HAIR)
for x in range(3, 13):
    px(x, 1, HAIR)
for x in range(3, 13):
    px(x, 2, SKIN)
for x in range(4, 12):
    px(x, 3, SKIN)
for x in range(4, 12):
    px(x, 4, SKIN)
for x in range(4, 12):
    px(x, 5, SKIN)

# hair sideburns
px(3,2,HAIR)
px(12,2,HAIR)
px(3,3,HAIR)
px(12,3,HAIR)

# eyes
px(6,3,EYE)
px(9,3,EYE)

# mouth
for x in range(6,9):
    px(x,5,EYE)

# --- neck ---
for x in range(6,10):
    px(x,6,SKIN)

# --- shoulders/arms ---
for x in range(2,14):
    px(x,7,SHIRT)
# arms skin
for y in range(8,13):
    px(2,y,SKIN)
    px(13,y,SKIN)

# --- torso ---
for y in range(8,14):
    for x in range(4,12):
        px(x,y,SHIRT)

# --- belt line ---
for x in range(4,12):
    px(x,14,(90,90,90,255))

# --- legs/pants ---
for y in range(15,20):
    for x in range(4,8):
        px(x,y,PANTS)
    for x in range(8,12):
        px(x,y,PANTS)

# --- shoes ---
for x in range(4,8):
    px(x,20,SHOES)
    px(x,21,SHOES)
for x in range(8,12):
    px(x,20,SHOES)
    px(x,21,SHOES)

# upscale for visibility
scale = 10
big = img.resize((w*scale, h*scale), Image.NEAREST)


big.save()


