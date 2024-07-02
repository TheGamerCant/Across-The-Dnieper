import os
import random
import PIL
from PIL import Image
from img_handling import return_binary_array

def write_history_files(provincesArray, statesArray):
    current_directory = os.getcwd()
    history_states_folder_directory = os.path.join(current_directory, "__code__", "history", "states")
    os.chdir(history_states_folder_directory) 
    for state in statesArray:
        if state.ID !=0:
            filename = f'{state.ID}-State_{state.ID}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                print(\
                    "state={\n\tid="\
                    +str(state.ID) + "\n\tname=\"STATE_"\
                    +str(state.ID)+"\"", file=f)
                if state.resources[0] != None:
                    print ("\tresources={", file=f )
                    for i in range (0,len(state.resources)):
                        print ("\t\t" + str(state.resources[i][0]) + " = " + str(state.resources[i][1]),file=f)
                    print ("\t}", file=f )

                print("\thistory={\n\t\towner = " + str(state.owner), file=f)
                if state.cores[0] != None:
                    for i in range (0,len(state.cores)):
                        print("\t\tadd_core_of = " + str(state.cores[i]), file=f)
                if state.claims[0] != None:
                    for i in range (0,len(state.claims)):
                        print("\t\tadd_claim_by = " + str(state.claims[i]), file=f)
                if state.stateFlags[0] != None:
                    for i in range (0,len(state.stateFlags)):
                        print("\t\tset_state_flag = " + str(state.stateFlags[i]), file=f)
                if state.variables[0] != None:
                    for i in range (0,len(state.variables)):
                        print("\t\tset_variable = { " + str(state.variables[i][0]) + " = " + str(state.variables[i][1]) +"}", file=f)
                for prov in state.provinces:
                    if provincesArray[int(prov)].victoryPoints != 0:
                        try:
                            print ("\t\tvictory_points={ " + str(provincesArray[int(prov)].ID) + " "\
                                + str(provincesArray[int(prov)].victoryPoints) + " }" + "\t\t#" + str(provincesArray[int(prov)].names[0][1]), file=f )
                        except:
                            print ("\t\tvictory_points={ " + str(provincesArray[int(prov)].ID) + " "\
                                + str(provincesArray[int(prov)].victoryPoints) + " }", file=f )
                print ("\t\tbuildings={", file=f)
                for prov in state.provinces:
                    if provincesArray[int(prov)].buildings[0] != None:
                        print ("\t\t\t" + str(provincesArray[int(prov)].ID) + " = { ", end="", file=f)
                        for i in range(0,len(provincesArray[int(prov)].buildings)):
                            print (str(provincesArray[int(prov)].buildings[i][0]) + " = " +  str(provincesArray[int(prov)].buildings[i][1]), end=" ", file=f)
                        print ("}", file=f)
                if state.buildings:
                    if state.buildings[0] != None:
                        for i in range(0,len(state.buildings)):
                            print("\t\t\t" + str(state.buildings[i][0])+ " = " + str(state.buildings[i][1]), file=f)
                print ("\t\t}", file=f)
                if state.dateInfo[0] != None:
                    for i in range(0,len(state.dateInfo)):
                        print ("\t\t" + str(state.dateInfo[i][0])+"={ "+str(state.dateInfo[i][1])+" }", file=f)
                print ("\t}\n\tprovinces={\n\t\t",end='', file=f)
                for prov in state.provinces:
                    print (prov+ " ",end='', file=f)
                print ("\n\t}\n\tmanpower=" + str(state.population)+"\n\tbuildings_max_level_factor=1.000\n\tlocal_supplies = 0.5\
                       \t\t\t#One unit of local_supplies is equal to 0.2 units of supply. If undefined, assumed to be 0.\n\tstate_category="\
                       + state.category, file=f)
                if state.impassable == True:
                    print("\timpassable=yes",file=f)
                print("}", file=f)

    os.chdir(current_directory)

def write_strategic_region_files(strategicRegionsArray):
    current_directory = os.getcwd()
    strategic_regions_folder_directory = os.path.join(current_directory, "__code__", "map", "strategicregions")
    os.chdir(strategic_regions_folder_directory) 
    for strategic_region in strategicRegionsArray:
        if strategic_region.ID !=0:
            filename = f'{strategic_region.ID}-{strategic_region.name}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                print("strategic_region={\n\tid=" + str(strategic_region.ID)\
                + "\n\tname = \"" + str(strategic_region.name) + "\"\n\tprovinces={\n\t\t", end="", file=f)
                for prov in strategic_region.provinces:
                    print (str(prov), end=" ", file=f)
                print("\n\t}\n\tweather={\n\t}\n}", file=f)

    os.chdir(current_directory)

def write_loc_files(provincesArray,statesArray,strategicRegionsArray):
    current_directory = os.getcwd()
    victory_points_loc_directory = os.path.join(current_directory, "__code__", "localisation", "english", "victory_points_l_english.yml")
    state_names_loc_directory = os.path.join(current_directory, "__code__", "localisation", "english", "state_names_l_english.yml")
    strategic_regions_loc_directory = os.path.join(current_directory, "__code__", "localisation", "english", "strategic_region_names_l_english.yml")

    with open(victory_points_loc_directory, 'w', encoding='utf-8-sig') as f:
        print("l_english: ", file=f)
        for i in provincesArray:
            if i.names[0]!=None:
                for j in range (0,len(i.names)):
                    if str(i.names[j][0]) == "DEFAULT":
                        print(" VICTORY_POINTS_" + str(i.ID) + ":0 \"" + str(i.names[j][1] + "\""), file=f)
                    else:
                        print(" VICTORY_POINTS_" + str(i.ID) + "_" + str(i.names[j][0]) + ":0 \"" + str(i.names[j][1] + "\""), file=f)

    with open(state_names_loc_directory, 'w', encoding='utf-8-sig') as f:
        print("l_english: ", file=f)
        for i in statesArray:
            if i.names[0]!=None:
                for j in range (0,len(i.names)):
                    if str(i.names[j][0]) == "DEFAULT":
                        print(" STATE_" + str(i.ID) + ":0 \"" + str(i.names[j][1] + "\""), file=f)
                    else:
                        print(" STATE_" + str(i.ID) + "_" + str(i.names[j][0]) + ":0 \"" + str(i.names[j][1] + "\""), file=f)

    with open(strategic_regions_loc_directory, 'w', encoding='utf-8-sig') as f:
        print("l_english: ", file=f)
        for i in strategicRegionsArray:
            print(" STRATEGICREGION_" + str(i.ID) + ":0 \"" + str(i.name + "\""), file=f)

def write_state_names_scripted_effects_files(provincesArray,statesArray):
    current_directory = os.getcwd()
    scripted_effects_directory = os.path.join(current_directory, "__code__", "common", "scripted_effects", "state_and_province_names_scripted_effects.txt")
    with open(scripted_effects_directory, 'w', encoding='utf-8') as f:
        for state in statesArray:
            if state.ID !=0:
                print ("update_state_" + str(state.ID) + "_names={\t\t#" + str(state.names[0][1]), file=f)
                if len(state.names) != 1:
                    print ("\t" + str(state.ID) + "={", file=f)
                    print ("\t\tif={\n\t\t\tlimit = { CONTROLLER = { " + str(state.names[1][0]) + " = yes } }"\
                        "\n\t\t\tset_state_name = STATE_" + str(state.ID) + "_" + str(state.names[1][0]), "\n\t\t}", file=f)
                    if len(state.names) > 2:
                        for i in range(2,len(state.names)):
                            print ("\t\telse_if={\n\t\t\tlimit = { CONTROLLER = { " + str(state.names[i][0]) + " = yes } }"\
                                "\n\t\t\tset_state_name = STATE_" + str(state.ID) + "_" + str(state.names[i][0]), "\n\t\t}", file=f)

                    print ("\t\telse={\n\t\t\treset_state_name=yes\n\t\t}\n\t}", file=f)

                for prov in state.provinces:
                    if len(provincesArray[int(prov)].names) > 1:
                        print ("\tif={\t\t\t#" + str(provincesArray[int(prov)].names[0][1]) + "\n\t\tlimit={ any_country={ controls_province = " + str(prov) + " "\
                            + str(provincesArray[int(prov)].names[1][0]) + " = yes } }\n\t\tset_province_name = { id = "\
                            + str(prov) + " name = VICTORY_POINTS_" + str(prov) + "_"\
                            + str(provincesArray[int(prov)].names[1][0]) + " }\n\t}",file=f)
                        if len(provincesArray[int(prov)].names) > 2:
                            for i in range(2,len(provincesArray[int(prov)].names)):
                                print ("\telse_if={\n\t\tlimit={ any_country={ controls_province = " + str(prov) + " "\
                                    + str(provincesArray[int(prov)].names[i][0]) + " = yes } }\n\t\tset_province_name = { id = "\
                                    + str(prov) + " name = VICTORY_POINTS_" + str(prov) + "_"\
                                    + str(provincesArray[int(prov)].names[i][0]) + " }\n\t}",file=f)
                        
                        print ("\telse={\n\t\treset_province_name = " + str(prov) +  "\n\t}",file=f)
                    

                print ("}", file=f)
        print ("\n\nchange_city_names={\n\tZZZ={", file=f)
        for i in range (1,len(statesArray)):
            print ("\t\tupdate_state_" + str(i) + "_names=yes", file=f)
        print ("\t}\n}\nrevert_city_names_to_original={\n\tevery_state = { reset_state_name=yes }", file=f)
        for state in statesArray:
            if state.ID!=0:
                for i in range(0,len(state.names)):
                    if str(state.names[i][0]) == "IS_2016_DECOM":       #Can add more in the future if there's the option to change city names
                        print ("\t" + str(state.ID) + "={\n\t\tif={\n\t\t\tlimit={ "\
                            + str(state.names[i][0]) + " = yes }\n\t\t\tset_state_name = STATE_"\
                            + str(state.ID) + "_" + str(state.names[i][0])\
                            + "\n\t\t}\n\t\telse={ reset_state_name = yes }\n\t}",file=f)
        
        for prov in provincesArray:
            if prov.names[0] !=None:
                hasUniqueDefaultName = False
                for i in range(0,len(prov.names)):
                    if str(prov.names[i][0]) == "IS_2016_DECOM":
                        hasUniqueDefaultName = True
                        print ("\tif={\n\t\tlimit = { " + str(prov.names[i][0]) + " = yes }\n\t\tset_province_name = { id = "\
                            + str(prov.ID) + " name = VICTORY_POINTS_" + str(prov.ID) + "_" + str(prov.names[i][0])\
                            + " }\n\t}\n\telse={\n\t\tset_province_name = { id = " + str(prov.ID) + " name = VICTORY_POINTS_" + str(prov.ID) + " }\n\t}", file=f)
                        
                    elif i == (len(prov.names)-1) and hasUniqueDefaultName == False:
                        print ("\tset_province_name = { id = " + str(prov.ID) + " name = VICTORY_POINTS_" + str(prov.ID) + " }", file=f)

        print ("}", file=f)

def write_definitions_csv(provincesArray):
    current_directory = os.getcwd()
    definition_csv_file = os.path.join(current_directory, "__code__", "map", "definition.csv")
    with open(definition_csv_file, 'w', encoding='utf-8') as f:
        for prov in provincesArray:
            red = int(prov.hexadecimal[0:2], 16) 
            green = int(prov.hexadecimal[2:4], 16) 
            blue = int(prov.hexadecimal[4:], 16) 
            print(str(prov.ID)+";" + str(red)+";"+str(green)+";"+str(blue)+";"+prov.type\
                  +";" + str.lower(str(prov.coastal))+";"+prov.terrain+";"+str(prov.continent),file=f)

def write_buildings_position_files(provincesArray, statesArray, buildingsArray, terrainArray):
    current_directory = os.getcwd()
    rocketsites_file = os.path.join(current_directory, "__code__", "map", "rocketsites.txt")
    airports_file = os.path.join(current_directory, "__code__", "map", "airports.txt")
    buildings_file = os.path.join(current_directory, "__code__", "map", "buildings.txt")

    provincesImage = Image.open(current_directory+"\\map\\provinces.bmp")
    width, height = provincesImage.size
    provincesImage.close()

    rocketsiteProvs = []
    airportProvs = []
    statesArray.pop(0)
    noOfStates = len(statesArray)
    with open(buildings_file, 'w', encoding='utf-8') as f:
        for i in range(0,noOfStates):
            state = statesArray[0]
            for building in buildingsArray:
                if building.provincial == False:
                    for i in range(0,building.show_on_map):
                        if building.only_coastal == False:
                            random_prov = int(random.choice(state.provinces))
                            terrain_is_water = False
                            for t in terrainArray:
                                if t.name == provincesArray[random_prov].terrain and t.is_water == True:
                                    terrain_is_water = True
                            while terrain_is_water == True:
                                random_prov = int(random.choice(state.provinces))
                                terrain_is_water = False
                                for t in terrainArray:
                                    if t.name == provincesArray[random_prov].terrain and t.is_water == True:
                                        terrain_is_water = True

                            random_coords = random.choice(provincesArray[random_prov].coordinates)
                            random_rotat = random.uniform(0.0, 6.27)
                            random_rotat = float("{:.2f}".format(random_rotat))
                            array = return_binary_array(random_coords[1])
                            y_axis = float(array[random_coords[0]][4])
                            y_axis = y_axis/10

                            adjacent_coastal_province = 0

                            print (str(state.ID) + ";" + building.name + ";"+ str(random_coords[0]) + ".00;"+ str(y_axis)\
                                +"0;" + str(height-random_coords[1]) + ".00;" + str(random_rotat)+";"+str(adjacent_coastal_province), file=f)
                        else:
                            coastal_provs = []
                            for prov in state.provinces:
                                if provincesArray[int(prov)].coastal == True:
                                    coastal_provs.append(int(prov))

                            if coastal_provs:
                                random_prov = int(random.choice(coastal_provs))
                                terrain_is_water = False
                                for t in terrainArray:
                                    if t.name == provincesArray[random_prov].terrain and t.is_water == True:
                                        terrain_is_water = True
                                while terrain_is_water == True:
                                    random_prov = int(random.choice(coastal_provs))
                                    terrain_is_water = False
                                    for t in terrainArray:
                                        if t.name == provincesArray[random_prov].terrain and t.is_water == True:
                                            terrain_is_water = True
                                coastal_prov_coordinates = []
                                for bc in provincesArray[random_prov].border_coords:
                                    current_prov = int(bc[2])
                                    current_prov_is_naval = False
                                    current_prov_terrain = provincesArray[current_prov].terrain
                                    for t in terrainArray:
                                        if t.name == current_prov_terrain and t.naval == True:
                                            current_prov_is_naval = True
                                    if current_prov_is_naval == True:
                                        coastal_prov_coordinates.append(bc)

                                random_coords = random.choice(coastal_prov_coordinates)     #X,Z,prov,direction
                                if random_coords[3] == "north":
                                    random_rotat = random.uniform(6, 6.5)
                                    random_rotat = random_rotat%6.28
                                    random_rotat = float("{:.2f}".format(random_rotat))
                                elif random_coords[3] == "south":
                                    random_rotat = random.uniform(3, 3.5)
                                    random_rotat = float("{:.2f}".format(random_rotat))
                                elif random_coords[3] == "east":
                                    random_rotat = random.uniform(1.25, 1.75)
                                    random_rotat = float("{:.2f}".format(random_rotat))
                                elif random_coords[3] == "west":
                                    random_rotat = random.uniform(4.5, 5)
                                    random_rotat = float("{:.2f}".format(random_rotat))

                                array = return_binary_array(random_coords[1])
                                y_axis = float(array[random_coords[0]][4])
                                y_axis = y_axis/10

                                adjacent_coastal_province = 0

                                print (str(state.ID) + ";" + building.name + ";"+ str(random_coords[0]) + ".00;"+ str(y_axis)\
                                    +"0;" + str(height-random_coords[1]) + ".00;" + str(random_rotat)+";"+str(adjacent_coastal_province), file=f)
                        
                        if building.name == "air_base":
                            airportProvs.append(random_prov)
                        elif building.name == "rocket_site":
                            rocketsiteProvs.append(random_prov)
                else:
                    if building.show_on_map != 0:
                        for i in range(0,len(state.provinces)):
                            provClass = provincesArray[int(state.provinces[i])]
                            terrain_is_water = False
                            for t in terrainArray:
                                if t.name == provClass.terrain and t.is_water == True:
                                    terrain_is_water = True
                            if terrain_is_water == False:
                                if building.only_coastal == False:
                                    random_coords = random.choice(provClass.coordinates)
                                    random_rotat = random.uniform(0.0, 6.27)
                                    random_rotat = float("{:.2f}".format(random_rotat))
                                    array = return_binary_array(random_coords[1])
                                    y_axis = float(array[random_coords[0]][4])
                                    y_axis = y_axis/10
                                    adjacent_coastal_province = 0
                                    print (str(state.ID) + ";" + building.name + ";"+ str(random_coords[0]) + ".00;"+ str(y_axis)\
                                            +"0;" + str(height-random_coords[1]) + ".00;" + str(random_rotat)+";"+str(adjacent_coastal_province), file=f)
                                elif building.only_coastal == True and provClass.coastal == True:
                                    coastal_prov_coordinates = []
                                    for bc in provClass.border_coords:
                                        current_prov = int(bc[2])
                                        current_prov_is_naval = False
                                        current_prov_terrain = provincesArray[current_prov].terrain
                                        for t in terrainArray:
                                            if t.name == current_prov_terrain and t.naval == True:
                                                current_prov_is_naval = True
                                        if current_prov_is_naval == True:
                                            coastal_prov_coordinates.append(bc)

                                    random_coords = random.choice(coastal_prov_coordinates)     #X,Z,prov,direction
                                    if random_coords[3] == "north":
                                        random_rotat = random.uniform(6, 6.5)
                                        random_rotat = random_rotat%6.28
                                        random_rotat = float("{:.2f}".format(random_rotat))
                                    elif random_coords[3] == "south":
                                        random_rotat = random.uniform(3, 3.5)
                                        random_rotat = float("{:.2f}".format(random_rotat))
                                    elif random_coords[3] == "east":
                                        random_rotat = random.uniform(1.25, 1.75)
                                        random_rotat = float("{:.2f}".format(random_rotat))
                                    elif random_coords[3] == "west":
                                        random_rotat = random.uniform(4.5, 5)
                                        random_rotat = float("{:.2f}".format(random_rotat))

                                    array = return_binary_array(random_coords[1])
                                    y_axis = float(array[random_coords[0]][4])
                                    y_axis = y_axis/10

                                    if building.is_port == True:
                                        adjacent_coastal_province = random_coords[2]
                                    else:
                                        adjacent_coastal_province = 0

                                    print (str(state.ID) + ";" + building.name + ";"+ str(random_coords[0]) + ".00;"+ str(y_axis)\
                                        +"0;" + str(height-random_coords[1]) + ".00;" + str(random_rotat)+";"+str(adjacent_coastal_province), file=f)
                            

            statesArray.pop(0)
                            
    with open(rocketsites_file, 'w', encoding='utf-8') as f:
        for i in range(0,len(rocketsiteProvs)):
            print(str(i+1),"={ " + str(rocketsiteProvs[i]) + " }",file=f)
    
    with open(airports_file, 'w', encoding='utf-8') as f:
        for i in range(0,len(airportProvs)):
            print(str(i+1),"={ " + str(airportProvs[i]) + " }",file=f)