#include <string>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <vector>
#include <algorithm>
#include <regex>
#include <stdexcept>

#include "load_map.hpp"
#include "func.hpp"
using namespace std;

vector<string> loadNameIdentifiers(const string& filename){
    vector<string>nameIdentifiers;
    nameIdentifiers.push_back("DEFAULT");
    ifstream file(filename);
    string fileContent((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    regex whiteSpaceRegex("\\s+");
    fileContent = regex_replace(fileContent, whiteSpaceRegex, " ");

    int continueLoop = fileContent.find('{')!= string::npos;
    while(continueLoop==1){
        int bracketPos = fileContent.find('{');
        string triggerContent = returnBetweenBrackets(fileContent,fileContent.substr(0,bracketPos));
        int contentPos = fileContent.find(triggerContent); 
        fileContent.erase(fileContent.begin()+contentPos,fileContent.begin()+contentPos+triggerContent.size());

        regex triggerRegex("(\\w+)\\s*=\\s*\\{\\s*\\}");
        smatch triggerMatch;
        if (regex_search(fileContent, triggerMatch, triggerRegex)) {
            nameIdentifiers.push_back(triggerMatch[1].str());
        }
        fileContent = regex_replace(fileContent, triggerRegex, "");
        continueLoop = fileContent.find('{')!= string::npos;
    }
    return nameIdentifiers;
}

void loadMapNames(const string& filename, vector<stateClass>& statesArray, vector<provinceClass>& provincesArray){
    ifstream file(filename);
    string line;
    bool isProvince = false;
    while (getline(file, line)) {   
        try{  
            if(line.substr(0,7) == " STATE_"){
                line.erase(0,7);
            }else if(line.substr(0,16) == " VICTORY_POINTS_"){
                line.erase(0,16);
                isProvince = true;
            }

            vector<string> nameSplit;
            stringstream ss(line);
            string item;
            while (getline(ss, item, ':')) { nameSplit.push_back(item); }

            int id;
            string name;
            string identifier;

            if(all_of(nameSplit[0].begin(), nameSplit[0].end(), ::isdigit)){
                id = stoi(nameSplit[0]);
                identifier = "DEFAULT";

            } else{
                int firstUnderscore = nameSplit[0].find('_');
                id = stoi(nameSplit[0].substr(0,firstUnderscore));
                identifier = nameSplit[0].substr(firstUnderscore+1);
            }

            regex nameRegex("\"\\s*(.*?)\\s*\"");
            smatch nameMatch;
            if (regex_search(nameSplit[1], nameMatch, nameRegex)) {
                name = nameMatch[1];
            }

            if(isProvince == false){
                statesArray[id].names.insert(make_pair(identifier,name));
            }else{
                provincesArray[id].names.insert(make_pair(identifier,name));
            }
        }catch (...) {}
    }
}