'''
    this code is based on:
        https://www.askpython.com/python/examples/turn-images-to-ascii-art-using-python
        https://github.com/mdq3/terminal-animation

    you can set the aspectratio of the gennerated ascii image
        by changing the value of "scale = " in def scale(image)
    it hase a blach and white mode
        you can set the thresh hold

    it workes by:
    converting all Images in a folder to asci.txt images and saves them in a folder.
        it doas so by asii() and scale()
    then it adds all Images to a animation file.py calles ohmy.py
        it doas so by calling ohmy()
'''

import PIL.Image
import os
import shutil

inputT = False                                              # to setup via terminal
# Settings:
directory = "/home/lhl/Downloads/new"                     # directory in which images to conert are stored
new_width = 130                                             # amaunt of characters used to show x(width) of animation
scale = 2                                                   # animation ratio y(heith) is 1 x(width) is set here. scale =2 will be 2:1 ration
filename = "/home/lhl/Documents/bash/asci/ascii_imageX.txt" # folder and filename where asci-frames are stored kepp the "X" bc it will be replaced with the frame number
wtsaa = "/home/lhl/Documents/bash/ohmy.py"                  # wehre to save asci animation
doBW = False                                                # sets black whihte conversion mode
th = 45                                                     # threshold on which a character is black
inv = False                                                 # invert colors
if inv:                                                     # characters used for inverted colors
    chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]
    black = "@"
    white = " "
else:                                                       # characters used for non inverted colors
    chars = [" ", "·", ":", ",", "-", "~", ";", "i", "U", "%", "@"]
    black = " "
    white = "@"

def scal(image):
    im = PIL.Image.open(image)
    width, height = im.size                     # gets image size date
    #print ("width is: ", width)                 # debugging
    #print ("hight is: ", height)                # debugging

# calculate size of croped image
    new_hight = width/scale                     # new scale y

# calculates center of image in order to crop from the middle:
    x = width/2
    y = height/2

# calculates coordinates of where to crop image 0/0 top left corner width/height lower rifht corner
    x_Ct = 0
    x_Cb = width
    y_Ct = y - new_hight/2
    y_Cb = y + new_hight/2

# Cropped image of above dimension
    im1 = im.crop((x_Ct, y_Ct, x_Cb, y_Cb))                 # crops image d.h. cuts rectangle out
    mhh = int(round(new_width/scale*0.55))                  # mulytiply by 0.55 bc. pixels on y are spaced much more appaert then on x 
    newsize = (new_width, mhh)                              # writes new size
    im1 = im1.resize(newsize)                               # rezises image
    return(im1)                                             # returns coped and scaled image to asii(directory, count)


def asii(directory, count):
    #count = count
    for file in os.listdir(directory):                      # for objekts / files in folder do:
        image = os.path.join(directory, file)               # create absoluth path to frame which is to be converted
        if os.path.isfile(image):                           # checks if objekt in Folder is actually a file
            try:
              img = PIL.Image.open(image)                   # sest if file is aktualy there, in order to prevent error massage
              img_flag = True                               # fore above
            except:
              print(image, "Unable to find image ");        # prints "error" Message
            img = scal(image)                               # calls "scale" inorder to rezize and set aspectratio to image 
            img = img.convert('L')                          # convert image to grayscale other option would be 1 (black wite)
                        # 
            pixels = img.getdata()                          # get grayscale data in order to map characters acordingly
            if doBW:
                new_pixels = [black if pixel < th else white for pixel in pixels]       # do black white => need to uncomment new_pixels
            else:
                new_pixels = [chars[pixel//25] for pixel in pixels]                 # map grayscale data to ascii-characters
            
            new_pixels = ''.join(new_pixels)                                        # join new pixels together
            new_pixels_count = len(new_pixels)                                      # pass number of pixels
            ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]  # add pixels to ascii-frame
            ascii_image = "\n".join(ascii_image)                                    # join chrowes together
            filenam = filename.replace("X", str(count))     # crete filname based on count value
            with open(filenam, "w") as f:                   # create ascii-frame.txt
                f.write(ascii_image)                        # writes ascii-frame.txt
                #print("i got here")                         # debugging
            count +=1                                       # increase couenter
            #print (count)                                   # debigging
    return(count)

# Add characters to the beginning and end of each line
def ohmy():
    count = 1                                       # create new counter
    directory = os.path.dirname(filename)           # directory in which ascii-frame.txt's are stored
    updated_lines = []                              # declare list in which animation code will be saved
    frames = "frames = [frame1"                     # string containing all frames
    for file in os.listdir(directory):              # for objekts / ascii-frames do:
        frame = 'frameX = \\'                       # base variable to be modified acordingly to frame number used for the animation code
        txt = os.path.join(directory, file)         # creates absolut path to ascii-frames
        if os.path.isfile(txt):                     # checs if variable txt is actually a file
            with open(txt, 'r') as file:            # opens ascii-frame.txt
                lines = file.readlines()            # reads it line by line, in order to add nessecary characters in order for the animation code to work
            frame = frame.replace("X", str(count))  # creates frame name used by the animation code
            frames += (", ")+("frame")+str(count)   # adds current frame to the frame string needed for animation code
            updated_lines.append([frame])           # adds frame nuber to list
            updated_lines.append (['"' + line.rstrip() +'\\n" + \\' if index != len(lines) - 1 else '"' + line.rstrip() + '\\n"' for index, line in enumerate(lines)])  # adds ascii-frame line aling with necesarry charactars for animation code to list, also has an exeption handerler, wehn at last line of ascii-frame
            count += 1                              # increase counter by 1
    frames += "]"                                   # closes frame string 
    updated_lines.append ([frames])
    with open(wtsaa, 'w') as file:
        file.write("\n".join(["\n".join(inner) for inner in updated_lines]))

if __name__ == "__main__":
    if inputT:
        directory = input("enter Absolut path to directory in which images to conert are stored: ")
        new_width = input("how many characters should be used for x(width): ")
        scale = input ("set scale if set to 2 => 2:1; 2 => 3:1: ")
        filename = input ("folder and filename where asci-frames are stored kepp the X bc it will be replaced with the frame number: ")
        wtsaa = "/home/lhl/Documents/bash/ohmy.py"                  # wehre to save asci animation
        doBW = input("Do you want to use black and white mode [True; False]:")
        inv = input("Do you want to invert colors [True; False]: ")
        if doBW:
            inv = input("do you want to ivert B/W: True / False: ")
            th = input("what do you want the threshhold for a black character to be: ")

    img_flag = True
    ksksk = os.path.dirname(filename)

    if os.path.isdir(ksksk):
        shutil.rmtree(ksksk)                    # delete folder in wich the ascii-frames are stond
        os.makedirs(ksksk)                      # create new empty folder to store ascii-frames in
    else:
        os.makedirs(ksksk)
    
    count = 0                                   # counter, in order to name generated ascii-frames
    count = asii(directory, count)
    ohmy()                                      # creates ohmy.py <= file which contains animation data
