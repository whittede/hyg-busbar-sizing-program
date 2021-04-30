# First version of script written by Ethan Whitted - ewhitted17@georgefox.edu
# Last modified by Ethan Whitted (ewhitted17@georgfox.edu) on 26-4-2021
# A script to create a GUI into which users can input either the cross-sectional
# area of a busbar or the amount of electrical current that will be running
# through it. The GUI (using the hysterYaleEquations.py script) takes the
# inputted values and pulls from CSV files containing results from
# experimentally-validated data to output the either the amount of current that
# can be run through a busbar or the cross-sectional area it can have while
# still keeping the surface temperature of the bar under 90°C.

import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import Toplevel
from hysterYaleEquations import calculateArea
from hysterYaleEquations import calculateAmp
from hysterYaleEquations import convertUnits

# The defined options for the different option menus
X_AREA_UNITS = ["mm²","cm²","m²", "in²"] #The options that can be selected for cross-sectional area units.
LENGTH_UNITS = ["mm","cm","m", "in"] #The options that can be selected.
BEND_OPTIONS = [0, 1] #The options for the number of 90° bends in the bar.
FOLD_OPTIONS = [0, 1, 2, 3, 4] #The options for the number of 180° folds in the bar.

# Create the main window for the program.
mainWindow= tk.Tk()
mainWindow.title("Hyster-Yale software")

# Create a stylesheet that can be used to make the tabs look nice.
style_ref = ttk.Style()
guiFont = tkFont.Font(family="Helvetica", size=10)
style_ref.theme_create("guiTheme", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": "#0a154a" } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "#4355ab", "foreground": "white" },
            "map":       {"background": [("selected", "#0a154a")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )

style_ref.theme_use("guiTheme")

# Load in all the images here so that Python's garbage collection doesn't remove
# them if we put them inside the other windows.
errorIconFile = tk.PhotoImage(file="error_icon.png", width=50, height=50)
logo = tk.PhotoImage(file="logo.png", width=400, height=98)
faviconFile = tk.PhotoImage(file="ico.png")

# Set the icon for the program.
mainWindow.iconphoto(True, faviconFile)

# The function to be called to display an error to the user. The parameter
# "error" is the text that will be displayed to the user.
#
# Creates and positions a new window that displays the error.
def displayError (error):
    errorWindow = Toplevel(master=mainWindow, bg='#0a154a')
    errorWindow.title("Busbar calculation error!")
    errorWindow.rowconfigure(0, weight=1, minsize=20)
    errorWindow.columnconfigure(0, weight=1, minsize=20)
    errorWindow.columnconfigure(1, weight=1, minsize=20)
    errorText = tk.Label(master=errorWindow, text=error, font=("Helvetica", 9), bg='#0a154a', fg="white")
    errorIcon = tk.Label(master=errorWindow, image=errorIconFile, bg='#0a154a')
    errorIcon.grid(row=0, column=0, sticky="w", padx=(30,0))
    errorText.grid(row=0, column=1, sticky="e", padx=(0,30), pady=40)

# The function for outputting the cross-sectional area when the user inputs a
# maximum ampacity. Calls the calculateArea() function to do all the hard work.
def outputArea ():
    xAreaLabel1.config(text = "Error calculating X-sec. area")
    amp = maxAmpInput1.get()
    length = lengthInput1.get()
    bends = bendsDefault1.get()
    folds = foldsDefault1.get()
    lengthUnits = lengthDefault1.get()
    try:
        length = float(length)
        amp = float(amp)

        calculatedArea = calculateArea(float(amp), int(bends), int(folds))
        if (calculatedArea == -1):
            displayError("The inputted ampacity is above the currents tested experimentally.")
        elif (calculatedArea == -2):
            displayError("The inputted ampacity is below the currents tested experimentally.")
        elif (calculatedArea == -3):
            displayError("No busbars with the combination of bends and folds inputted were tested experimentally.")
        elif (calculatedArea < 0):
            displayError("There was an unknown error when trying to calculate the cross-sectional area.")
        else:
            xAreaLabel1.config(text = "Cross-sectional area: {:.3e} m²".format(calculatedArea))

    except ValueError:
        displayError("Must input a valid number for ampacity and length.")

# The function for outputting a maximum electrical current ampacity when the
# user inputs a busbar's cross-sectional area. Calls the calculateAmp() function
# to do all the hard work.
def outputAmp ():
    ampacityLabel2.config(text = "Error calculating ampacity")
    xAreaRaw = xAreaInput2.get()
    xAreaUnits = xAreaDefault.get()
    bends = bendsDefault2.get()
    folds = foldsDefault2.get()
    length = lengthInput2.get()
    try:
        # Attempt to convert the inputs to float to ensure the user inputted numbers
        length = float(length)
        xAreaUnconverted = float(xAreaRaw)
        xArea = convertUnits(xAreaUnits, xAreaUnconverted, "m²")

        calculatedAmp = calculateAmp(xArea, int(bends), int(folds))
        if (calculatedAmp == -1):
            displayError("The inputted cross-sectional area is above the busbar sizes tested experimentally.")
        elif (calculatedAmp == -2):
            displayError("The inputted cross-sectional area is below the busbar sizes tested experimentally.")
        elif (calculatedAmp == -3):
            displayError("No busbars with the combination of bends and folds inputted were tested experimentally.")
        elif (calculatedAmp < 0):
            displayError("There was an unknown error when trying to calculate the ampacity.")
        else:
            ampacityLabel2.config(text = "Ampacity: {:.3f} A".format(calculatedAmp))

    except ValueError:
        displayError("Must input a valid number for cross-sectional area and length.")

# Configure the parameters for all the rows and columns
mainWindow.columnconfigure(0, weight=1, minsize=75)
mainWindow.columnconfigure(1, weight=1, minsize=75)
mainWindow.columnconfigure(2, weight=1, minsize=75)
mainWindow.columnconfigure(3, weight=1, minsize=75)
mainWindow.rowconfigure(0, weight=1, minsize=50)
mainWindow.rowconfigure(1, weight=1, minsize=50)
mainWindow.rowconfigure(2, weight=1, minsize=50)
mainWindow.rowconfigure(3, weight=1, minsize=50)

# Create the default values for the dropdowns
xAreaDefault = tk.StringVar(mainWindow)
xAreaDefault.set(X_AREA_UNITS[0])
lengthDefault1 = tk.StringVar(mainWindow)
lengthDefault1.set(LENGTH_UNITS[0])
lengthDefault2 = tk.StringVar(mainWindow)
lengthDefault2.set(LENGTH_UNITS[0])
bendsDefault1 = tk.StringVar(mainWindow)
bendsDefault1.set(BEND_OPTIONS[0])
foldsDefault1 = tk.StringVar(mainWindow)
foldsDefault1.set(FOLD_OPTIONS[0])
bendsDefault2 = tk.StringVar(mainWindow)
bendsDefault2.set(BEND_OPTIONS[0])
foldsDefault2 = tk.StringVar(mainWindow)
foldsDefault2.set(FOLD_OPTIONS[0])

# Create the tab frames and tab controls
outerTabs = ttk.Notebook(master=mainWindow)
outerFrame1 = tk.Frame(master=outerTabs, padx=50, pady=25, bg='#0a154a')
outerFrame2 = tk.Frame(master=outerTabs, padx=50, pady=25, bg='#0a154a')

# Add the frames as tabs
outerTabs.add(outerFrame1, text='Calculate cross-sectional area')
outerTabs.add(outerFrame2, text='Calculate max ampacity')
outerTabs.pack(expand=1, fill="both")

#################################### All content below this line is for Tab 1 #################################################
# Create the objects that will go inside the outermost frame
logoLabel1 = tk.Label(master=outerFrame1, image=logo)
inputOutputFrame1 = tk.Frame(master=outerFrame1, bg='#0a154a')

# Create the objects that will go in the frame holding both inputs and outputs
inputsFrame1 = tk.Frame(master=inputOutputFrame1, width=20, height=80, borderwidth=1, relief=tk.RIDGE, pady=5, padx=72, bg='white')
outputFrame1 = tk.Frame(master=inputOutputFrame1, width=20, height=20, borderwidth=1, pady=10, bg='#0a154a')

# Create the objects that will go inside the frame holding the output and
# calculate button
calculateButton1 = tk.Button(master=outputFrame1, width=20, height=1, text='Calculate C-S Area', pady=2, command=outputArea, bg='#f4bb01',fg='#000000', font=("Helvetica", 9))
xAreaLabel1 = tk.Label(master=outputFrame1, text="Cross-sectional area:", font=("Helvetica", 9), bg='#0a154a', fg="white")

# Create all the objects that will go inside the input controls frame
lengthInput1 = tk.Entry(master=inputsFrame1, bg="#fcfcfc")
lengthLabel1 = tk.Label(master=inputsFrame1, text="Length:", font=guiFont, bg='white')
bendsLabel1 = tk.Label(master=inputsFrame1, text="Number of 90° bends:", font=guiFont, bg='white')
bendsSelect1 = tk.OptionMenu(inputsFrame1, bendsDefault1, *BEND_OPTIONS)
bendsSelect1.config(bg='white')
bendsSelect1["borderwidth"]=0
bendsSelect1["highlightthickness"]=0
bendsSelect1["menu"].config(bg="white")
foldsLabel1 = tk.Label(master=inputsFrame1, text="Number of 180° folds:", font=guiFont, bg='white')
foldsSelect1 = tk.OptionMenu(inputsFrame1, foldsDefault1, *FOLD_OPTIONS)
foldsSelect1.config(bg='white')
foldsSelect1["borderwidth"]=0
foldsSelect1["highlightthickness"]=0
foldsSelect1["menu"].config(bg="white")
lengthUnitSelect1 = tk.OptionMenu(inputsFrame1, lengthDefault1, *LENGTH_UNITS)
lengthUnitSelect1.config(bg='white')
lengthUnitSelect1["borderwidth"]=0
lengthUnitSelect1["highlightthickness"]=0
lengthUnitSelect1["menu"].config(bg="white")
maxAmpInput1 = tk.Entry(master=inputsFrame1, bg="#fcfcfc")
maxAmpLabel1 = tk.Label(master=inputsFrame1, text="Max ampacity:", font=guiFont, bg='white')

# Position the objects that will go inside the outermost frame (the window)
logoLabel1.grid(row=0, column=0, pady=5)
inputOutputFrame1.grid(row=1, column=0, sticky="w")

# Position the objects that will go in the frame holding both inputs and outputs
inputsFrame1.grid(row=0, column=0, sticky="w")
outputFrame1.grid(row=1, column=0, sticky="e")

# Position the objects that will go in the frame holding the output and button
calculateButton1.grid(row=0, column=0, sticky="w")
xAreaLabel1.grid(row=0, column=1, sticky="e", padx=60)

# Position all the objects that will go inside the input controls frame
lengthLabel1.grid(row=1, column=0, sticky="e")
lengthInput1.grid(row=1, column=1, pady=3, sticky="ew")
lengthUnitSelect1.grid(row=1, column=2, pady=3, sticky="w")
bendsLabel1.grid(row=2, column=0, sticky="e")
bendsSelect1.grid(row=2, column=1, pady=3, sticky="ew")
foldsLabel1.grid(row=3, column=0, sticky="e")
foldsSelect1.grid(row=3, column=1, pady=3, sticky="ew")
maxAmpLabel1.grid(row=4, column=0, sticky="e")
maxAmpInput1.grid(row=4, column=1, pady=3, sticky="ew")

#################################### All content below this line is for Tab 2 #################################################
# Create the objects that will go inside the outermost frame
logoLabel2 = tk.Label(master=outerFrame2, image=logo)
inputOutputFrame2 = tk.Frame(master=outerFrame2, bg='#0a154a')

# Create the objects that will go in the frame holding both inputs and outputs
inputsFrame2 = tk.Frame(master=inputOutputFrame2, width=20, height=80, borderwidth=1, relief=tk.RIDGE, pady=5, padx=72, bg="white")
outputFrame2 = tk.Frame(master=inputOutputFrame2, width=20, height=20, borderwidth=1, pady=10, bg='#0a154a')

# Create the objects that will go inside the frame holding the output and
# calculate button
calculateButton2 = tk.Button(master=outputFrame2, width=20, height=1, text='Calculate ampacity', pady=2, command=outputAmp, bg='#f4bb01',fg='#000000', font=guiFont)
ampacityLabel2 = tk.Label(master=outputFrame2, text="Ampacity:", font=guiFont, bg='#0a154a', fg="white")

# Create all the objects that will go inside the input controls frame
xAreaInput2 = tk.Entry(master=inputsFrame2, bg="#fcfcfc")
xAreaLabel2 = tk.Label(master=inputsFrame2, text="Cross-sec Area:", font=guiFont, bg="white")
lengthInput2 = tk.Entry(master=inputsFrame2, bg="#fcfcfc")
lengthLabel2 = tk.Label(master=inputsFrame2, text="Length:", font=guiFont, bg="white")
bendsSelect2 = tk.OptionMenu(inputsFrame2, bendsDefault2, *BEND_OPTIONS)
bendsSelect2.config(bg='white')
bendsSelect2["borderwidth"]=0
bendsSelect2["highlightthickness"]=0
bendsSelect2["menu"].config(bg="white")
bendsLabel2 = tk.Label(master=inputsFrame2, text="Number of 90° bends:", font=guiFont, bg="white")
foldsLabel2 = tk.Label(master=inputsFrame2, text="Number of 180° folds:", font=guiFont, bg="white")
xAreaUnitSelect2 = tk.OptionMenu(inputsFrame2, xAreaDefault, *X_AREA_UNITS)
foldsSelect2 = tk.OptionMenu(inputsFrame2, foldsDefault2, *FOLD_OPTIONS)
foldsSelect2.config(bg='white')
foldsSelect2["borderwidth"]=0
foldsSelect2["highlightthickness"]=0
foldsSelect2["menu"].config(bg="white")
xAreaUnitSelect2["highlightthickness"]=0
xAreaUnitSelect2["borderwidth"]=0
xAreaUnitSelect2["menu"].config(bg="white")
xAreaUnitSelect2.config(bg='white')
lengthUnitSelect2 = tk.OptionMenu(inputsFrame2, lengthDefault2, *LENGTH_UNITS)
lengthUnitSelect2.config(bg='white')
lengthUnitSelect2["borderwidth"]=0
lengthUnitSelect2["highlightthickness"]=0
lengthUnitSelect2["menu"].config(bg="white")

# Position the objects that will go inside the outermost frame (the window)
logoLabel2.grid(row=0, column=0, pady=5)
inputOutputFrame2.grid(row=1, column=0, sticky="w")

# Position the objects that will go in the frame holding both inputs and outputs
inputsFrame2.grid(row=0, column=0, sticky="w")
outputFrame2.grid(row=1, column=0, sticky="e")

# Position the objects that will go in the frame holding the output and button
calculateButton2.grid(row=0, column=0, sticky="w")
ampacityLabel2.grid(row=0, column=1, sticky="e", padx=60)

# Position all the objects that will go inside the input controls frame
xAreaLabel2.grid(row=1, column=0, sticky="e")
xAreaInput2.grid(row=1, column=1, pady=3, sticky="ew")
xAreaUnitSelect2.grid(row=1, column=2, pady=3, sticky="w")
lengthLabel2.grid(row=2, column=0, sticky="e")
lengthInput2.grid(row=2, column=1, pady=3, sticky="ew")
lengthUnitSelect2.grid(row=2, column=2, pady=3, sticky="w")
bendsLabel2.grid(row=3, column=0, sticky="e")
bendsSelect2.grid(row=3, column=1, pady=3, sticky="ew")
foldsLabel2.grid(row=4, column=0, sticky="e")
foldsSelect2.grid(row=4, column=1, pady=3, sticky="ew")

# Run the GUI
mainWindow.mainloop()
