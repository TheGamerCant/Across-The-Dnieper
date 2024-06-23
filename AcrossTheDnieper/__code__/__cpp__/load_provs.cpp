#include "load_provs.h"
#include <fstream>
#include <sstream>
#include <iostream>

Province::Province(int id, int red, int green, int blue, const std::string& type, bool coastal, const std::string& terrain, int continent)
    : id(id), red(red), green(green), blue(blue), type(type), coastal(coastal), terrain(terrain), continent(continent) {}

std::vector<Province> loadProvinces(const std::string& filename) {
    std::vector<Province> provinces;
    std::ifstream file(filename);
    std::string line;

    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return provinces;
    }

    while (std::getline(file, line)) {
        std::istringstream ss(line);
        std::string token;
        std::vector<std::string> tokens;

        while (std::getline(ss, token, ';')) {
            tokens.push_back(token);
        }

        if (tokens.size() == 8) {
            int id = std::stoi(tokens[0]);
            int red = std::stoi(tokens[1]);
            int green = std::stoi(tokens[2]);
            int blue = std::stoi(tokens[3]);
            std::string type = tokens[4];
            bool coastal = (tokens[5] == "true");
            std::string terrain = tokens[6];
            int continent = std::stoi(tokens[7]);

            provinces.emplace_back(id, red, green, blue, type, coastal, terrain, continent);
        }
    }

    return provinces;
}
