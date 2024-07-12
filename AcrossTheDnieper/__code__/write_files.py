import os
import random
import math
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

    variation_radii = 0.25      #Amount of variation in radii for angles

    rocketsiteProvs = []
    airportProvs = []
    statesArray.pop(0)
    noOfStates = len(statesArray)

    #Remove all lakes/water tiles from state provinces
    for state in statesArray:
        nonWaterProvs = []
        for prov in state.provinces:
            currentProv = provincesArray[int(prov)]
            t = currentProv.terrain
            for terrain in terrainArray:
                if terrain.name == t and terrain.naval == False and terrain.is_water == False:
                    nonWaterProvs.append(prov)
        
        state.provinces = nonWaterProvs
                    

            
    with open(buildings_file, 'w', encoding='utf-8') as f:
        for i in range(0,noOfStates):
            state = statesArray[0]
            for building in buildingsArray:
                #Non-provincial, show_on_map no of buildings for the entire state
                if building.provincial == False and building.show_on_map != 0:
                    for i in range (0, building.show_on_map):
                        if building.only_coastal == True and state.coastal == True:
                            #Bulding and state are coastal

                            #Duplicate states provinces and randomise order
                            #Go through array. If province is coastal return that as the selected province, otherwise delete from array and go again
                            coastal_prov = -1
                            duplicate_provinces_array = state.provinces
                            random.shuffle(duplicate_provinces_array)
                            while coastal_prov == -1:
                                current_prov = int(duplicate_provinces_array[0])
                                if provincesArray[current_prov].coastal == True:
                                    coastal_prov = current_prov
                                else:
                                    duplicate_provinces_array.pop(0)

                            valid_coords = None
                            duplicate_coordinates_array = provincesArray[coastal_prov].border_coords
                            random.shuffle(duplicate_coordinates_array)
                            #Do same as before, with border_coords entries as [X,Y, ProvID, Direction]
                            while valid_coords == None:
                                current_prov = int(duplicate_coordinates_array[0][2])
                                #current_prov is ID of neighbouring province
                                if provincesArray[current_prov].type == "sea":
                                    valid_coords = duplicate_coordinates_array[0]
                                else:
                                    duplicate_coordinates_array.pop(0)

                            #We now have 'coastal_prov', an integer variable corresponding to a province within the state which is coastal
                            #We also have 'valid_coords', an array in the form of [X,Y, ProvID, Direction], telling us what direction to face

                            #Remember - Models are by default facing south, and because the map is flipped horizontally, radians work in reverse - positive is anti-clockwise, negative is clockwise
                            if valid_coords[3] == "north":
                                lower_bound = (math.pi) - variation_radii
                                upper_bound = (math.pi) + variation_radii
                            elif valid_coords[3] == "south":
                                lower_bound = variation_radii*-1
                                upper_bound = variation_radii
                            elif valid_coords[3] == "east":
                                lower_bound = ((math.pi)/2) - variation_radii
                                upper_bound = ((math.pi)/2) + variation_radii
                            elif valid_coords[3] == "west":
                                lower_bound = math.pi + ((math.pi)/2) - variation_radii
                                upper_bound = math.pi + ((math.pi)/2) + variation_radii

                            random_rotat = random.uniform(lower_bound, upper_bound)
                            random_rotat = float("{:.2f}".format(random_rotat))

                            #Return y-value of co-ords as a float (will be to 1 d.p)
                            array = return_binary_array(valid_coords[1])
                            y_axis = float(array[valid_coords[0]][4])
                            y_axis = y_axis/10

                            print (str(state.ID) + ";" + building.name + ";"+ str(valid_coords[0]) + ".00;"+ str(y_axis)\
                                    +"0;" + str(height-valid_coords[1]) + ".00;" + str(random_rotat)+";0", file=f)
                                
                        elif building.only_coastal == False:
                            #Building is non-coastal

                            #Pick random province as integer ID
                            random_prov = int(random.choice(state.provinces))

                            #Pick random coordinates and rotation to 2 d.p
                            random_coords = random.choice(provincesArray[random_prov].coordinates)
                            upper_bound = (math.pi)*2
                            random_rotat = random.uniform(0.0, upper_bound)
                            random_rotat = float("{:.2f}".format(random_rotat))

                            #Return y-value of co-ords as a float (will be to 1 d.p)
                            array = return_binary_array(random_coords[1])
                            y_axis = float(array[random_coords[0]][4])
                            y_axis = y_axis/10

                            if building.name == "air_base":
                                airportProvs.append(random_prov)
                            elif building.name == "rocket_site":
                                rocketsiteProvs.append(random_prov)

                            print (str(state.ID) + ";" + building.name + ";"+ str(random_coords[0]) + ".00;"+ str(y_axis)\
                                    +"0;" + str(height-random_coords[1]) + ".00;" + str(random_rotat)+";0", file=f)

                #Provincial, show_on_map no. of buildings for the province
                elif building.provincial == True and building.show_on_map != 0:
                    if building.only_coastal == True and state.coastal == True:
                        #Building and state are coastal
                        for p in state.provinces:
                            #Go through provinces, only execute code for the prov if province is coastal
                            prov = int(p)
                            if provincesArray[prov].coastal == True:
                                for i in range (0,building.show_on_map):
                                    #Make duplicate and shuffle the border coordinates of the province
                                    valid_coords = None
                                    duplicate_coordinates_array = provincesArray[prov].border_coords
                                    random.shuffle(duplicate_coordinates_array)
                                    while valid_coords == None:
                                        current_prov = int(duplicate_coordinates_array[0][2])
                                        #current_prov is ID of neighbouring province
                                        if provincesArray[current_prov].type == "sea":
                                            valid_coords = duplicate_coordinates_array[0]
                                        else:
                                            duplicate_coordinates_array.pop(0)

                                    #Right now, we have the variable 'prov', the integer ID of the coastal province
                                    #As well as the array 'valid_coords' in the form [X,Y, ProvID, Direction]

                                    if valid_coords[3] == "north":
                                        lower_bound = (math.pi) - variation_radii
                                        upper_bound = (math.pi) + variation_radii
                                    elif valid_coords[3] == "south":
                                        lower_bound = variation_radii*-1
                                        upper_bound = variation_radii
                                    elif valid_coords[3] == "east":
                                        lower_bound = ((math.pi)/2) - variation_radii
                                        upper_bound = ((math.pi)/2) + variation_radii
                                    elif valid_coords[3] == "west":
                                        lower_bound = math.pi + ((math.pi)/2) - variation_radii
                                        upper_bound = math.pi + ((math.pi)/2) + variation_radii

                                    random_rotat = random.uniform(lower_bound, upper_bound)
                                    random_rotat = float("{:.2f}".format(random_rotat))

                                    #Return y-value of co-ords as a float (will be to 1 d.p)
                                    array = return_binary_array(valid_coords[1])
                                    y_axis = float(array[valid_coords[0]][4])
                                    y_axis = y_axis/10

                                    if building.is_port == True:
                                        #If the building is a port, we need the adjacent sea province - this is the sea province the port building is facing
                                        adj_sea_province = int(valid_coords[2])
                                    else:
                                        adj_sea_province = 0

                                    print (str(state.ID) + ";" + building.name + ";"+ str(valid_coords[0]) + ".00;"+ str(y_axis)\
                                            +"0;" + str(height-valid_coords[1]) + ".00;" + str(random_rotat)+";" + str(adj_sea_province), file=f)

                    elif building.only_coastal == False:
                        #Non-coastal, make entites for each prov in the state
                        for p in state.provinces:
                            prov = int(p)
                            for i in range (0,building.show_on_map):
                   
                                #Pick random coordinates and rotation to 2 d.p
                                random_coords = random.choice(provincesArray[prov].coordinates)
                                upper_bound = (math.pi)*2
                                random_rotat = random.uniform(0.0, upper_bound)
                                random_rotat = float("{:.2f}".format(random_rotat))

                                #Return y-value of co-ords as a float (will be to 1 d.p)
                                array = return_binary_array(random_coords[1])
                                y_axis = float(array[random_coords[0]][4])
                                y_axis = y_axis/10

                                print (str(state.ID) + ";" + building.name + ";"+ str(random_coords[0]) + ".00;"+ str(y_axis)\
                                        +"0;" + str(height-random_coords[1]) + ".00;" + str(random_rotat)+";0", file=f)

            #Need seperate code for floating harbours as they're a bit different
            #And by a bit I mean very. Fuck you paradox eat my nuts

            for p in state.provinces:
                #Go through provinces, only execute code for the prov if province is coastal
                prov = int(p)
                if provincesArray[prov].coastal == True:
                    adj_sea_province = prov     #ASP has to be the land province that the floating harbour is facing

                    valid_coords = None
                    duplicate_coordinates_array = provincesArray[prov].border_coords
                    random.shuffle(duplicate_coordinates_array)
                    while valid_coords == None:
                        current_prov = int(duplicate_coordinates_array[0][2])
                        #current_prov is ID of neighbouring province
                        if provincesArray[current_prov].type == "sea":
                            valid_coords = duplicate_coordinates_array[0]
                        else:
                            duplicate_coordinates_array.pop(0)

                    selected_sea_prov = int(valid_coords[2])
                    random_coords = random.choice(provincesArray[selected_sea_prov].coordinates)

                    #Swap the functions 'south' <-> 'north', 'west' <-> 'east'
                    if valid_coords[3] == "south":
                        lower_bound = (math.pi) - variation_radii
                        upper_bound = (math.pi) + variation_radii
                    elif valid_coords[3] == "north":
                        lower_bound = variation_radii*-1
                        upper_bound = variation_radii
                    elif valid_coords[3] == "west":
                        lower_bound = ((math.pi)/2) - variation_radii
                        upper_bound = ((math.pi)/2) + variation_radii
                    elif valid_coords[3] == "east":
                        lower_bound = math.pi + ((math.pi)/2) - variation_radii
                        upper_bound = math.pi + ((math.pi)/2) + variation_radii

                    random_rotat = random.uniform(lower_bound, upper_bound)
                    random_rotat = float("{:.2f}".format(random_rotat))

                    print (str(state.ID) + ";floating_harbor;"+ str(random_coords[0]) + ".00;9.50;" + str(height-random_coords[1]) + ".00;"\
                            + str(random_rotat)+";" + str(adj_sea_province), file=f)

            statesArray.pop(0)

               
    with open(rocketsites_file, 'w', encoding='utf-8') as f:
        for i in range(0,len(rocketsiteProvs)):
            print(str(i+1),"={ " + str(rocketsiteProvs[i]) + " }",file=f)
    
    with open(airports_file, 'w', encoding='utf-8') as f:
        for i in range(0,len(airportProvs)):
            print(str(i+1),"={ " + str(airportProvs[i]) + " }",file=f)