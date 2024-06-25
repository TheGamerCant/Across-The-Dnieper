#ifndef WRITE_TO_FILES_HPP
#define WRITE_TO_FILES_HPP

#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
using namespace std;


void write_definition_csv(const filesystem::path& directory, vector<provinceClass>& provincesArray);
void write_scripted_effects_txt(const filesystem::path& directory, vector<provinceClass>& provincesArray, vector<stateClass>& statesArray);
void write_state_names(const filesystem::path& directory, vector<stateClass>& statesArray);
void write_victory_point_names(const filesystem::path& directory, vector<provinceClass>& provincesArray);
void write_strategic_region_names(const filesystem::path& directory, vector<strategicRegionClass>& strategicRegionsArray);
void write_state_files(const filesystem::path& directory, vector<provinceClass>& provincesArray, vector<stateClass>& statesArray);
void write_strategic_region_files(const filesystem::path& directory, vector<strategicRegionClass>& strategicRegionsArray);
#endif // WRITE_TO_FILES_HPP