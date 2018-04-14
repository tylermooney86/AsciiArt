#
# Ascii art generator

from PIL import Image
from os import listdir

# load image using name
def load_image(img_name,x,y):
    img_dir = 'Images/'
    image = Image.open(img_dir + img_name)
    image = image.resize((x,y),Image.BILINEAR)
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
def create_ascii(img_name,x,y):
    #load image get image size
    img = monochrome(load_image(img_name,x,y))
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

# generate list of images in Images dir
def generate_image_list():
    images = listdir('Images/')
    dir_list = {}
    for i in range(len(images)):
        dir_list[i+1] = images[i]
    return dir_list

# generate menu and get user input
def generate_menu():
    # create list of images in image directory
    images = generate_image_list()

    #Check if images is empty
    if(len(images) == 0):
        print('Please add images to Images directory before running program.')
    else:
        # print list of images for user selection
        print('#'*5 + 'Images' + '#'*5)
        for key, value in images.items():
            print('{} : {}'.format(key,value))

        # get user selection
        user_selection = int(input('Enter image number:'))
        img_dimensions = input('Enter desired output dimensions separated by a comma, ex: x,y: ')
        img_dimensions = img_dimensions.split(',')

        # generate ascii art of user selected image
        print("Generating ascii art from {}.....".format(images[user_selection]))
        create_ascii(images[user_selection],int(img_dimensions[0]),int(img_dimensions[1]))
        #print results to terminal
        print_results(images[user_selection])

#print ascii art to terminal
def print_results(filename):
    filename = strip_extension(filename)
    text_file = open('AsciiArt/' + filename + '.txt', 'r')
    output = text_file.read()
    print(output)
    text_file.close()


##### Main #####

generate_menu()
