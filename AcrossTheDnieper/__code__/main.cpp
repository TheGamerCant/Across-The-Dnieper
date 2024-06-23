#include <iostream>
#include <filesystem>
#include <algorithm>
#include <string>
#include "load_map.hpp"
#include "func.hpp"

int main() {
    filesystem::path current_path = filesystem::current_path();
    filesystem::path base_directory = current_path.parent_path();
    filesystem::path map_folder_path = base_directory / "map";
    filesystem::path definitions_csv_file_path = map_folder_path / "definition.csv";
    filesystem::path history_states_folder_path = base_directory / "history\\states";

    vector<provinceClass> provincesArray = loadProvinces(definitions_csv_file_path.string());
    vector<stateClass> statesArray = loadStates(history_states_folder_path, provincesArray);
    sort(statesArray.begin(), statesArray.end(), [](const stateClass& a, const stateClass& b) { return a.id < b.id; });

//    for (const auto& province : provincesArray) {
//        cout << "ID: " << province.id 
//            << ", Red: " << province.red
//            << ", Green: " << province.green 
//            << ", Blue: " << province.blue 
//            << ", Type: " << province.type 
//            << ", Coastal: " << (province.coastal ? "true" : "false") 
//            << ", Terrain: " << province.terrain 
//            << ", Continent: " << province.continent 
//            << endl;
//    }

    
    return 0;
}
