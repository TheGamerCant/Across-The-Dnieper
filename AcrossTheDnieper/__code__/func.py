import re

def returnStringBetweenBrackets(fullStr, str):
    startBracketPos = fullStr.find(str)
    fullStr = fullStr[startBracketPos:]

    startBracketPos = fullStr.find("{")
    fullStr = fullStr[startBracketPos + 1:]

    i = 0
    bracketBalance = 1
    while bracketBalance != 0:
        if fullStr[i] == '{':
            bracketBalance += 1
        elif fullStr[i] == '}':
            bracketBalance -= 1
        i += 1

    return fullStr[:i - 1]

def removeStringBetweenBrackets(fullStr, str):
    startBracketPos = fullStr.find(str)
    fullStrOriginal = fullStr[:startBracketPos]
    fullStr = fullStr[startBracketPos:]

    startBracketPos = fullStr.find("{")
    fullStr = fullStr[startBracketPos + 1:]

    i = 0
    bracketBalance = 1
    while bracketBalance != 0:
        if fullStr[i] == '{':
            bracketBalance += 1
        elif fullStr[i] == '}':
            bracketBalance -= 1
        i += 1

    stringToReturn = fullStrOriginal + fullStr[i:]

    return stringToReturn

def removeAllTextBetweenBracketsAndReturnAsArray(str):
    array=[]
    bracketMatch = re.search(r'(\w+)\s*=\s*{', str)
    if bracketMatch:
        array.append(str(bracketMatch.group(1)))
        str = removeStringBetweenBrackets(str,str(bracketMatch.group(1)))

        print ("")

    return array

def rgbToHex(red,green,blue):
    red = int(red)
    green = int(green)
    blue = int(blue)

    hex_r = f"{red:02x}"
    hex_g = f"{green:02x}"
    hex_b = f"{blue:02x}"

    return hex_r + hex_g + hex_b