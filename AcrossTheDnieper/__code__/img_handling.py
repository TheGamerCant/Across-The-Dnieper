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
    provincesBmpDirectory = os.path.join(current_directory, "map", "provinces.bmp")

    provincesImage = Image.open(provincesBmpDirectory)
    image_array = np.array(provincesImage)
    provincesImage.close()
    height, width, channels = image_array.shape

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
                    
                format_string = 'HBBBH'
                hex_bytes = bytes.fromhex(hexToFind)
                record = (j, hex_bytes[0], hex_bytes[1], hex_bytes[2], provincesArrayHexID[hexPos][1])
                packed_data = struct.pack(format_string, *record)
                file.write(packed_data)
                
    os.chdir(current_directory) 

def return_binary_array(column):
    format_string = 'HBBBH'
    format_string_size = struct.calcsize(format_string)
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