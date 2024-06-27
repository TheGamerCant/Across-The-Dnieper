import os

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
                        print("\t\tadd_core_of = " + str(state.cores[i][0]), file=f)
                if state.claims[0] != None:
                    for i in range (0,len(state.claims)):
                        print("\t\tadd_claim_by = " + str(state.claims[i][0]), file=f)
                if state.stateFlags[0] != None:
                    for i in range (0,len(state.stateFlags)):
                        print("\t\tset_state_flag = " + str(state.stateFlags[i][0]), file=f)
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
                        print ("\t\t" + str(state.dateInfo[i][0])+"."+str(state.dateInfo[i][1])+"."+str(state.dateInfo[i][2])\
                               +"={"+str(state.dateInfo[i][3])+"}", file=f)
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