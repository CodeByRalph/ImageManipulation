from PIL import Image


image = Image.open("Lena.jpg")
width, height = image.size
image.show()

print('--------------------------------------------------------------')
print("Image Mode:", image.mode)
print("\nDimensions of the image (Width x Height):", width, "x", height)

uncompressed_size = width * height * 24
print("\nUncompressed size of the image:", uncompressed_size, "bits")
compressed_size = width*height
print('\nCompression Rate:', uncompressed_size/compressed_size, '%')

# Converting RGB image to YCbCr
image = image.convert('YCbCr')
print('\nImage Mode after Conversion:', image.mode)


# ///////////////////// Changing Y Value //////////////////////////
# Splitting YCbCr image into channels
y, cb, cr = image.split()

# Change brighness factor to increase brightness
brightness_factor = 3
adjusted_y_pixels = []

for pixel in y.getdata():
    adjusted_y_pixels.append(min(int(pixel * brightness_factor), 255))

adjusted_y = y.copy()
adjusted_y.putdata(adjusted_y_pixels)
adjusted_ycbcr_image = Image.merge("YCbCr", (adjusted_y, cb, cr))

#Converting back to RGB
final_rgb_image = adjusted_ycbcr_image.convert("RGB")


#//////////////// Changing a selection of Red Values ////////////////
lower_bound = (20, 0, 0)
upper_bound = (255, 190, 190)

for i in range(image.height):
    for j in range(image.width):
        ycbcr_pixels = image.getpixel((j,i))

        if lower_bound[0] <= ycbcr_pixels[0] <= upper_bound[0] and \
           lower_bound[1] <= ycbcr_pixels[1] <= upper_bound[1] and \
           lower_bound[2] <= ycbcr_pixels[2] <= upper_bound[2]:
            
            ycbcr_pixels = (ycbcr_pixels[0], 128, ycbcr_pixels[2])
            image.putpixel((j, i), ycbcr_pixels)

result_image = image.convert('RGB')


#/////////////////// Simulating JPEG Compression ONLY Cb and Cr////////////////////
downsampled_cb = image.getchannel("Cb").resize((int(image.width / 2), int(image.height / 2)), Image.BOX)
downsampled_cr = image.getchannel("Cr").resize((int(image.width / 2), int(image.height / 2)), Image.BOX)

upsampled_cb = downsampled_cb.resize((image.width, image.height), Image.BOX)
upsampled_cr = downsampled_cr.resize((image.width, image.height), Image.BOX)

upsampled_ycbcr_image = Image.merge("YCbCr", (image.getchannel("Y"), upsampled_cb, upsampled_cr))
result_image2 = upsampled_ycbcr_image.convert("RGB")

#////////////////// Simulating JPEG Compression With all three channels //////////////////
downsampled_y = image.getchannel("Y").resize((int(image.width / 2), int(image.height / 2)), Image.BOX)
downsampled_cb = image.getchannel("Cb").resize((int(image.width / 2), int(image.height / 2)), Image.BOX)
downsampled_cr = image.getchannel("Cr").resize((int(image.width / 2), int(image.height / 2)), Image.BOX)

upsampled_y = downsampled_y.resize((image.width, image.height), Image.BOX)
upsampled_cb = downsampled_cb.resize((image.width, image.height), Image.BOX)
upsampled_cr = downsampled_cr.resize((image.width, image.height), Image.BOX)

upsampled_ycbcr_image = Image.merge("YCbCr", (upsampled_y, upsampled_cb, upsampled_cr))
result_image3 = upsampled_ycbcr_image.convert("RGB")

# Final Images being displayed
final_rgb_image.show()
result_image.show()
result_image2.show()
result_image3.show()

print('--------------------------------------------------------------')


