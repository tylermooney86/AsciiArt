
Ascii Art Generator
========================

About
-----
This program allows users to generate custom ascii art text files from an image.
- Load an image to the Images directory
- Run the program in the terminal
- Select the image
- generate ascii art
- adjust parameters and image processing values from settings until you get desired output

Example Output
----------

![alt text](https://raw.githubusercontent.com/tylermooney86/AsciiArt/master/ExampleImages/python.png)

![alt text](https://raw.githubusercontent.com/tylermooney86/AsciiArt/master/ExampleImages/Obama.png)

![alt text](https://raw.githubusercontent.com/tylermooney86/AsciiArt/master/ExampleImages/mario.png)

![alt text](https://raw.githubusercontent.com/tylermooney86/AsciiArt/master/ExampleImages/marioIG.png)

To run the program:
-------
Clone the Repository

In a terminal type: "python ascii.py" (Language: Python3: Dependencies: PIL)

Menus 
---------
### Select Image:
   - prints a list of images stored in images folder
### Generate Ascii Art:
   - Two output modes:
       - Monochrome: uses two char to render image
       - Grayscale: uses many char to render image
### Settings:
   - Character Lists:
       - Change Character List:
           - Customize character lists used to render ascii art
           - Do not separate characters
               - I recommend using smaller character sets for grayscale set and dont for get the space(' ')
            - Monochrome only takes two characters in the order they are entered
            - Grayscale takes many characters and orders them by density of the character
       - Invert Character List:
           - Reverses the order of the characters in character list
   - Dimensions:
       - Change dimensions of output
            - input should be in the form: width,height (ie: 80,40 or characters,lines)
            - entering an incorrectly formatted value will cause program to use input image's dimensions
   - Brightness/Contrast:
        - Takes float values:
            - 1.0 = no brightness/contrast Change
            - 0.0 = black image
            - 1.0+ = high contrast/Brightness
            - not a number = None
### View Generated Images:
   - Prints selected text file to console


