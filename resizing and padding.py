from PIL import Image, ImageOps

def process_image(input_path, output_path, resize_size=(500, 500), padding_size=33, padding_color=(204, 204, 204)):
    img = Image.open(input_path)
    
    # Resize ảnh thành 500x500
    img = img.resize(resize_size, Image.LANCZOS)

    # Tạo ảnh nền vuông (nếu resize rồi thì không cần nữa, nhưng giữ lại cho an toàn)
    size = max(img.size)
    square_img = Image.new("RGB", (size, size), (0, 0, 0))
    x_offset = (size - img.size[0]) // 2
    y_offset = (size - img.size[1]) // 2
    square_img.paste(img, (x_offset, y_offset))

    # Thêm padding
    padded_img = ImageOps.expand(square_img, border=padding_size, fill=padding_color)
    
    # Lưu ảnh kết quả
    padded_img.save(output_path)
    print(f"✅ Đã xử lý và lưu tại: {output_path}")

# Đường dẫn file
input_file = r"C:\Users\Administrator.DESKTOP-98TGIBL\Downloads\input.png"
output_file = r"C:\Users\Administrator.DESKTOP-98TGIBL\Downloads\output.png"

# Gọi hàm xử lý
process_image(input_file, output_file, resize_size=(500, 500), padding_size=33, padding_color=(204, 204, 204))
