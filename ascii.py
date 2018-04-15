'''
# ###################
# Ascii art generator
# ###################
This program allows the user to create ascii art from an image.
It uses a simple menu system to control the parameters of
the generated image.

##### Menus #####
Select Image:
    prints a list of images stored in images folder
Generate Ascii Art:
    Two output modes:
        Monochrome: uses two char to render image
        Grayscale: uses many char to render image
Settings:
    Character Lists:
        Change Character List:
            Customize character lists used to render ascii art
            Do not separate characters
                I recommend using smaller character sets for grayscale set and dont for get the space(' ')
            Monochrome only takes two characters in the order they are entered
            Grayscale takes many characters and orders them by density of the character
        Invert Character List:
            Reverses the order of the characters in character list
    Dimensions:
        Change dimensions of output
            input should be in the form: width,height (ie: 80,40 or characters,lines)
            entering an incorrectly formatted value will cause program to use input image's dimensions
    Brightness/Contrast:
        Takes float values:
            1.0 = no brightness/contrast Change
            0.0 = black image
            >1.0 = high contrast/Brightness
            not a number = None
View Generated Images:
    Prints selected text file to console

'''
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from os import listdir
import sys
import string
import collections
'''
# ################
# Global Variables
# ################
'''
image_dimensions = (80,40)
font = ImageFont.load_default()
image_dir = 'Images/'
output_dir = 'AsciiArt/'
selected_image = None
contrast = None
brightness = None

'''
# ############
#  Functions
# ############
'''

# check density of char for sorting
def char_density(c, font=font):
    image = Image.new('1', font.getsize(c), color=255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), c, font=font)
    return collections.Counter(image.getdata())[0] #0 is black

# Default character lists
mono_chars = '$ '
grayscale_chars = list(sorted(string.ascii_letters + string.digits + string.punctuation + ' ', key=char_density, reverse=True))

# load image using name
def load_image(img_name):
    image = Image.open(image_dir + img_name)

    if image_dimensions is not None:
        image = image.resize(image_dimensions, Image.ANTIALIAS)
    if contrast is not None:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if brightness is not None:
        image = ImageEnhance.Brightness(image).enhance(brightness)

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
        mono_chars = list(new_list)
    else:
        grayscale_chars = list(sorted(new_list, key=char_density, reverse=True))

#print ascii art to terminal
def print_results(filename):
    filename = strip_extension(filename)
    text_file = open(output_dir + filename + '.txt', 'r')
    output = text_file.read()
    print(output)
    text_file.close()

# set brightness
def set_brightness(b):
    global brightness
    brightness = b

# set contrast
def set_contrast(c):
    global contrast
    contrast = c

# reverse order of character list
def invert_character_list(ch = 'Grayscale'):
    global mono_chars, grayscale_chars
    if ch == 'Monochrome':
        mono_chars = mono_chars[::-1]
    else:
        grayscale_chars = grayscale_chars[::-1]

#exit program
def exit():
    sys.exit()

'''
# #############
#     ascii
# #############
'''
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
def generate_ascii(image_filter='Grayscale'):
    if selected_image == None:
        select_image_menu()
    else:
        # generate ascii art of user selected image
        print("Generating ascii art from {}.....".format(selected_image))
        if(image_filter == 'Monochrome'):
            create_ascii(selected_image)
        else:
            create_grayscale_ascii(selected_image)
        if(image_dimensions):
            #print results to terminal
            print_results(selected_image)
        main_menu()

'''
# ##############
#     Menus
# ##############
'''
def select_image_menu():
    global selected_image
    print('='*32)
    print('#' + ' '*8 + ' Select Image ' + ' '*8 + '#')
    print('='*32)
    # create list of images in image directory
    images = generate_image_list(image_dir)

    #Check if images is empty
    if(len(images) == 0):
        print('Please add images to Images directory before running program.')
    else:
        for key, value in images.items():
            print('{} : {}'.format(key,value))
        print('='*32)

        # get user selection
        user_selection = int(input('Enter Selection: '))
        if user_selection == 0:
            exit()
        elif user_selection < 1 or user_selection > len(images):
            print('Invalid Selection')
            select_image_menu()
        else:
            selected_image = images[user_selection]
            print('Current Selected Image: ' + selected_image)
        main_menu()

# resize menu
def resize_menu():
    print('='*32)
    print('#' + ' '*11 + ' Resize ' + ' '*11 + '#')
    print('='*32)

    if(image_dimensions):
        print('Current image dimensions: ({},{})'.format(image_dimensions[0],image_dimensions[1]))
    print('='*32)
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
    print('='*32)
    print('#' + ' '*9 + ' Processing ' + ' '*9 + '#')
    print('='*32)
    print('Select Image Processing: ')
    print('1 : Monochrome')
    print('2 : Grayscale')
    print('9 : Back')
    print('='*32)
    choice = input('Enter Selection: ')
    if choice == '1':
        generate_ascii('Monochrome')
    elif choice == '2':
        generate_ascii('Grayscale')
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
        print('='*32)
        print('#' + ' '*7 + 'Generated Images' + ' '*7 + '#')
        print('='*32)
        for key, value in images.items():
            print('{} : {}'.format(key,value))
        print('='*32)

        # get user selection
        user_selection = int(input('Enter image number:'))
        print('** ' + images[user_selection] + ' **')
        print_results(images[user_selection])
        main_menu()

# Character list menu
def char_menu():
    print('='*32)
    print('#' + ' '*7 + 'Character Lists ' + ' '*7 + '#')
    print('='*32)

    print('1 : Change Monochrome List')
    print('2 : Change Grayscale List')
    print('3 : Invert Character List')
    print('9 : Back')
    print('='*32)
    choice = input('Enter Selection: ')
    # Monochrome
    if choice == '1':
        print('='*32)
        print('Current Monochrome List:')
        print(''.join(mono_chars))
        print('='*32)
        new_list = input('Enter New List:')
        print('='*32)
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
        print('='*32)
        print('Current Grayscale List:')
        print(''.join(grayscale_chars))
        print('='*32)
        new_list = input('Enter New List:')
        print('='*32)
        if len(new_list) >= 2:
            update_char_list(new_list,'Grayscale')
            print('Updated list:')
            print(''.join(grayscale_chars))
            main_menu()
        else:
            print('Invalid Entry')
            print('Grayscale list takes at least two characters')
            char_menu()
    elif choice == '3':
        print('='*32)
        print('1 : Invert Monochrome List')
        print('2 : Invert Grayscale List')
        print('9 : Back')
        print('='*32)
        invert_choice = input('Enter Selection: ')
        print('='*32)
        if invert_choice == '1':
            invert_character_list('Monochrome')
            print('Updated list:')
            print(''.join(mono_chars))
            main_menu()
        elif invert_choice == '2':
            invert_character_list()
            print('Updated list:')
            print(''.join(grayscale_chars))
            main_menu()
        elif invert_choice == '9':
            settings_menu()
        else:
            print('Invalid Selection')
            char_menu()
    # Back
    else:
        main_menu()

# brightness Menu
def brightness_menu():
    print('='*32)
    print('#' + ' '*9 + ' Brightness ' + ' '*9 + '#')
    print('='*32)

    print('Current Brightness: {}'.format(brightness))
    choice = input('Enter Value: ')
    if choice.isdigit():
        set_brightness(float(choice))
        print('New Brightness: {}'.format(brightness))
    else:
        print('Invalid Entry')
        set_brightness(None)
    main_menu()

def contrast_menu():
    print('='*32)
    print('#' + ' '*10 + ' Contrast ' + ' '*10 + '#')
    print('='*32)

    print('Current Contrast: {}'.format(contrast))
    choice = input('Enter Value: ')
    if choice.isdigit():
        set_contrast(float(choice))
        print('New Contrast: {}'.format(contrast))
    else:
        print('Invalid Entry')
        set_contrast(None)
    main_menu()

# settings menu
def settings_menu():
    print('='*32)
    print('#' + ' '*10 + ' Settings ' + ' '*10 + '#')
    print('='*32)

    print('1 : Change Character List')
    print('2 : Set Output Dimensions')
    print('3 : Change Brightness')
    print('4 : Change Contrast')
    print('9 : Back')
    print('='*32)

    choice = input('Enter Selection: ')
    if choice == '1':
        char_menu()
    elif choice == '2':
        resize_menu()
    elif choice == '3':
        brightness_menu()
    elif choice == '4':
        contrast_menu()
    elif choice == '9':
        main_menu()
    elif choice == '0':
        exit()
    else:
        print('Please enter selection from menu options')
        main_menu()
'''
# ###########
#  Main Menu
# ###########
'''
def main_menu():
    print('='*32)
    print('#'*32)
    print('#' + ' '*30 + '#')
    print('#' + ' '*5 + 'Ascii Art Generator ' + ' '*5 + '#')
    print('#' + ' '*30 + '#')
    print('#'*32)
    print('='*32)

    print('1 : Select Image')
    print('2 : Generate Ascii Art')
    print('3 : Settings')
    print('4 : View Generated Text File')
    print('0 : Exit')
    print('='*32)

    choice = input('Enter Selection: ')
    if choice == '1':
        select_image_menu()
    elif choice == '2':
        art_menu()
    elif choice == '3':
        settings_menu()
    elif choice == '4':
        view_menu()
    elif choice == '0':
        exit()
    else:
        print('Please enter selection from menu options')
        main_menu()

##### Main #####
if __name__ == '__main__':
    main_menu()
