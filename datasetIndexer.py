import os

datasetLabels = "datasets/HAR/train/labels"
datasetImages = "datasets/HAR/train/images"


desiredLabels = [0, 5, 11, 12, 13, 14]



testString = "14 0.5046875 0.51484375 0.990625 0.9703125"

aux = testString.split(" ")

aux[0] = str(desiredLabels.index(int(aux[0])))

testString = " ".join(aux)

print(testString)

# Iterate over every txt file with labels
for filename in os.scandir(datasetLabels):
    with open(filename.path, 'r') as file:
        print(filename.name)
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].split(" ")
            data[i][0] = data[i][0].replace('0', '0')
            data[i][0] = data[i][0].replace('5', '1')
            data[i][0] = data[i][0].replace('11', '2')
            data[i][0] = data[i][0].replace('12', '3')
            data[i][0] = data[i][0].replace('13', '4')
            data[i][0] = data[i][0].replace('14', '5')
        
            data[i] = " ".join(data[i])
        data = "".join(data)

        print(data)
        print("*****************")
    with open(filename.path, 'w') as file:
        file.write(data)

print("Text Replaced")
        
        

    # CODE FOR DELETING UNUSED LABELS 

    # try:
        # Open file in read mode 
    #     with open(filename.path, 'r') as fr:
    #         lines = fr.readlines()
            # Open file in write mode
    #         with open(filename.path, 'w') as fw:
    #             for line in lines:
                
    #                 # strip() is used to remove '\n'
    #                 # present at the end of each line
    #                 # If the label is desired
    #                 if int(line.split(" ")[0]) in desiredLabels:
    #                     # Write the line 
    #                     fw.write(line)
    #     # Else delete the line
    #     print("Deleted")
    # except:
    #     print("Oops! something error")
    # 

