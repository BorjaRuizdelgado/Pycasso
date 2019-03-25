from PIL import Image, ImageDraw
from random import randint
import argparse
import sys
import numpy

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

class Picture:
    def __init__(self, size, numberdots):
        self.size = size
        width, height = size
        self.points = [Point(width,height) for i in range(numberdots)]
    
    def composeImage(self):
        newImage = Image.new("RGB",self.size,(255,255,255))
        canvas = ImageDraw.Draw(newImage)
        for point in self.points:
                canvas.ellipse([point.x-point.radius,point.y-point.radius,point.x+point.radius,point.y+point.radius],outline=(point.r,point.g,point.b),fill=(point.r,point.g,point.b))
        return newImage

    #from STACK OVERFLOW need a new fitness function
    def fitness(self, image2):
        #Convert Image types to numpy arrays
        i1 = numpy.array(self.composeImage(),numpy.int16)
        i2 = numpy.array(image2,numpy.int16)
        dif = numpy.sum(numpy.abs(i1-i2))
        return (dif / 255.0 * 100) / i1.size


class Population:
    def __init__(self, size, numberdots, populationSize):
        self.pictures = [Picture(size, numberdots) for i in range(populationSize)]
    
    def crossover(self):
        print("Crossover needs to be implemented")



def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()



def generateImage(imageTarget, generations, numberdots, populationSize):
    generation = 0
    population = Population(imageTarget.size,numberdots,populationSize)

    while (generation != generations):
        print_same_line("Generation number: " + str(generation))
        generation += 1

    
        

    print("\n")
        
def pycasso(args):

    try:
        print(args)
        imageTarget = Image.open(args.path)
        imageTarget.show()
        print('The image will be painted with ' + str(args.numberdots) + ' dots.\n')
        generateImage(imageTarget, args.numbergenerations, args.numberdots, args.populationsize)
    except IOError:
        print("Couldn't open the file")
        exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=None, required=True, help='Path to find the image')
    parser.add_argument('--numbergenerations', default=1, required=False,help='Number of generations the program will make')
    parser.add_argument('--numberdots', default=1000,required=False, help='Number of dots to generate the image')
    parser.add_argument('--populationsize', default=100,required=False, help='Size of the population')
    args = parser.parse_args()
    pycasso(args)



main()
