# the screen is 360 characters wide and 90 characters high
# my settings: 
# so then 236 characters fit onto the screen (width) and 133 down (hight)
# the file I'll be testing is: C:\Users\torbi\OneDrive\Desktop\Programming_projects\video-to-ascii\clip.mp4
# the testimage file is here: C:\Users\torbi\OneDrive\Desktop\Programming_projects\video-to-ascii\image.png

# cmd has to be set to width: 612 and hight: 123 and font size 7 with corier new

import os
import time
import cv2
import pathlib
import math
# from PIL import Image
from PIL import Image

charValues = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
charString = [" ", " ", ".", ",", ":", "*", "°", "-", "÷", "(", "{", "x", "m", "±", "o", "¤", "O", "§", "¥", "#", "@",  ]

def GetFrame(filename):
    
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    count = 0

    # get frame count
    while success:
        # PixelToTextConverter(filename, image) # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
        success, image = vidcap.read()
        count += 1
    vidcap.release()

    line_length = 55
    print(f"[{'.'*(line_length-1)}]", end="\r")
    
    percentage = 0

    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()

    # put the progress thing here
    for c, i in enumerate(range(count)):
        print(f"[{'#' * math.ceil(line_length * percentage)}{'-' * math.ceil(line_length * (1-percentage))}]   {i + 1}/{count}", end="\r")
        percentage = (c / count)

        cv2.imwrite("frame%d.jpg" % i, image)  

        PixelToTextConverter(filename, i, image)
        success,image = vidcap.read()  

def PixelToTextConverter(filename, i, frame):
    
    size = (442 , 123)
    outfileString = ""
    pixelValue = 0
  
    im = Image.open("frame%d.jpg" % i).convert('L')
    # im.thumbnail(size, Image.Resampling.LANCZOS)
    im = im.resize(size)
    
    for y in range(123):
        for x in range(442):

            pixelValue = im.getpixel((x, y))
            percent = int((pixelValue / 255) * 100)
            closest_value = min(charValues, key=lambda x: abs(percent - x))
            index = charValues.index(closest_value)
            outfileString += charString[index]

        outfileString += "\n"

    im.close()
    os.remove("frame%d.jpg" % i)
    
    WriteToFile(os.path.basename(filename).split('/')[-1], outfileString)

def WriteToFile(saveIntoFilename, content):

    saveIntoFilename += "-lowquality.txt"

    file = open(saveIntoFilename, "a")
    file.write(content)
    file.write("DAVID\n") # here do something to differentiate from the different frames
    file.close()

def ShowVideo(filename):

    file = open(filename, "r")
    frames = file.read().split("DAVID")

    os.system('cls')
    for frame in frames:
        print("\033[H\033[xJ", end="")
        print(frame)
        time.sleep(0.03)

def main():

    while True:
        filename = input("Select a file to convert: ")
        print(pathlib.Path(filename).suffix)
        if (os.path.exists(filename) and pathlib.Path(filename).suffix != '.txt'):
            GetFrame(filename)
            result = str(os.path.basename(filename).split('/')[-1] + "-lowquality.txt")
            ShowVideo(result)
            break
        elif (pathlib.Path(filename).suffix == '.txt'):
            ShowVideo(filename)
            break

if __name__ == "__main__":
    main()

"""
cls 
venv\\Scripts\\activate 
python main.py 
sex-now.mp4

"""