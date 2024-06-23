#include <iostream>
#include <filesystem>
#include "load_provs.h"

int main() {
    // Get the current working directory
    std::filesystem::path current_path = std::filesystem::current_path();

    // Move up one directory to get the base directory
    std::filesystem::path base_directory = current_path.parent_path();

    // Construct the path to the map folder and the definition.csv file
    std::filesystem::path map_folder_path = base_directory / "map";
    std::filesystem::path definitions_csv_file_path = map_folder_path / "definition.csv";

    // Convert the path to a string
    std::string filename = definitions_csv_file_path.string();

    std::vector<Province> provinces = loadProvinces(filename);

    for (const auto& province : provinces) {
        std::cout << "ID: " << province.id
            << ", Red: " << province.red
            << ", Green: " << province.green
            << ", Blue: " << province.blue
            << ", Type: " << province.type
            << ", Coastal: " << (province.coastal ? "true" : "false")
            << ", Terrain: " << province.terrain
            << ", Continent: " << province.continent
            << std::endl;
    }

    return 0;
}
