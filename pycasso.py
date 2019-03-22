from PIL import Image, ImageDraw
from random import randint
import argparse
import sys

class Point:
    def __init__(self, maxX, maxY):
        self.x = randint(0,maxX)
        self.y = randint(0,maxY)
        self.radius = randint(10,50)
        self.r = randint(0,255)
        self.g = randint(0,255)
        self.b = randint(0,255)

    def setRadius(self, radius):
        self.radius = radius
    
    def setColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def changePos(self, x, y):
        self.x = x
        self.y = y


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

def generateImage(imageTarget, generations, numberdots):
    generation = 0
    width, height = imageTarget.size
    allPoints = [Point(width,height) for i in range(numberdots)]



    while (generation != generations):
        print_same_line("Generation number: " + str(generation))
        generation += 1
        newImage = ImageDraw.Draw(imageTarget)
        for point in allPoints:
             newImage.ellipse([point.x-point.radius,point.y-point.radius,point.x+point.radius,point.y+point.radius],outline=(point.r,point.g,point.b),fill=(point.r,point.g,point.b))
        print("pene")
        imageTarget.show()

    
   


    print("\n")
        
def pycasso(filePath, generations,numberdots):

    try:
        imageTarget = Image.open(filePath)
        imageTarget.show()
        print('The image will be painted with ' + str(numberdots) + ' dots.\n')
        generateImage(imageTarget,generations,numberdots)
    except IOError:
        print("Couldn't open the file")
        exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=None, required=True, help='Path to find the image')
    parser.add_argument('--numbergenerations', default=1, required=False,help='Number of generations the program will make')
    parser.add_argument('--numberdots', default=1000,required=False, help='Number of dots to generate the image')
    args = parser.parse_args()
    pycasso(args.path, args.numbergenerations,args.numberdots)



main()
