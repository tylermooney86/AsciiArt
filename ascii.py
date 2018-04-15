#
# Ascii art generator

from PIL import Image
from os import listdir
import sys

# set default image dimensions
image_dimensions = (80,40)

# load image using name
def load_image(img_name):
    img_dir = 'Images/'
    image = Image.open(img_dir + img_name)
    image = image.resize(image_dimensions, Image.BILINEAR)
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

# generate list of images in Images dir
def generate_image_list():
    images = listdir('Images/')
    dir_list = {}
    for i in range(len(images)):
        dir_list[i+1] = images[i]
    return dir_list

# generate menu and get user input
def generate_ascii():
    # create list of images in image directory
    images = generate_image_list()

    #Check if images is empty
    if(len(images) == 0):
        print('Please add images to Images directory before running program.')
    else:
        # print list of images for user selection
        print('#'*6 + ' Images ' + '#'*6)
        print('='*20)
        for key, value in images.items():
            print('{} : {}'.format(key,value))

        # get user selection
        user_selection = int(input('Enter image number:'))

        # generate ascii art of user selected image
        print("Generating ascii art from {}.....".format(images[user_selection]))
        create_ascii(images[user_selection])
        #print results to terminal
        print_results(images[user_selection])
        main_menu()

# resize menu
def resize_menu():
    print('#'*6 + ' Resize ' + '#'*6)
    print('='*20)
    print('Current output image dimensions: ({},{})'.format(image_dimensions[0],image_dimensions[1]))
    dimensions = input('Input new dimensions separated by a comma, ex: x,y : ')
    dimensions = dimensions.split(',')
    set_image_dimensions(int(dimensions[0]), int(dimensions[1]))
    print('New output image dimensions: ({},{})'.format(image_dimensions[0],image_dimensions[1]))
    main_menu()


# set image Dimensions
def set_image_dimensions(x,y):
    global image_dimensions
    image_dimensions = (x,y)

#generate main menu
def main_menu():
    print('#'*23)
    print('#' + ' '*21 + '#')
    print('#' + ' ' + 'Ascii Art Generator' + ' ' + '#')
    print('#' + ' '*21 + '#')
    print('#'*23)
    print('='*23)

    print('1 : Generate Ascii Art From Image')
    print('2 : Set Output Dimensions')
    print('0 : Exit')
    choice = input('Enter Selection: ')
    if choice == '1':
        generate_ascii()
    if choice == '2':
        resize_menu()
    elif choice == '0':
        exit()
    else:
        print('Please enter selection from menu options')
        main_menu()

#print ascii art to terminal
def print_results(filename):
    filename = strip_extension(filename)
    text_file = open('AsciiArt/' + filename + '.txt', 'r')
    output = text_file.read()
    print(output)
    text_file.close()

#exit program
def exit():
    sys.exit()


##### Main #####
if __name__ == '__main__':
    main_menu()
