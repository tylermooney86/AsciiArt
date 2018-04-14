#
# Ascii art generator

from PIL import Image

# load image using name
def load_image(img_name):
    img_dir = 'Images/'
    image = Image.open(img_dir + img_name)
    return image

#strip extension from image name
def strip_extension(img_name):
    img_split = img_name.split('.')
    return img_split[0]

# convert images to monochrome
def monochrome(image):
    return image.convert('1')

#read pixel value from image
def read_pixels(img, x, y):
    pixel = img.load()
    return pixel[x,y]

#generate ascii image
def create_ascii(img_name):
    #load image get image size
    img = monochrome(load_image(img_name))
    width, height = img.size

    # starting coordinates on image
    x = 0
    y = 0

    #assign ascii chars to monochrome values
    chars = {0: '$', 255: ' '}

    # open file to write ascii art to
    text_file = open('AsciiArt/' + strip_extension(img_name) + '.txt', 'w')

    # convert each pixel to ascii char and write to file
    while y <= height - 1:
        rgb = read_pixels(img,x,y)
        text_file.write(chars[rgb])
        x += 1
        if(x == width -1):
            text_file.write('\n')
            y += 1
            x = 0

    #close text file
    text_file.close()

##### Main #####

#prompt user for file name and extension
image_name = input('please enter name of image:')
create_ascii(image_name)
