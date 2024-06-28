from load_map import buildingClass
from load_map import provinceClass
from load_map import stateClass
from load_map import strategicRegionClass
from load_map import terrainClass
from load_map import load_buildings
from load_map import load_terrain
from load_map import load_states
from load_map import load_provinces
from load_map import load_strategic_regions
from load_map import load_names
from load_map import load_triggers
from func import delete_and_create_new_folders
from img_handling import save_prov_bin_file
from img_handling import return_binary_array
from write_files import write_history_files
from write_files import write_strategic_region_files
from write_files import write_loc_files
from write_files import write_state_names_scripted_effects_files

from GUI import tkinter_main




def main():
    print ("Loading data types:")
    buildingsArray=load_buildings()
    terrainArray=load_terrain()
    triggersArray = load_triggers()
    print ("Loading provinces, states and strategic regions:")
    provincesArray = load_provinces()
    statesArray = load_states(provincesArray,buildingsArray)
    strategicRegionsArray = load_strategic_regions(provincesArray)
    load_names(provincesArray,statesArray)

    print ("Saving province data as binary:")
    delete_and_create_new_folders()
    #save_prov_bin_file(provincesArray)

    print ("Launching interface:")
    tkinter_main(provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray)

    #print("Writing to files:")
    #write_history_files(provincesArray,statesArray)
    #write_strategic_region_files(strategicRegionsArray)
    #write_loc_files(provincesArray,statesArray,strategicRegionsArray)
    #write_state_names_scripted_effects_files(provincesArray,statesArray)



if __name__ == "__main__":
    main()