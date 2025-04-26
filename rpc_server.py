import grpc
from concurrent import futures
import mask_service_pb2
import mask_service_pb2_grpc
from PIL import Image, ImageDraw, ImageOps
import io
import logging

class MaskServiceServicer(mask_service_pb2_grpc.MaskServiceServicer):
    def ApplyMask(self, request, context):
        try:
            image_data = io.BytesIO(request.image_data)
            image = Image.open(image_data).convert("RGBA")
            
            mask = self.create_puzzle_mask(
                edges=request.edges,
                piece_size=request.piece_size,
                tab_size=request.tab_size
            )
            
            result_image = self.apply_mask(
                image=image,
                mask=mask,
                x=request.x,
                y=request.y,
                piece_size=request.piece_size,
                tab_size=request.tab_size
            )
            
            result_bytes = io.BytesIO()
            result_image.save(result_bytes, format="PNG")
            result_bytes.seek(0)
            
            return mask_service_pb2.MaskResponse(
                result_image_data=result_bytes.read()
            )
            
        except Exception as e:
            logging.error(f"Error in ApplyMask: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mask_service_pb2.MaskResponse()

    def create_puzzle_mask(self, edges, piece_size, tab_size):
        top, right, bottom, left = edges
        extra_padding = 10  # Tăng padding để tránh cắt mất tab
        total_size = piece_size + 2 * (tab_size + extra_padding)
        
        mask = Image.new('L', (total_size, total_size), 0)
        draw = ImageDraw.Draw(mask)
        
        center_box = [
            tab_size + extra_padding,
            tab_size + extra_padding,
            tab_size + extra_padding + piece_size,
            tab_size + extra_padding + piece_size
        ]
        draw.rectangle(center_box, fill=255)
        
        def draw_jigsaw_tab(direction, tab_type):
            if tab_type == 0:
                return
            
            neck_width = tab_size * 0.5
            head_size = tab_size * 0.7
            neck_length = tab_size * 0.5
            
            if direction == 'top':
                center_x = tab_size + extra_padding + piece_size // 2
                if tab_type == 1:  # Protruding tab
                    neck_points = [
                        (center_x - neck_width / 2, tab_size + extra_padding),
                        (center_x + neck_width / 2, tab_size + extra_padding),
                        (center_x + neck_width / 2, tab_size + extra_padding - neck_length),
                        (center_x - neck_width / 2, tab_size + extra_padding - neck_length)
                    ]
                    head_box = [
                        center_x - head_size / 2,
                        tab_size + extra_padding - neck_length - head_size / 2,
                        center_x + head_size / 2,
                        tab_size + extra_padding - neck_length + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=255)
                    draw.ellipse(head_box, fill=255)
                else:  # Inset groove
                    neck_points = [
                        (center_x - neck_width / 2, tab_size + extra_padding),
                        (center_x + neck_width / 2, tab_size + extra_padding),
                        (center_x + neck_width / 2, tab_size + extra_padding + neck_length),
                        (center_x - neck_width / 2, tab_size + extra_padding + neck_length)
                    ]
                    head_box = [
                        center_x - head_size / 2,
                        tab_size + extra_padding + neck_length - head_size / 2,
                        center_x + head_size / 2,
                        tab_size + extra_padding + neck_length + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=0)
                    draw.ellipse(head_box, fill=0)
            
            elif direction == 'right':
                center_y = tab_size + extra_padding + piece_size // 2
                if tab_type == 1:
                    neck_points = [
                        (tab_size + extra_padding + piece_size, center_y - neck_width / 2),
                        (tab_size + extra_padding + piece_size, center_y + neck_width / 2),
                        (tab_size + extra_padding + piece_size + neck_length, center_y + neck_width / 2),
                        (tab_size + extra_padding + piece_size + neck_length, center_y - neck_width / 2)
                    ]
                    head_box = [
                        tab_size + extra_padding + piece_size + neck_length - head_size / 2,
                        center_y - head_size / 2,
                        tab_size + extra_padding + piece_size + neck_length + head_size / 2,
                        center_y + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=255)
                    draw.ellipse(head_box, fill=255)
                else:
                    neck_points = [
                        (tab_size + extra_padding + piece_size, center_y - neck_width / 2),
                        (tab_size + extra_padding + piece_size, center_y + neck_width / 2),
                        (tab_size + extra_padding + piece_size - neck_length, center_y + neck_width / 2),
                        (tab_size + extra_padding + piece_size - neck_length, center_y - neck_width / 2)
                    ]
                    head_box = [
                        tab_size + extra_padding + piece_size - neck_length - head_size / 2,
                        center_y - head_size / 2,
                        tab_size + extra_padding + piece_size - neck_length + head_size / 2,
                        center_y + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=0)
                    draw.ellipse(head_box, fill=0)
            
            elif direction == 'bottom':
                center_x = tab_size + extra_padding + piece_size // 2
                if tab_type == 1:
                    neck_points = [
                        (center_x - neck_width / 2, tab_size + extra_padding + piece_size),
                        (center_x + neck_width / 2, tab_size + extra_padding + piece_size),
                        (center_x + neck_width / 2, tab_size + extra_padding + piece_size + neck_length),
                        (center_x - neck_width / 2, tab_size + extra_padding + piece_size + neck_length)
                    ]
                    head_box = [
                        center_x - head_size / 2,
                        tab_size + extra_padding + piece_size + neck_length - head_size / 2,
                        center_x + head_size / 2,
                        tab_size + extra_padding + piece_size + neck_length + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=255)
                    draw.ellipse(head_box, fill=255)
                else:
                    neck_points = [
                        (center_x - neck_width / 2, tab_size + extra_padding + piece_size),
                        (center_x + neck_width / 2, tab_size + extra_padding + piece_size),
                        (center_x + neck_width / 2, tab_size + extra_padding + piece_size - neck_length),
                        (center_x - neck_width / 2, tab_size + extra_padding + piece_size - neck_length)
                    ]
                    head_box = [
                        center_x - head_size / 2,
                        tab_size + extra_padding + piece_size - neck_length - head_size / 2,
                        center_x + head_size / 2,
                        tab_size + extra_padding + piece_size - neck_length + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=0)
                    draw.ellipse(head_box, fill=0)
            
            elif direction == 'left':
                center_y = tab_size + extra_padding + piece_size // 2
                if tab_type == 1:
                    neck_points = [
                        (tab_size + extra_padding, center_y - neck_width / 2),
                        (tab_size + extra_padding, center_y + neck_width / 2),
                        (tab_size + extra_padding - neck_length, center_y + neck_width / 2),
                        (tab_size + extra_padding - neck_length, center_y - neck_width / 2)
                    ]
                    head_box = [
                        tab_size + extra_padding - neck_length - head_size / 2,
                        center_y - head_size / 2,
                        tab_size + extra_padding - neck_length + head_size / 2,
                        center_y + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=255)
                    draw.ellipse(head_box, fill=255)
                else:
                    neck_points = [
                        (tab_size + extra_padding, center_y - neck_width / 2),
                        (tab_size + extra_padding, center_y + neck_width / 2),
                        (tab_size + extra_padding + neck_length, center_y + neck_width / 2),
                        (tab_size + extra_padding + neck_length, center_y - neck_width / 2)
                    ]
                    head_box = [
                        tab_size + extra_padding + neck_length - head_size / 2,
                        center_y - head_size / 2,
                        tab_size + extra_padding + neck_length + head_size / 2,
                        center_y + head_size / 2
                    ]
                    draw.polygon(neck_points, fill=0)
                    draw.ellipse(head_box, fill=0)
        
        if top != 0:
            draw_jigsaw_tab('top', top)
        if right != 0:
            draw_jigsaw_tab('right', right)
        if bottom != 0:
            draw_jigsaw_tab('bottom', bottom)
        if left != 0:
            draw_jigsaw_tab('left', left)
        
        return mask

    def apply_mask(self, image, mask, x, y, piece_size, tab_size):
        padding = tab_size + 10
        new_width = image.width + 2 * padding
        new_height = image.height + 2 * padding
        padded_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        padded_image.paste(image, (padding, padding)) 
        alpha = Image.new('L', (new_width, new_height), 0)
        alpha.paste(mask, (x , y )) 

        result = padded_image.copy()
        result.putalpha(alpha)

        # alpha = Image.new('L', image.size, 0)
        # alpha.paste(mask, (x, y))
        # result = image.copy()
        # result.putalpha(alpha)
        # bbox = result.getbbox()
        # if bbox:
        #     cropped = result.crop(bbox)
        #     # Tính final_size động để đảm bảo đủ chỗ cho tab
        #     neck_length = tab_size * 0.5
        #     head_size = tab_size * 0.7
        #     final_size = piece_size + 2 * (neck_length + head_size / 2) + 20  # +20 để dư padding
            
        #     final_size = int(final_size)
        #     centered = Image.new('RGBA', (final_size, final_size), (0, 0, 0, 0))
        #     paste_x = (final_size - cropped.width) // 2
        #     paste_y = (final_size - cropped.height) // 2
        #     centered.paste(cropped, (paste_x, paste_y))
        #     return centered
        return result

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mask_service_pb2_grpc.add_MaskServiceServicer_to_server(
        MaskServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server running on port 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
