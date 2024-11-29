import os

datasetLabels = "datasets/HAR/train/labels"
datasetImages = "datasets/HAR/train/images"


desiredLabels = [0, 5, 11, 12, 13, 14]

# Iterate over every txt file with labels
for filename in os.scandir(datasetLabels):
    # If the file exists
    if filename.is_file():
        print(filename.path)

        # False = The file doesn't have desired labels, True = the file has desired labels
        auxLabels = False

        # Open file
        file = open(filename.path)
        # For every line (label) in the file
        for line in file:
            
            splitLine = line.split(" ")
            # Print the label's index 
            print(splitLine[0])
            # If the label is one of the desired labels
            if int(splitLine[0]) in desiredLabels:
                # Mark the file as desired
                auxLabels = True
                print("*******", splitLine[0], "********")
        file.close()
        # If the file is not desired
        if not auxLabels:
            # File name for matching image
            imgFile = filename.name[:len(filename.name)-4] + ".jpg"
            print(imgFile)
            # File path for matching image
            delImages = datasetImages + "/" + imgFile


            print(filename.name, " DELETED")
            os.remove(filename.path)
            print(imgFile, " DELETED")
            os.remove(delImages)
