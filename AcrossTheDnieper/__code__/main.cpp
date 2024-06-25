#include <QApplication>
#include <iostream>
#include <filesystem>
#include <algorithm>
#include <string>
#include "load_map.hpp"
#include "load_names.hpp"
#include "write_to_files.hpp"
#include "gui.hpp"
#include "func.hpp"

int main(int argc, char *argv[]) {
    filesystem::path current_path = filesystem::current_path();
    filesystem::path base_directory = current_path.parent_path();
    base_directory = base_directory.parent_path(); base_directory = base_directory.parent_path();
    filesystem::path map_folder_path = base_directory / "map";
    filesystem::path definitions_csv_file_path = map_folder_path / "definition.csv";
    filesystem::path history_states_folder_path = base_directory / "history\\states";
    filesystem::path strategic_regions_folder_path = map_folder_path / "strategicregions";

    cout << "Loading provinces:" << endl;
    vector<provinceClass> provincesArray = loadProvinces(definitions_csv_file_path.string());
    cout << "Loading states:" << endl;
    vector<stateClass> statesArray = loadStates(history_states_folder_path, provincesArray);
    sort(statesArray.begin(), statesArray.end(), [](const stateClass& a, const stateClass& b) { return a.id < b.id; });     //Sort states by ID
    cout << "Loading strategic regions:" << endl;
    vector<strategicRegionClass> strategicRegionsArray = loadStrategicRegions(strategic_regions_folder_path, provincesArray);
    sort(strategicRegionsArray.begin(), strategicRegionsArray.end(), [](const strategicRegionClass& a, const strategicRegionClass& b) { return a.id < b.id; });     //Sort strategic regions by ID

    cout << "Loading names:" << endl;
    filesystem::path localisation_english_folder_path = base_directory / "localisation\\english";
    filesystem::path victory_points_names_path = localisation_english_folder_path / "victory_points_l_english.yml";
    filesystem::path state_names_path = localisation_english_folder_path / "state_names_l_english.yml";

    loadMapNames(state_names_path.string(), statesArray, provincesArray);
    loadMapNames(victory_points_names_path.string(), statesArray, provincesArray);
    
    bool isAtD = true;
    try{        //Code should work fine if the file exists, if it doesn't just create "DEFAULT"
        filesystem::path identifiers_file_path = base_directory / "common\\scripted_triggers\\state_controller_scripted_triggers.txt";
        vector<string>nameIdentifiers = loadNameIdentifiers(identifiers_file_path.string());
    }catch (...) {vector<string>nameIdentifiers;nameIdentifiers.push_back("DEFAULT"); isAtD=false;}


    vector<filesystem::path> foldersToDelete={
        current_path / "common",
        current_path / "history",
        current_path / "localisation",
        current_path / "map"
    };

    for (const auto& dir : foldersToDelete) {
        try { if (filesystem::remove_all(dir)) { } 
        } catch (...) { }
    }

    vector<filesystem::path> foldersToCreate={
        current_path / "common",
        current_path / "common\\scripted_effects",
        current_path / "history",
        current_path / "history\\states",
        current_path / "localisation",
        current_path / "localisation\\english",
        current_path / "map",
        current_path / "map\\strategicregions"
    };

    for (const auto& dir : foldersToCreate) {
        try { if (filesystem::create_directory(dir)) { } 
        } catch (...) { }
    }

    int width, height;
    cout << "Loading province positions:" << endl;
    filesystem::path provincesBmpPath = map_folder_path / "provinces.bmp";
    loadProvinceMap(provincesBmpPath.string(), provincesArray, width, height);
    //Use 'stbi_image_free(data);' to empty image memory

    cout << "Launching interface:" << endl;
    createWindowGUI(argc, argv, width, height, provincesArray);


    cout << "Writing to files:" << endl;
    map_folder_path = current_path / "map";
    write_definition_csv(map_folder_path, provincesArray);
    if(isAtD == true){
        filesystem::path scripted_effects_folder_path = current_path / "common\\scripted_effects";
        write_scripted_effects_txt(scripted_effects_folder_path, provincesArray, statesArray);
    }

    localisation_english_folder_path = current_path / "localisation\\english";
    write_state_names(localisation_english_folder_path, statesArray);
    write_victory_point_names(localisation_english_folder_path, provincesArray);
    write_strategic_region_names(localisation_english_folder_path, strategicRegionsArray);

    history_states_folder_path = current_path / "history\\states";
    write_state_files(history_states_folder_path, provincesArray, statesArray);

    strategic_regions_folder_path = current_path / "map\\strategicregions";
    write_strategic_region_files(strategic_regions_folder_path, strategicRegionsArray);

    return 0;
}
