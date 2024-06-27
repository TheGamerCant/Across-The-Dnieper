from func import returnStringBetweenBrackets
from func import removeStringBetweenBrackets
from func import removeAllTextBetweenBracketsAndReturnAsArray
from func import rgbToHex
import re
import os

class buildingClass:
    def __init__(self, name, provincial, show_on_map,max_level):
        self.name = str(name)
        self.provincial = bool(provincial)
        self.show_on_map = int(show_on_map)
        self.max_level = int(max_level)

class terrainClass:
    def __init__(self, name, naval, hexadecimal):
        self.name = str(name)
        self.naval = bool(naval)
        self.hexadecimal = str(hexadecimal)

class provinceClass:
    def __init__(self, ID, hexadecimal, type, coastal, terrain, continent, stateID, victoryPoints, strategicRegion, names, buildings, coordinates):
        self.ID = int(ID)
        self.hexadecimal = str(hexadecimal)
        self.type = str(type)
        self.coastal = str(coastal)
        self.terrain = str(terrain)
        self.continent = int(continent)
        self.stateID = int(stateID)
        self.victoryPoints = int(victoryPoints)
        self.strategicRegion = int(strategicRegion)
        self.names = names if isinstance(names, list) else [names]
        self.buildings = buildings if isinstance(buildings, list) else [buildings]
        self.coordinates = coordinates if isinstance(coordinates, list) else [coordinates]

class stateClass:
    def __init__(self, ID, population, category, owner, provinces, names, buildings, resources, dateInfo, cores, claims, stateFlags, impassable, variables):
        self.ID = int(ID)
        self.population = int(population)
        self.category = str(category)
        self.owner = str(owner)
        self.provinces = provinces if isinstance(provinces, list) else [provinces]
        self.names = names if isinstance(names, list) else [names]
        self.buildings = buildings if isinstance(buildings, list) else [buildings]
        self.resources = resources if isinstance(resources, list) else [resources]
        self.dateInfo = dateInfo if isinstance(dateInfo, list) else [dateInfo]
        self.cores = cores if isinstance(cores, list) else [cores]
        self.claims = claims if isinstance(claims, list) else [claims]
        self.stateFlags = stateFlags if isinstance(stateFlags, list) else [stateFlags]
        self.impassable = bool(impassable)
        self.variables = variables if isinstance(variables, list) else [variables]

class strategicRegionClass:
    def __init__(self, ID, name, provinces):
        self.ID = int(ID)
        self.name = str(name)
        self.provinces = provinces if isinstance(provinces, list) else [provinces]

def load_buildings():
    buildingsArray=[]

    current_directory = os.getcwd()
    base_directory = os.path.dirname(current_directory)
    buildings_folder_path = os.path.join(base_directory, "common", "buildings")
    
    os.chdir(buildings_folder_path) 
    try:
        for file in os.listdir(): 
            if file.endswith(".txt"): 
                file_path = f"{buildings_folder_path}\{file}"
        
                with open(file_path, 'r', errors='ignore') as f: 
                    buildingsString = ''
                    for line in f:
                        findHash = line.find('#')
                        if findHash!=-1:
                            line = line[:findHash]
                        buildingsString+=line

                    buildingsString = re.sub(r'\t', ' ', buildingsString)
                    buildingsString = re.sub(r'\n', '', buildingsString)
                    buildingsString = re.sub(r'\s+', ' ', buildingsString).strip()

                    buildingsString = returnStringBetweenBrackets(buildingsString, "buildings")

                    findBuilding = re.search(r'(\w+)\s*=\s*\{', buildingsString)
                    while findBuilding:
                        name = str(findBuilding.group(1))
                        currentBuildingInfo = returnStringBetweenBrackets(buildingsString,name)

                        provincial_match = re.search(r'provincial\s*=\s*yes', currentBuildingInfo)
                        if provincial_match:
                            provincial = True
                        else:
                            provincial = False

                        showOnMap_match = re.search(r'show_on_map\s*=\s*(\d+)', currentBuildingInfo)
                        if showOnMap_match:
                            showOnMap = int(showOnMap_match.group(1))
                        else:
                            showOnMap = 0

                        maxLevel_match = re.search(r'max_level\s*=\s*(\d+)', currentBuildingInfo)
                        if maxLevel_match:
                            maxLevel = int(maxLevel_match.group(1))
                        else:
                            maxLevel = 1

                        buildingsArray.append(buildingClass(name,provincial,showOnMap,maxLevel))
                        buildingsString = removeStringBetweenBrackets(buildingsString, name)
                        findBuilding = re.search(r'(\w+)\s*=\s*\{', buildingsString)


    except:
        buildingsArray.append(buildingClass('infrastructure',False,0,5))
        buildingsArray.append(buildingClass('arms_factory',False,6,20))
        buildingsArray.append(buildingClass('industrial_complex',False,6,20))
        buildingsArray.append(buildingClass('air_base',False,1,10))
        buildingsArray.append(buildingClass('supply_node',True,1,1))
        buildingsArray.append(buildingClass('rail_way',True,1,1))
        buildingsArray.append(buildingClass('naval_base',True,1,10))
        buildingsArray.append(buildingClass('bunker',True,1,10))
        buildingsArray.append(buildingClass('dockyard',False,1,20))
        buildingsArray.append(buildingClass('anti_air_building',False,3,5))
        buildingsArray.append(buildingClass('synthetic_refinery',False,1,3))
        buildingsArray.append(buildingClass('fuel_silo',False,1,3))
        buildingsArray.append(buildingClass('radar_station',False,1,6))
        buildingsArray.append(buildingClass('rocket_site',False,1,5))
        buildingsArray.append(buildingClass('nuclear_reactor',False,1,1))

    os.chdir(base_directory) 
    return buildingsArray


def load_terrain():
    terrainArray=[]

    current_directory = os.getcwd()
    terrain_folder_path = os.path.join(current_directory, "common", "terrain")
    
    os.chdir(terrain_folder_path) 
    try:
        for file in os.listdir(): 
            if file.endswith(".txt"): 
                file_path = f"{terrain_folder_path}\{file}"
        
                with open(file_path, 'r', errors='ignore') as f: 
                    terrainString = ''
                    for line in f:
                        findHash = line.find('#')
                        if findHash!=-1:
                            line = line[:findHash]
                        terrainString+=line

                    terrainString = re.sub(r'\t', ' ', terrainString)
                    terrainString = re.sub(r'\n', '', terrainString)
                    terrainString = re.sub(r'\s+', ' ', terrainString).strip()

                    terrainString = returnStringBetweenBrackets(terrainString, "categories")

                    findTerrain = re.search(r'(\w+)\s*=\s*\{', terrainString)
                    while findTerrain:
                        name = str(findTerrain.group(1))
                        currentTerrainInfo = returnStringBetweenBrackets(terrainString,name)

                        naval_match = re.search(r'naval_terrain\s*=\s*yes', currentTerrainInfo)
                        if naval_match:
                            naval = True
                        else:
                            naval = False

                        hexadecimal_match = re.search(r'color\s*=\s*\{\s*(\d+)\s*(\d+)\s*(\d+)\s*\}', currentTerrainInfo)
                        if hexadecimal_match:
                            red = hexadecimal_match.group(1)
                            green = hexadecimal_match.group(2)
                            blue = hexadecimal_match.group(3)

                            hexadecimal = rgbToHex(red,green,blue)
                        else:
                            hexadecimal = 0


                        terrainArray.append(terrainClass(name,naval, hexadecimal))
                        terrainString = removeStringBetweenBrackets(terrainString, name)
                        findTerrain = re.search(r'(\w+)\s*=\s*\{', terrainString)

    except:
        terrainArray.append(terrainClass('unknown',False,'ff0000'))
        terrainArray.append(terrainClass('ocean',True,'2853b0'))
        terrainArray.append(terrainClass('lakes',False,'3a5bff'))
        terrainArray.append(terrainClass('forest',False,'59c755'))
        terrainArray.append(terrainClass('hills',False,'f8ff99'))
        terrainArray.append(terrainClass('mountain',False,'9dc0d0'))
        terrainArray.append(terrainClass('plains',False,'ff8142'))
        terrainArray.append(terrainClass('urban',False,'787878'))
        terrainArray.append(terrainClass('jungle',False,'7fbf00'))
        terrainArray.append(terrainClass('marsh',False,'4c6023'))
        terrainArray.append(terrainClass('desert',False,'ff7f00'))
        terrainArray.append(terrainClass('water_fjords',True,'4ba2c6'))
        terrainArray.append(terrainClass('water_shallow_sea',True,'3876d9'))
        terrainArray.append(terrainClass('water_deep_ocean',True,'022696'))


    os.chdir(current_directory) 
    return terrainArray

def load_provinces():
    current_directory = os.getcwd()
    definitions_csv_file_path = os.path.join(current_directory, "map", "definition.csv")
    provincesArray = []
    with open(definitions_csv_file_path, 'r') as file:
        for line in file:
            if line[0]!= '#':
                parts = line.strip().split(';')
                ID, red, green, blue, type, coastal, terrain, continent = parts[0:8]
                hexadecimal = rgbToHex(red,green,blue)
                province = provinceClass(ID, hexadecimal, type, coastal, terrain, continent, 0, 0, 0, None, None, None)
                provincesArray.append(province)

    provincesArray.sort(key=lambda x: x.ID)
    return provincesArray

def load_states(provincesArray,buildingsArray): 
    statesArray = []
    statesArray.append(stateClass(0,0,"","",0,0,0,0,0,0,0,0,False,0))
    current_directory = os.getcwd()
    history_states_folder_path = os.path.join(current_directory, "history", "states")

    os.chdir(history_states_folder_path) 
    for file in os.listdir(): 
        if file.endswith(".txt"): 
            file_path = f"{history_states_folder_path}\{file}"
    
            with open(file_path, 'r', errors='ignore') as f: 
                stateData = ''
                for line in f:
                    findHash = line.find('#')
                    if findHash!=-1:
                        line = line[:findHash]
                    stateData+=line

                stateData = re.sub(r'\t', ' ', stateData)
                stateData = re.sub(r'\n', '', stateData)
                stateData = re.sub(r'\s+', ' ', stateData).strip()

                historyData = returnStringBetweenBrackets(stateData, "history")
                stateData = removeStringBetweenBrackets(stateData, "history")

                buildingData = returnStringBetweenBrackets(historyData, "buildings")
                historyData = removeStringBetweenBrackets(historyData, "buildings")


                id_match = re.search(r'id\s*=\s*(\d+)', stateData)
                if id_match:
                    ID = id_match.group(1)
                    stateData = re.sub(r'id\s*=\s*(\d+)', '', stateData).strip()
                else:
                    ID = None

                try:
                    stateData = re.sub(r'name\s*=\s*\"(\w+)\"', '', stateData).strip()
                except:
                    pass

                population_match = re.search(r'manpower\s*=\s*(\d+)', stateData)
                if population_match:
                    population = population_match.group(1)
                    stateData = re.sub(r'manpower\s*=\s*(\d+)', '', stateData).strip()
                else:
                    population = None

                category_match = re.search(r'state_category\s*=\s*(\w+)', stateData)
                if category_match:
                    category = category_match.group(1)
                    stateData = re.sub(r'state_category\s*=\s*(\w+)', '', stateData).strip()
                else:
                    category = None

                impassable_match = re.search(r'impassable\s*=\s*yes', stateData)
                if impassable_match:
                    impassable = True
                    stateData = re.sub(r'impassable\s*=\s*(\w+)', '', stateData).strip()
                else:
                    impassable = False

                provinces_match = re.search(r'provinces\s*=\s*\{(.*?)\}', stateData, re.DOTALL)
                if provinces_match:
                    provinces = re.findall(r'(\d+)', provinces_match.group(1))
                    stateData = re.sub(r'provinces\s*=\s*\{(.*?)\}', '', stateData).strip()
                    for prov in provinces:
                        provincesArray[int(prov)].stateID = ID
                else:
                    provinces = []

                resources_match = re.search(r'resources\s*=\s*\{(.*?)\}', stateData, re.DOTALL)
                if resources_match:
                    resources = re.findall(r'(\w+)\s*=\s*(\d+)', resources_match.group(1))
                    resources = [list(item) for item in resources]
                    stateData = re.sub(r'resources\s*=\s*\{(.*?)\}', '', stateData).strip()
                else:
                    resources = None

                owner_match = re.search(r'owner\s*=\s*(\w{3})', historyData)
                if owner_match:
                    owner = owner_match.group(1)
                    historyData = re.sub(r'owner\s*=\s*(\w{3})', '', historyData).strip()
                else:
                    owner = None

                victoryPoints_match = re.findall(r'victory_points\s*=\s*\{\s*(\d+)\s*(\d+)\s*\}', historyData)
                if victoryPoints_match:
                    VPs = [list(item) for item in victoryPoints_match]
                    for i in range(0,len(VPs)):
                        provincesArray[int(VPs[i][0])].victoryPoints = int(VPs[i][1])
                    historyData = re.sub(r'victory_points\s*=\s*\{\s*(\d+)\s*(\d+)\s*\}', '', historyData).strip()

                dateInfo_match = re.findall(r'(\d+)\.(\d+)\.(\d+)\s*=\s*\{(.*?)\}', historyData)
                if dateInfo_match:
                    dateInfo = [list(item) for item in dateInfo_match]
                    historyData = re.sub(r'(\d+)\.(\d+)\.(\d+)\s*=\s*\{(.*?)\}', '', historyData).strip()
                else:
                    dateInfo = None

                cores_match = re.findall(r'add_core_of\s*=\s*(\w{3})', historyData)
                if cores_match:
                    cores = cores_match
                    historyData = re.sub(r'add_core_of\s*=\s*(\w{3})', '', historyData).strip()
                else:
                    cores = None

                claims_match = re.findall(r'add_claim_by\s*=\s*(\w{3})', historyData)
                if claims_match:
                    claims = claims_match
                    historyData = re.sub(r'add_claim_by\s*=\s*(\w{3})', '', historyData).strip()
                else:
                    claims = None

                flags_match = re.findall(r'set_state_flag\s*=\s*(\w+)', historyData)
                if flags_match:
                    stateFlags = flags_match
                    historyData = re.sub(r'set_state_flag\s*=\s*(\w+)', '', historyData).strip()
                else:
                    stateFlags = None


                variables = []
                find_variables = historyData.find("set_variable")
                while find_variables !=-1:
                    currentVar = returnStringBetweenBrackets(historyData, "set_variable")
                    var_match = re.search(r'(.+)\s*=\s*(.+)', currentVar)
                    variables.append([var_match.group(1),var_match.group(2)])
                    historyData= removeStringBetweenBrackets(historyData, "set_variable")
                    find_variables = historyData.find("set_variable")

                provBuildings_match = re.findall(r'(\d+)\s*=\s*\{\s*(.*?)\s*\}', buildingData)
                if provBuildings_match:
                    provBuildings = [list(item) for item in provBuildings_match]
                    for i in range(0,len(provBuildings)):
                        provID = int(provBuildings[i][0])
                        provBuildings_match2 = re.findall(r'(\w+)\s*=\s*(\d+)', provBuildings[i][1])
                        provBuildings_match2 = [list(item) for item in provBuildings_match2]

                        for i in range (0,len(provBuildings_match2)):
                            for validBuilding in buildingsArray:
                                if provBuildings_match2[i][0] == validBuilding.name and validBuilding.provincial == True:
                                    if provincesArray[provID].buildings == None:
                                        provincesArray[provID].buildings = []

                                    provincesArray[provID].buildings.append(provBuildings_match2[i])

                    
                    buildingData = re.sub(r'(\d+)\s*=\s*\{\s*(.*?)\s*\}', '', buildingData).strip()
                    
                
                buildings_match = re.findall(r'(\w+)\s*=\s*(\d+)', buildingData)
                if buildings_match:
                    buildings = []
                    buildings_temp = [list(item) for item in buildings_match]
                    for i in range (0,len(buildings_temp)):
                        for validBuilding in buildingsArray:
                            if buildings_temp[i][0] == validBuilding.name and validBuilding.provincial == False:
                                buildings.append(buildings_temp[i])


                    buildingData = re.sub(r'(\w+)\s*=\s*(\d+)', '', buildingData).strip()
                else:
                    buildings = None


                statesArray.append(stateClass(ID, population, category, owner, provinces, 0, buildings, resources, dateInfo, cores, claims, stateFlags, impassable, variables))

    
    statesArray.sort(key=lambda x: x.ID)
    os.chdir(current_directory)
    return statesArray

def load_strategic_regions(provincesArray):
    strategicRegionsArray = []
    
    current_directory = os.getcwd()
    strategic_regions_folder_path = os.path.join(current_directory, "map", "strategicregions")

    os.chdir(strategic_regions_folder_path) 
    for file in os.listdir(): 
        if file.endswith(".txt"): 
            file_path = f"{strategic_regions_folder_path}\{file}"
    
            with open(file_path, 'r', errors='ignore') as f: 
                fileData = ''
                for line in f:
                    findHash = line.find('#')
                    if findHash!=-1:
                        line = line[:findHash]
                    fileData+=line

                fileData = re.sub(r'\t', ' ', fileData)
                fileData = re.sub(r'\n', '', fileData)
                fileData = re.sub(r'\s+', ' ', fileData).strip()

                id_match = re.search(r'id\s*=\s*(\d+)', fileData)
                if id_match:
                    ID = id_match.group(1)
                    fileData = re.sub(r'id\s*=\s*(\d+)', '', fileData).strip()
                else:
                    ID = None

                name_match = re.search(r'name\s*=\s*\"(\w+)\"', fileData)
                if name_match:
                    name = name_match.group(1)
                    fileData = re.sub(r'name\s*=\s*\"(\w+)\"', '', fileData).strip()
                else:
                    name = None

                provinces_match = re.search(r'provinces\s*=\s*\{(.*?)\}', fileData, re.DOTALL)
                if provinces_match:
                    provinces = re.findall(r'(\d+)', provinces_match.group(1))
                    fileData = re.sub(r'provinces\s*=\s*\{(.*?)\}', '', fileData).strip()
                else:
                    provinces = []

                strategicRegionsArray.append(strategicRegionClass(ID, name, provinces))

    strategicRegionsArray.sort(key=lambda x: x.ID)
    return strategicRegionsArray