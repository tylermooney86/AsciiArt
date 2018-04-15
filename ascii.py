#
# Ascii art generator

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from os import listdir
import sys
import string
import collections

# set default image dimensions
image_dimensions = (80,40)
font = ImageFont.load_default()
image_dir = 'Images/'
output_dir = 'AsciiArt/'
selected_image = None

#TODO use selected_image to allow the user to select an image and generate separately
#so they can tweak settings and generate without selecting every time

#TODO use ImageEnhance to create contrast/brightness settings for more control


# check density of char for sorting
def char_density(c, font=font):
    image = Image.new('1', font.getsize(c), color=255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), c, font=font)
    return collections.Counter(image.getdata())[0] #0 is black

# Default character lists
mono_chars = ' $'
grayscale_chars = list(sorted(string.ascii_letters + string.digits + string.punctuation + ' ', key=char_density, reverse=True))

# load image using name
def load_image(img_name):
    image = Image.open(image_dir + img_name)
    if(image_dimensions):
        image = image.resize(image_dimensions, Image.ANTIALIAS)
    return image

#strip extension from image name
def strip_extension(img_name):
    img_split = img_name.split('.')
    return img_split[0]

# convert images to monochrome
def monochrome(image):
    return image.convert('1')

# convert image to grayscale
def grayscale(image):
    return image.convert('L')

#read pixel value from image
def read_pixels(img, x, y):
    pixel = img.load()
    return pixel[x,y]

# set image Dimensions
def set_image_dimensions(dimensions):
    global image_dimensions
    image_dimensions = dimensions

# generate list of images in Images dir
def generate_image_list(directory):
    images = listdir(directory)
    dir_list = {}
    for i in range(len(images)):
        dir_list[i+1] = images[i]
    return dir_list

# Update a character list
def update_char_list(new_list, list_name):
    # These are global variables
    global mono_chars, grayscale_chars
    # for the monochrome list
    if list_name == 'Monochrome':
        mono_chars = list(sorted(new_list, key=char_density, reverse=True))
    else:
        grayscale_chars = list(sorted(new_list, key=char_density, reverse=True))

#generate ascii image
def create_ascii(img_name):
    #load image get image size
    img = monochrome(load_image(img_name))
    width, height = img.size

    # starting coordinates on image
    x = 0
    y = 0

    #assign ascii chars to monochrome values
    chars = {0: mono_chars[0], 255: mono_chars[1]}

    # open file to write ascii art to
    text_file = open(output_dir + strip_extension(img_name) + '.txt', 'w')

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

# write grayscale ascii art to file
def create_grayscale_ascii(img_name):
    #load image get image size
    img = grayscale(load_image(img_name))
    width, height = img.size

    # starting coordinates on image
    x = 0
    y = 0

    #assign ascii chars weighted by char_density
    chars = grayscale_chars

    # open file to write ascii art to
    text_file = open(output_dir + strip_extension(img_name) + '.txt', 'w')

    # convert each pixel to ascii char and write to file
    while y <= height - 1:
        rgb = read_pixels(img,x,y)
        text_file.write(chars[int(rgb /255. * (len(chars) - 1) + 0.5) ])
        x += 1
        if(x == width -1):
            text_file.write('\n')
            y += 1
            x = 0

    #close text file
    text_file.close()

# generate menu and get user input
def generate_ascii():
    # create list of images in image directory
    images = generate_image_list(image_dir)

    #Check if images is empty
    if(len(images) == 0):
        print('Please add images to Images directory before running program.')
    else:
        # print list of images for user selection
        print('='*20)
        print('#'*6 + ' Images ' + '#'*6)
        print('='*20)
        for key, value in images.items():
            print('{} : {}'.format(key,value))
        print('='*20)

        # get user selection
        user_selection = int(input('Enter image number:'))

        # generate ascii art of user selected image
        print("Generating ascii art from {}.....".format(images[user_selection]))
        create_ascii(images[user_selection])
        if(image_dimensions):
            #print results to terminal
            print_results(images[user_selection])
        main_menu()

def generate_grayscale_ascii():
    # create list of images in image directory
    images = generate_image_list(image_dir)

    #Check if images is empty
    if(len(images) == 0):
        print('Please add images to Images directory before running program.')
    else:
        # print list of images for user selection
        print('='*20)
        print('#'*6 + ' Images ' + '#'*6)
        print('='*20)
        for key, value in images.items():
            print('{} : {}'.format(key,value))
        print('='*20)

        # get user selection
        user_selection = int(input('Enter image number:'))

        # generate ascii art of user selected image
        print("Generating ascii art from {}.....".format(images[user_selection]))
        create_grayscale_ascii(images[user_selection])
        if(image_dimensions):
            #print results to terminal
            print_results(images[user_selection])
        main_menu()

# resize menu
def resize_menu():
    print('='*20)
    print('#'*6 + ' Resize ' + '#'*6)
    print('='*20)

    if(image_dimensions):
        print('Current image dimensions: ({},{})'.format(image_dimensions[0],image_dimensions[1]))
    print('='*20)
    dimensions = input('Input new dimensions separated by a comma, ex: x,y : ')
    dimensions = dimensions.split(',')

    if(len(dimensions) == 2):
        set_image_dimensions((int(dimensions[0]), int(dimensions[1])))
        print('New image dimensions: ({},{})'.format(image_dimensions[0],image_dimensions[1]))
    else:
        print('Image will not be resized')
        set_image_dimensions(None)

    main_menu()

# art style menu
def art_menu():
    print('='*20)
    print('#'*4 + ' Processing ' + '#'*4)
    print('='*20)
    print('Select Image Processing: ')
    print('1 : Monochrome')
    print('2 : Grayscale')
    print('9 : Back')
    print('0 : Exit')
    print('='*20)
    choice = input('Enter Selection: ')
    if choice == '1':
        generate_ascii()
    elif choice == '2':
        generate_grayscale_ascii()
    elif choice == '9':
        main_menu()
    elif choice == '0':
        exit()
    else:
        print('Please enter selection from menu options')
        art_menu()

# view menu
def view_menu():
    # create list of images in image directory
    images = generate_image_list(output_dir)

    #Check if images is empty
    if(len(images) == 0):
        print('Please add images to Images directory before running program.')
    else:
        # print list of images for user selection
        print('='*20)
        print('#' + ' Generated Images ' + '#')
        print('='*20)
        for key, value in images.items():
            print('{} : {}'.format(key,value))
        print('='*20)

        # get user selection
        user_selection = int(input('Enter image number:'))
        print('** ' + images[user_selection] + ' **')
        print_results(images[user_selection])
        main_menu()

# Character list menu
def char_menu():
    print('='*20)
    print('#' + ' Character Lists  ' + '#')
    print('='*20)

    print('1 : Change Monochrome List')
    print('2 : Change Grayscale List')
    print('9 : Back')
    print('='*20)
    choice = input('Enter Selection: ')
    # Monochrome
    if choice == '1':
        print('Current Monochrome List:')
        print(''.join(mono_chars))
        new_list = input('Enter New List:')
        if len(new_list) == 2:
            update_char_list(new_list,'Monochrome')
            print('Updated list:')
            print(''.join(mono_chars))
            main_menu()
        else:
            print('Invalid Entry')
            print('Monochrome list takes two characters')
            char_menu()
    # Grayscale
    elif choice == '2':
        print('Current Grayscale List:')
        print(''.join(grayscale_chars))
        new_list = input('Enter New List:')
        if len(new_list) >= 2:
            update_char_list(new_list,'Grayscale')
            print('Updated list:')
            print(''.join(grayscale_chars))
            main_menu()
        else:
            print('Invalid Entry')
            print('Grayscale list takes at least two characters')
            char_menu()
    # Back
    else:
        main_menu()

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
    print('3 : Change Character Lists')
    print('4 : View Generated Text Files')
    print('0 : Exit')
    print('='*23)
    choice = input('Enter Selection: ')
    if choice == '1':
        art_menu()
    elif choice == '2':
        resize_menu()
    elif choice == '3':
        char_menu()
    elif choice == '4':
        view_menu()
    elif choice == '0':
        exit()
    else:
        print('Please enter selection from menu options')
        main_menu()

#print ascii art to terminal
def print_results(filename):
    filename = strip_extension(filename)
    text_file = open(output_dir + filename + '.txt', 'r')
    output = text_file.read()
    print(output)
    text_file.close()

#exit program
def exit():
    sys.exit()


##### Main #####
if __name__ == '__main__':
    main_menu()
