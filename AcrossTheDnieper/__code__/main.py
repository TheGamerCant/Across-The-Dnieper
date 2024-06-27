import os 
import tkinter 

from func import returnStringBetweenBrackets
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




def main():
    buildingsArray=load_buildings()
    terrainArray=load_terrain()
    provincesArray = load_provinces()
    statesArray = load_states(provincesArray,buildingsArray)
    strategicRegionArray = load_strategic_regions(provincesArray)

    print ("")

if __name__ == "__main__":
    main()