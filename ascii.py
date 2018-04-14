#
# Ascii art generator

from PIL import Image

# convert images to monochrome
def monochrome(img_name, extension):
    photo = Image.open('Images/'+img_name+extension)
    photo = photo.convert('1')
    return photo

#read pixel value from image
def read_pixels(img, x, y):
    pixel = img.load()
    return pixel[x,y]

#generate ascii image
def create_ascii(img, img_name):
    # get image size
    width, height = img.size

    # starting coordinates on image
    x = 0
    y = 0

    #assign ascii chars to monochrome values
    chars = {0: '$', 255: ' '}

    # open file to write ascii art to
    text_file = open('Images/' + img_name + '.txt', 'w')

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
extension = input('enter extension (.jpg):')

image = monochrome(image_name, extension)
create_ascii(image, image_name)
