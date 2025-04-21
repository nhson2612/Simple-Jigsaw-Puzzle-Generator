from PIL import Image, ImageDraw, ImageOps

def draw_puzzle_piece(PIECE_SIZE, TAB_SIZE, edges):
    top, right, bottom, left = edges
    total_size = PIECE_SIZE + 2 * TAB_SIZE

    # Tạo ảnh gốc màu trắng
    original = Image.new('RGB', (PIECE_SIZE, PIECE_SIZE), 'white')
    img = Image.new('RGB', (total_size, total_size), 'black')
    img.paste(original, (TAB_SIZE, TAB_SIZE))

    draw = ImageDraw.Draw(img)

    def draw_tab_arc(direction, tab_type):
        radius = TAB_SIZE
        if direction == 'top':
            center = (TAB_SIZE + PIECE_SIZE // 2, TAB_SIZE)
            bbox = [center[0]-radius, center[1]-radius,
                    center[0]+radius, center[1]+radius]
            if tab_type == 1:
                draw.pieslice(bbox, 180, 360, fill='white')
            else:
                mask = Image.new('L', img.size, 0)
                ImageDraw.Draw(mask).pieslice(bbox, 0, 180, fill=255)
                img.paste('black', mask=mask)

        elif direction == 'bottom':
            center = (TAB_SIZE + PIECE_SIZE // 2, TAB_SIZE + PIECE_SIZE)
            bbox = [center[0]-radius, center[1]-radius,
                    center[0]+radius, center[1]+radius]
            if tab_type == 1:
                draw.pieslice(bbox, 0, 180, fill='white')
            else:
                mask = Image.new('L', img.size, 0)
                ImageDraw.Draw(mask).pieslice(bbox, 180, 0, fill=255)
                img.paste('black', mask=mask)

        elif direction == 'left':
            center = (TAB_SIZE, TAB_SIZE + PIECE_SIZE // 2)
            bbox = [center[0]-radius, center[1]-radius,
                    center[0]+radius, center[1]+radius]
            if tab_type == 1:
                draw.pieslice(bbox, 450, 270, fill='white')
            else:
                mask = Image.new('L', img.size, 0)
                ImageDraw.Draw(mask).pieslice(bbox, 270, 450, fill=255)
                img.paste('black', mask=mask)

        elif direction == 'right':
            center = (TAB_SIZE + PIECE_SIZE, TAB_SIZE + PIECE_SIZE // 2)
            bbox = [center[0]-radius, center[1]-radius,
                    center[0]+radius, center[1]+radius]
            if tab_type == 1:
                draw.pieslice(bbox, 270, 90, fill='white')
            else:
                mask = Image.new('L', img.size, 0)
                ImageDraw.Draw(mask).pieslice(bbox, 90, 270, fill=255)
                img.paste('black', mask=mask)

    if top != 0: draw_tab_arc('top', top)
    if right != 0: draw_tab_arc('right', right)
    if bottom != 0: draw_tab_arc('bottom', bottom)
    if left != 0: draw_tab_arc('left', left)

    return img

from PIL import Image

# ==== Danh sách cấu hình edges và tọa độ ====
configs = [
    ([0, 1, -1, 0], (0, 0)),
    ([0, -1, 1, -1], (100, 0)),
    ([0, -1, 1, 1], (200, 0)),
    ([0, 1, -1, 1], (300, 0)),
    ([0, 0, 1, -1], (400, 0)),
    ([1, -1, -1, 0], (0, 100)),
    ([-1, -1, -1, 1], (100, 100)),
    ([-1, -1, 1, 1], (200, 100)),
    ([1, -1, 1, 1], (300, 100)),
    ([-1, 0, -1, 1], (400, 100)),
    ([1, 1, -1, 0], (0, 200)),
    ([1, -1, -1, -1], (100, 200)),
    ([-1, 1, 1, 1], (200, 200)),
    ([-1, 1, 1, -1], (300, 200)),
    ([1, 0, -1, -1], (400, 200)),
    ([1, -1, 1, 0], (0, 300)),
    ([1, 1, -1, 1], (100, 300)),
    ([-1, -1, 1, -1], (200, 300)),
    ([-1, 1, 1, 1], (300, 300)),
    ([1, 0, -1, -1], (400, 300)),
    ([-1, 1, 0, 0], (0, 400)),
    ([1, -1, 0, -1], (100, 400)),
    ([-1, 1, 0, 1], (200, 400)),
    ([-1, 1, 0, -1], (300, 400)),
    ([1, 0, 0, -1], (400, 400)),
]

# ==== Load ảnh gốc lớn ====
background = Image.open(r"C:\Users\Administrator.DESKTOP-98TGIBL\Downloads\output.png").convert('RGBA')

# ==== Thông số puzzle ====
PIECE_SIZE = 100
TAB_SIZE = 33

# ==== Duyệt từng config ====
for idx, (edges, (x, y)) in enumerate(configs):
    # Tạo mask trắng đen từ edges
    mask = draw_puzzle_piece(PIECE_SIZE, TAB_SIZE, edges)

    # Tạo mask phủ toàn ảnh
    full_mask = Image.new('L', background.size, 0)
    full_mask.paste(mask, (x, y))

    # Áp mask lên ảnh gốc
    cut_out = Image.new('RGBA', background.size, (0, 0, 0, 0))
    cut_out.paste(background, (0, 0), full_mask)

    # Cắt vùng đúng bằng kích thước mask
    box = (x, y, x + mask.width, y + mask.height)
    cropped_result = cut_out.crop(box)

    # Lưu ảnh
    cropped_result.save(f"piece_{idx:02d}.png")