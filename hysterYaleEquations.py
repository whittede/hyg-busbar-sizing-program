# First version of script written by Ethan Whitted - ewhitted17@georgefox.edu
# Last modified by Ethan Whitted (ewhitted17@georgfox.edu) on 26-4-2021
# A script to take values from CSV files and calculate using interpolation the
# current ampacities and cross-sectional areas for busbars of different
# geometries.
#
# Both the calculateArea and calculateAmp method return negative numbers to
# indicate errors:
# # -1 indicates the inputted ampacity/cross-sectional area was above the range
# # # of tested values in the CSV sheet.
# # -2 indicates the inputted ampacity/cross-sectional area was below the range
# # # of tested values in the CSV sheet.
# # -3 a CSV file with the title including the given numbers for folds and bends
# # # was not found.
# # Any higher negative number (such as -99) indicates a general error occured
# # # that was unaccounted for.

import csv
from collections import OrderedDict

# The function for calculating the cross-sectional area of a busbar that will
# stay under 90°C given a maximum amount of electrical amps running through it.
# Looks at the CSV that contains the experimental data for the specific busbar
# geometry and then uses the Linear Interpolation Formula to interpolate what
# the area would be based on the two real busbars tested with the closest
# electrical ampacities above and below the inputted value.
def calculateArea(inputAmp, bends, folds):
    try:
        # Each geometry has a different set of data, so open the correct file
        csvFile = "busbar-data-{0}folds-{1}bends.csv".format(folds, bends)
        try:
            with open(csvFile, mode='r') as csvFile:
                csvReader = csv.reader(csvFile, delimiter=',')
                rowCount = 0
                xAreaAmpDict = {}
                # Put all of the cross-sectional area values and ampacity values
                # into a dictionary of form {xArea:ampacity, xArea:ampacity, ...}
                for row in csvReader:
                    if rowCount > 0:
                        xAreaAmpDict[float(row[0])] = float(row[1])
                    rowCount += 1

                # Insert the user-inputted value into the dictionary
                xAreaAmpDict['unknown'] = float(inputAmp)

                # Sort the dictionary by ascending order of the ampacity values.
                sortedDict = OrderedDict(sorted(xAreaAmpDict.items(), key=lambda x: x[1]))

                # From our data, get the two cross-sectional areas & ampacities above
                # and below the inputted value.
                location = list(sortedDict.keys()).index("unknown")
                cannotInterpolate = False
                previousVal = None
                nextVal = None
                dictList = list(sortedDict.items())
                if (location != 0):
                    try:
                        previousVal = dictList[location-1]
                        nextVal = dictList[location+1]
                    except IndexError:
                        cannotInterpolate = True
                        previousVal = dictList[location-1]
                        # Returning a -1 indicates this amapacity is above all the values in the csv file
                        outputArea = -1
                        return outputArea

                elif (location == 0):
                    cannotInterpolate = True
                    nextVal = dictList[location+1]
                    # Returning a -2 indicates this amapacity is below all the values in the csv file
                    outputArea = -2
                    return outputArea

                # Use the Linear Interpolation Equation to interpolate the value
                # of the cross-sectional area for a bar with the inputted ampacity.
                if (cannotInterpolate == False):
                    part1 = (nextVal[0] - previousVal[0])/(nextVal[1] - previousVal[1])
                    outputArea = (part1*(inputAmp - previousVal[1])) + previousVal[0]
                    return outputArea
        except FileNotFoundError:
            return -3
    except Exception as e:
        print(e)
        return -99

# The function for calculating the maximum electrical current of a busbar that
# will stay under 90°C given the bar is a specific cross-sectional area in size.
# Looks at the CSV that contains the experimental data for the specific busbar
# geometry and then uses the Linear Interpolation Formula to interpolate what
# the current would be based on the two real busbars tested with the closest
# cross-sectional areas above and below the inputted value.
def calculateAmp(inputArea, bends, folds):
    try:
        csvFile = "busbar-data-{0}folds-{1}bends.csv".format(folds, bends)
        try:
            with open(csvFile, mode='r') as csvFile:
                csvReader = csv.reader(csvFile, delimiter=',')
                #print(list(csvReader))
                rowCount = 0
                xAreaAmpDict = {}
                # Put all of the cross-sectional area values and ampacity values
                # into a dictionary of form {ampacity:xArea, ampacity:xArea, ...}
                for row in csvReader:
                    if rowCount > 0:
                        xAreaAmpDict[float(row[1])] = float(row[0])
                    rowCount += 1

                # Insert the user-inputted value into the dictionary
                xAreaAmpDict["unknown"] = float(inputArea)

                # Sort the dictionary by ascending order of the ampacity values.
                sortedDict = OrderedDict(sorted(xAreaAmpDict.items(), key=lambda x: x[1]))

                # From our data, get the two cross-sectional areas & ampacities above
                # and below the inputted value.
                location = list(sortedDict.keys()).index("unknown")
                cannotInterpolate = False
                previousVal = None
                nextVal = None
                dictList = list(sortedDict.items())
                if (location != 0):
                    try:
                        previousVal = dictList[location-1]
                        nextVal = dictList[location+1]
                    except IndexError:
                        cannotInterpolate = True
                        previousVal = dictList[location-1]
                        # Returning a -1 indicates this cross-sectional area is above all the values in the csv file
                        outputAmp = -1
                        return outputAmp

                elif (location == 0):
                    cannotInterpolate = True
                    nextVal = dictList[location+1]
                    # Returning a -2 indicates this cross-sectional area is below all the values in the csv file
                    outputAmp = -2
                    return outputAmp

                # Use the equation to interpolate the value of the cross-sectional
                # area for a bar with the inputted ampacity.
                # val[0] is the cross-sectional area and val[1] is the ampacity.
                if (cannotInterpolate == False):
                    part1 = (nextVal[0] - previousVal[0])/(nextVal[1] - previousVal[1])
                    outputAmp = (part1*(inputArea - previousVal[1])) + previousVal[0]
                    return outputAmp
        except FileNotFoundError:
            return -3
    except Exception as e:
        print(e)
        return -99

# Convert different units to all be in either meters or meters².
# 'inputUnits' is a String of the units the inputted value is in
# 'inputValue' is the actual number being worked with
# 'outputUnits' is a String of the desired type of unit to be converted to
def convertUnits(inputUnits, inputValue, outputUnits):

    # Conversions for millimeters
    if (inputUnits == "mm"):
        if (outputUnits == "mm"):
            outputValue = (inputValue)
        elif (outputUnits == "cm"):
            outputValue = (inputValue/10)
        elif (outputUnits == "m"):
            outputValue = (inputValue/1000)
        elif (outputUnits == "in"):
            outputValue = (inputValue*0.039370)

    # Conversions for centimeters
    elif (inputUnits == "cm"):
        if (outputUnits == "mm"):
            outputValue = (inputValue*10)
        elif (outputUnits == "cm"):
            outputValue = (inputValue)
        elif (outputUnits == "m"):
            outputValue = (inputValue/100)
        elif (outputUnits == "in"):
            outputValue = (inputValue*0.39370)

    # Conversions for meters
    elif (inputUnits == "m"):
        if (outputUnits == "mm"):
            outputValue = (inputValue*1000)
        elif (outputUnits == "cm"):
            outputValue = (inputValue*100)
        elif (outputUnits == "m"):
            outputValue = (inputValue)
        elif (outputUnits == "in"):
            outputValue = (inputValue*39.370)

    # Conversions for inches
    elif (inputUnits == "in"):
        if (outputUnits == "mm"):
            outputValue = (inputValue/0.039370)
        elif (outputUnits == "cm"):
            outputValue = (inputValue/0.39370)
        elif (outputUnits == "m"):
            outputValue = (inputValue/39.370)
        elif (outputUnits == "in"):
            outputValue = (inputValue)


    # Conversions for square millimeters
    if (inputUnits == "mm²"):
        if (outputUnits == "mm²"):
            outputValue = (inputValue)
        elif (outputUnits == "cm²"):
            outputValue = (inputValue/100)
        elif (outputUnits == "m²"):
            outputValue = (inputValue/1000000)
        elif (outputUnits == "in²"):
            outputValue = (inputValue/645.16)

    # Conversions for square centimeters
    if (inputUnits == "cm²"):
        if (outputUnits == "mm²"):
            outputValue = (inputValue*100)
        elif (outputUnits == "cm²"):
            outputValue = (inputValue)
        elif (outputUnits == "m²"):
            outputValue = (inputValue/10000)
        elif (outputUnits == "in²"):
            outputValue = (inputValue/6.4516)

    # Conversions for square meters
    if (inputUnits == "m²"):
        if (outputUnits == "mm²"):
            outputValue = (inputValue*1000000)
        elif (outputUnits == "cm²"):
            outputValue = (inputValue/10000)
        elif (outputUnits == "m²"):
            outputValue = (inputValue)
        elif (outputUnits == "in²"):
            outputValue = (inputValue*1550)

    # Conversions for square inches
    if (inputUnits == "in²"):
        if (outputUnits == "mm²"):
            outputValue = (inputValue*645.16)
        elif (outputUnits == "cm²"):
            outputValue = (inputValue*6.4516)
        elif (outputUnits == "m²"):
            outputValue = (inputValue/1550)
        elif (outputUnits == "in²"):
            outputValue = (inputValue)

    return float(outputValue)
