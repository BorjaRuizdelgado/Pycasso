from PIL import Image, ImageDraw
import argparse
import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setRadius(self, radius):
        self.radius = radius
    
    def setColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

def generateImage(imageTarget, generations):
    generation = 1
    while (generation != generations):
        print_same_line("Generation number: " + str(generation))
        generation += 1
    
    #good shit to print points over an image
    point = Point(300,300)
    point.setRadius(50)
    point.setColor(255,0,0)

    newImage = ImageDraw.Draw(imageTarget)
    newImage.ellipse([point.x-point.radius,point.y-point.radius,point.x+point.radius,point.y+point.radius],outline=(point.r,point.g,point.b),fill=(point.r,point.g,point.b))
    imageTarget.show()


    print("\n")
        
def pycasso(filePath, generations):

    try:
        imageTarget = Image.open(filePath)
        imageTarget.show()
        generateImage(imageTarget,generations)
    except IOError:
        print("Couldn't open the file")
        exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=None, required=True, help='Path to find the image')
    parser.add_argument('--numbergenerations', default=1000, required=False,help='Number of generations the program will make')
    args = parser.parse_args()
    pycasso(args.path, args.numbergenerations)



main()
