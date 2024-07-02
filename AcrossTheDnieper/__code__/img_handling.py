import struct
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
	
def save_prov_bin_file(provincesArray):
    provincesArrayHexID = []
    for prov in provincesArray:
         provincesArrayHexID.append([prov.hexadecimal, prov.ID])
		
    provincesArrayHexID.sort(key=lambda x: x[0])	
    current_directory = os.getcwd()

    provincesImage = Image.open(current_directory+"\\map\\provinces.bmp")
    image_array = np.array(provincesImage)
    provincesImage.close()
    height, width, channels = image_array.shape
    heightmapImage = Image.open(current_directory+"\\map\\heightmap.bmp")
    heightmap_array = np.array(heightmapImage)
    heightmapImage.close()

    provinces_directory = os.path.join(current_directory, "__code__", "map", "provinces")
    os.chdir(provinces_directory) 
    hexPos=0
    for i in range(0,height):
        filename = f'pr__{i}.bin'
        with open(filename, 'wb') as file:
            for j in range(0,width):
                red,green,blue = image_array[i][j]
                hexToFind = rgbToHex(red, green, blue)
                
                if provincesArrayHexID[hexPos][0] !=  hexToFind:
                    hexPos = binarySearchHexArray(provincesArrayHexID, hexToFind)
                    
                format_string = 'BBBHB'
                hex_bytes = bytes.fromhex(hexToFind)
                record = (hex_bytes[0], hex_bytes[1], hex_bytes[2], provincesArrayHexID[hexPos][1], heightmap_array[i][j])
                packed_data = struct.pack(format_string, *record)
                file.write(packed_data)
                
    os.chdir(current_directory) 

def return_binary_array(column):
    format_string = 'BBBHB'
    current_directory = os.getcwd()
    bin_directory = os.path.join(current_directory, "__code__", "map", "provinces", f"pr__{column}.bin")
    array=[]
    with open(bin_directory, 'rb') as binary_file:
        while True:
            chunk = binary_file.read(struct.calcsize(format_string))
            if not chunk:
                break
            unpacked_data = struct.unpack(format_string, chunk)
            array.append(unpacked_data)

    
    return array

def form_border(prov1, prov2, provincesArray):
    prov1 = int(prov1)
    prov2 = int(prov2)
    if prov1 in provincesArray[prov2].borders:
        pass
    else:
        provincesArray[prov2].borders.append(prov1)
        provincesArray[prov1].borders.append(prov2)


def form_border_coords(prov1, prov2, x, y, direction, provincesArray):
    prov1 = int(prov1)
    prov2 = int(prov2)
    x = int(x)
    y = int(y)
    direction = str(direction)
    if direction == "east":
        provincesArray[prov2].border_coords.append([x+1,y,prov1,"west"])
        provincesArray[prov1].border_coords.append([x,y,prov2,"east"])
    elif direction == "south":
        provincesArray[prov2].border_coords.append([x,y+1,prov1,"north"])
        provincesArray[prov1].border_coords.append([x,y,prov2,"south"])

def load_borders(provincesArray):
    current_directory = os.getcwd()
    provincesImage = Image.open(current_directory+"\\map\\provinces.bmp")
    width, height = provincesImage.size
    provincesImage.close()

    for prov in provincesArray:
        if prov.borders[0] == None:
            prov.borders = []
        if prov.border_coords[0] == None:
            prov.border_coords = []


    for h in range(0,height-1):
        array1 = return_binary_array(h)
        array2 = return_binary_array(h+1)
        for w in range(0,width-1):
            if array1[w][0] != array1[w+1][0] and array1[w][1] != array1[w+1][1] and array1[w][2] != array1[w+1][2]:
                form_border(array1[w][3], array1[w+1][3], provincesArray)
                form_border_coords(array1[w][3], array1[w+1][3], w, h, "east", provincesArray)

            if array1[w][0] != array2[w][0] and array1[w][1] != array2[w][1] and array1[w][2] != array2[w][2]:
                form_border(array1[w][3], array2[w][3], provincesArray)
                form_border_coords(array1[w][3], array2[w][3], w, h, "south", provincesArray)
                 
    array1 = return_binary_array(height-1)
    if array1[width-2][0] != array1[width-1][0] and array1[width-2][1] != array1[width-1][1] and array1[width-2][2] != array1[width-1][2]:
        form_border(array1[width-2][3], array2[width-1][3], provincesArray)
        form_border_coords(array1[width-2][3], array2[width-1][3], width-2, height-1, "east", provincesArray)

def load_coordinates(provincesArray):
    current_directory = os.getcwd()
    provincesImage = Image.open(current_directory+"\\map\\provinces.bmp")
    width, height = provincesImage.size
    provincesImage.close()

    for prov in provincesArray:
        if prov.coordinates[0] == None:
            prov.coordinates = []
    
    for h in range(0, height):
        array1 = return_binary_array(h)
        for w in range(0,width):
            provID = int(array1[w][3])
            provincesArray[provID].coordinates.append([w,h])
