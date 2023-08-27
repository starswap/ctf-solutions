from PIL import Image

PIXELS_PER_SQUARE = 10
RAW_FORMAT_STRINGS = ["111111111111111", "111011111000100", "111001011110011", "111110110101010", "111100010011101", "110011000101111", "110001100011000", "110110001000001", "110100101110110", "101010000010010", "101000100100101", "101111001111100", "101101101001011", "100010111111001", "100000011001110", "100111110010111", "100101010100000", "011010101011111", "011000001101000", "011111100110001", "011101000000110", "010010010110100", "010000110000011", "010111011011010", "010101111101101", "001011010001001", "001001110111110", "001110011100111", "001100111010000", "000011101100010", "000001001010101", "000110100001100", "000100000111011"]
FORMAT_STRINGS = [*map(lambda string : [*map(lambda x : x == '1', string)], RAW_FORMAT_STRINGS)]
POSITION_MARKER_SIZE = 7

def image_to_qr(image):
    code = []
    width, height = image.size
    for y in range(0, height, PIXELS_PER_SQUARE):
        code.append([])
        for x in range(0, width, PIXELS_PER_SQUARE):
            (r, g, b, a) = image.getpixel((x, y))
            code[-1].append(r == 0)
    return code

def qr_to_image(code):
    image = Image.new("RGBA", (len(code) * PIXELS_PER_SQUARE, len(code) * PIXELS_PER_SQUARE))
    for r, row in enumerate(code):
        for c, sq in enumerate(row):
            for j in range(PIXELS_PER_SQUARE):
                for i in range(PIXELS_PER_SQUARE):
                    value = 0 if sq else 255
                    image.putpixel((c * PIXELS_PER_SQUARE + i, r * PIXELS_PER_SQUARE + j), (value, value, value, 255))
    return image

def insert_format_bits(code, format_bits):
    format_postitions = [(POSITION_MARKER_SIZE + 1, i) for i in range(6)] + [(POSITION_MARKER_SIZE + 1, 7)] + [(POSITION_MARKER_SIZE + 1, 8)]  +[(POSITION_MARKER_SIZE, 8)] + [(POSITION_MARKER_SIZE - i - 2, 8) for i in range(6)]
    for i, (r, c) in enumerate(format_postitions):
        code[r][c] = format_bits[i]

    format_postitions = [(20 - i, POSITION_MARKER_SIZE + 1) for i in range(7)] + [(POSITION_MARKER_SIZE + 1, 13 + i) for i in range(8)]
    for i, (r, c) in enumerate(format_postitions):
        code[r][c] = format_bits[i]
    return code

def read_wrong_bit_sequence(code):
    bits = []

    POSITION_MARKER_SIZE + 2


def collage_images(images, padding):
    (width, height) = images[0].size
    new_width = padding + (width + padding) * len(images) 
    new_height = padding + height + padding # (height + padding) * len(images) 
    image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))

    for i, old_image in enumerate(images):
        for r in range(height):
            for c in range(width):
                r_pixel = padding + r
                c_pixel = padding + (width + padding) * i + c
                image.putpixel((c_pixel, r_pixel), old_image.getpixel((c, r)))
                
    return image
    
# Open an image file
image_path = "chall.png"
image = Image.open(image_path)
output_path = "modified_example.png"
code = image_to_qr(image)

strings = []
for row in code:
    strings.append("")
    for item in row:
        strings[-1] += "1" if item else "0"
print("\n".join(strings))


# images = [qr_to_image(insert_format_bits(code, form_str)) for form_str in FORMAT_STRINGS]
# collage_images(images, 100).save(output_path)

# # Loop through each pixel in the image
# for y in range(height):
#     for x in range(width):
#         # Get the RGB values of the pixel
#         (r, g, b, a) = image.getpixel((x, y))

#         # # Example: Invert the colors
#         # inverted_r = 255 - r
#         # inverted_g = 255 - g
#         # inverted_b = 255 - b

#         # Update the pixel with the new RGB values
#         # image.putpixel((x, y), (inverted_r, inverted_g, inverted_b))

# # Save the modified image


# print("Image pixels edited and saved.")

