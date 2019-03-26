from PIL import Image, ImageDraw
from random import randint
import argparse
import sys
import numpy
from operator import itemgetter

positionMutationChanace = 20
colorMutationChanace = 20
radiusMutationChanace = 2

class Point:
    def __init__(self, maxX, maxY):
        self.maxSizeX = maxX
        self.maxSizeY = maxY
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

    def mutate(self):
        if(randint(0,100) <= colorMutationChanace):
            self.r = randint(0,255)
            self.g = randint(0,255)
            self.b = randint(0,255)

        if(randint(0,100) <= radiusMutationChanace):
            self.radius = randint(10,50)
            
        if(randint(0,100) <= positionMutationChanace):
            self.x = randint(0,self.maxSizeX)
            self.y = randint(0,self.maxSizeY)

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

    def mutatePic(self):
        for p in self.points:
            p.mutate()

    def getPoints(self):
        return self.points
    
    def setPoints(self, points):
        self.points = points
    
    def getSize(self):
        return self.size

    

class Population:
    def __init__(self, size, numberdots, populationSize, originalImage):
        self.originalImage = originalImage
        self.pictures = [Picture(size, numberdots) for i in range(populationSize)]
    
    def crossover(self):
        scoredPopulation = self.scorePopulation()
        scoredPopulationSorted = sorted(scoredPopulation,key=itemgetter(1), reverse=True)
        newPopulation = [a[0] for a in scoredPopulationSorted[:int((len(scoredPopulationSorted)+1)/2)]]
        print("\n")
        for a in scoredPopulationSorted:
            print(a[1])

        for i in range(0, len(newPopulation), 2):
            newPc = self.sex(newPopulation[i], newPopulation[i+1])
            newPc.mutatePic()
            newPopulation.append(newPc)
            newPc = self.sex(newPopulation[i], newPopulation[i+1])
            newPc.mutatePic()
            newPopulation.append(newPc)


        print(len(newPopulation))
        self.pictures = newPopulation[:len(scoredPopulation)]
        self.best = newPopulation[0]

        
    def scorePopulation(self):
        scoredPopulation = []
        
        for picture in self.pictures:
            punctuation = picture.fitness(self.originalImage)
            scoredPopulation.append((picture,punctuation))

        return scoredPopulation

    def getBest(self):
        return self.best
    
    def sex(self, first, second):
        newPoints = []
        firstPoints = first.getPoints()
        secondPoints = second.getPoints()
        for i in range(len(firstPoints)):
            if(randint(1,2) == 2):
                newPoints.append(firstPoints[i])
            else:
                newPoints.append(secondPoints[i])
        newPic = Picture(first.getSize(), len(newPoints))
        newPic.setPoints(newPoints)
        return newPic



def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()



def generateImage(imageTarget, generations, numberdots, populationSize):
    generation = 0
    population = Population(imageTarget.size,numberdots,populationSize,imageTarget)

    while (generation != generations):
        print_same_line("Generation number: " + str(generation))
        generation += 1
        population.crossover()
    
    population.getBest().composeImage().show()


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
    parser.add_argument('--numbergenerations', default=100, required=False,help='Number of generations the program will make')
    parser.add_argument('--numberdots', default=500,required=False, help='Number of dots to generate the image')
    parser.add_argument('--populationsize', default=12,required=False, help='Size of the population')
    args = parser.parse_args()
    pycasso(args)



main()
