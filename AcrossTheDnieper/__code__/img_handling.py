import os
from func import rgbToHex
try:
	import numpy as np
	has_numpy = True
except ImportError:
	has_numpy = False
try:
	from PIL import Image
	has_pil = True
except ImportError:
	has_pil = False
	
def binarySearchHexArray(array, target):
    left, right = 0, len(array) - 1

    while left <= right:
        mid = (left + right) // 2
        if array[mid][0] == target:
            return mid
        elif array[mid][0] < target:
            left = mid + 1
        else:
            right = mid - 1

    return mid
	
def save_prov_csv_file(provincesArray):
    provincesArrayHexID = []
    for prov in provincesArray:
         provincesArrayHexID.append([prov.hexadecimal, prov.ID])
		
    provincesArrayHexID.sort(key=lambda x: x[0])	
    current_directory = os.getcwd()
    provincesBmpDirectory = os.path.join(current_directory, "map", "provinces.bmp")

    provincesImage = Image.open(provincesBmpDirectory)
    image_array = np.array(provincesImage)
    provincesImage.close()
    height, width, channels = image_array.shape

    provinces_directory = os.path.join(current_directory, "__code__", "map", "provinces")
    os.chdir(provinces_directory) 
    hexPos=0
    for i in range(0,height):
        filename = f'pr__{i}.csv'
        with open(filename, 'w', encoding='utf-8') as file:
            for j in range(0,width):
                red,green,blue = image_array[i][j]
                hexToFind = rgbToHex(red, green, blue)
                if provincesArrayHexID[hexPos][0] ==  hexToFind:
                    print(str(j)+";"+hexToFind+";"+str(provincesArrayHexID[hexPos][1]),file=file)
                else:
                    hexPos = binarySearchHexArray(provincesArrayHexID, hexToFind)
                    print(str(j)+";"+hexToFind+";"+str(provincesArrayHexID[hexPos][1]),file=file)
                
    os.chdir(current_directory) 