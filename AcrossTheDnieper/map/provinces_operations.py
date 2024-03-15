#Before using, make a blank "definition_new.txt" file and a "provs_to_make_mountains.txt" with the provinces you want to become mountains in the same directory
#Use this when you want to change all the provinces in states (provided they fulfill your conditions), otherwise it's best to directly edit definitions.csv or use the nudge tool

terrainOld = open("definition.csv","r")
terrainNew = open("provs_to_make_mountains.txt","r")
terrainMerge = open("definition_new.txt","w")

terrainNewLines = terrainNew.readlines()
terrainOldLines = terrainOld.readlines()

provincesInStatesArray=[]

for i in terrainNewLines:
    line_numbers = i.split()
    provincesInStatesArray.extend([int(num) for num in line_numbers])

provincesInStatesArray.sort()

currentLineCount = 0
for i in terrainOldLines:
    parts = i.split(';')
    provinceID = int(parts[0])

    
    if provinceID in provincesInStatesArray and parts[-2] == "forest":
        parts[-2] = "mountain"

    print("{};{};{};{};{};{};{};{}".format((parts[0]),(parts[1]),(parts[2]),(parts[3]),(parts[4]),(parts[5]),(parts[6]),(parts[7])), file=terrainMerge, end="")
    currentLineCount+=1

parts
terrainOld.close()
terrainNew.close()
terrainMerge.close()
