#ifndef LOAD_NAMES_HPP
#define LOAD_NAMES_HPP

#include <string>
#include <iostream>
#include <vector>
#include <filesystem>
using namespace std;

vector<string> loadNameIdentifiers(const string& filename);
void loadMapNames(const string& filename, vector<stateClass>& statesArray, vector<provinceClass>& provincesArray);

#endif // LOAD_NAMES_HPP