from PIL import Image, ImageDraw
from random import randint
import argparse
import sys
import numpy
from operator import itemgetter
from copy import deepcopy

colors = []



class Point:
    def __init__(self, maxX, maxY):
        self.maxSizeX = maxX
        self.maxSizeY = maxY
        self.x = randint(0, maxX)
        self.y = randint(0, maxY)
        self.radius = randint(1, 25)
        self.color = colors[randint(0, (len(colors) - 1))]

    def mutate(self):
        if randint(1,200) == 1:
            self.color = colors[randint(0, (len(colors) - 1))]

        if randint(1,200) == 2:
            self.radius = randint(1, 25)

        if randint(1,200) == 3:
            self.x = randint(0,self.maxSizeX)
            self.y = randint(0,self.maxSizeY)

            
        


class Picture:
    def __init__(self, size, numberdots, assignRandom):
        self.size = size
        width, height = size
        if assignRandom == 1:
            self.points = [Point(width, height) for i in range(numberdots)]

    def composeImage(self):
        newImage = Image.new("RGB", self.size, (255, 255, 255))
        canvas = ImageDraw.Draw(newImage)
        for point in self.points:
            canvas.ellipse(
                [point.x - point.radius, point.y - point.radius, point.x + point.radius, point.y + point.radius],
                outline=point.color, fill=point.color)
        return newImage

    # from STACK OVERFLOW need a new fitness function
    def fitness(self, image2):
        # Convert Image types to numpy arrays
        i1 = numpy.array(self.composeImage(), numpy.int16)
        i2 = numpy.array(image2, numpy.int16)
        dif = numpy.sum(numpy.abs(i1 - i2))
        return (dif / 255.0 * 100) / i1.size

    def mutatePic(self):
        for p in self.points:
            p.mutate()

    def getPoints(self):
        return self.points

    def setPoints(self, points):
        self.points = deepcopy(points)

    def getSize(self):
        return self.size


class Population:
    def __init__(self, size, numberdots, populationSize, originalImage):
        self.originalImage = originalImage
        self.pictures = [Picture(size, numberdots, 1) for i in range(populationSize)]

    def crossover(self):
        scoredPopulation = self.scorePopulation()
        scoredPopulationSorted = sorted(scoredPopulation, key=itemgetter(1))
        allPics = [a[0] for a in scoredPopulationSorted]
        firstHalf = allPics[:int((len(allPics) + 1) / 2)]
        print(scoredPopulation[0][1])

        for i in range(0, len(firstHalf)):
            newPic = self.mix(firstHalf[i], allPics[randint(0, len(allPics) - 1)])
            newPic.mutatePic()
            firstHalf.append(newPic)

        self.pictures = firstHalf[:len(scoredPopulation)]
        self.best = deepcopy(firstHalf[0])

    def scorePopulation(self):
        scoredPopulation = []

        for picture in self.pictures:
            punctuation = picture.fitness(self.originalImage)
            scoredPopulation.append((picture, punctuation))

        return scoredPopulation

    def getBest(self):
        return self.best

    def mix(self, first, second):
        newPoints = []
        firstPoints = first.getPoints()
        secondPoints = second.getPoints()
        for i in range(len(firstPoints)):
            if i% 10 <= 5:
                newPoints.append(firstPoints[i])
            else:
                newPoints.append(secondPoints[i])
        newPic = Picture(first.getSize(), len(newPoints), 0)
        newPic.setPoints(newPoints)
        return newPic


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


def generateImage(imageTarget, generations, numberDots, populationSize):
    generation = 0
    population = Population(imageTarget.size, numberDots, populationSize, imageTarget)

    while (generation != generations):
        print("Generation number: " + str(generation))
        generation += 1
        population.crossover()
        if generation % 200 == 0:
            population.getBest().composeImage().save(".\\generateLisa\\image"+str(generation)+".jpg")
            
    population.getBest().composeImage().save("image"+str(randint(0,1000))+".jpg")

    print("\n")


def pycasso(args):
    try:
        print(args)
        imageTarget = Image.open(args.path)
        # imageTarget.show()
        allColors = imageTarget.getcolors(imageTarget.size[0] * imageTarget.size[1])
        global colors
        colors = [a[1] for a in sorted(allColors, key=itemgetter(1), reverse=True)]
        print('The image will be painted with ' + str(args.numberdots) + ' dots.\n')
        generateImage(imageTarget, args.numbergenerations, args.numberdots, args.populationsize)
    except IOError:
        print("Couldn't open the file")
        exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=None, required=True, help='Path to find the image')
    parser.add_argument('--numbergenerations', default=100, type=int, required=False,
                        help='Number of generations the program will make')
    parser.add_argument('--numberdots', default=400, type=int, required=False,
                        help='Number of dots to generate the image')
    parser.add_argument('--populationsize', default=90, type=int, required=False, help='Size of the population')
    args = parser.parse_args()
    pycasso(args)


main()
