#include "load_map.hpp"
#include "func.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <regex>
#include <map>
#include <stdexcept>



provinceClass::provinceClass(int id, string hexadecimal, string type, bool coastal, string terrain, int continent, int state, 
        int victoryPoints, map<string, int>buildings, int strategicRegion, map<string, string> names, map<int, int> coordinates)
    : id(id), hexadecimal(hexadecimal), type(type), coastal(coastal), terrain(terrain), continent(continent), 
    state(state), victoryPoints(victoryPoints), buildings(buildings), strategicRegion(strategicRegion), names(names), coordinates(coordinates) {}

vector<provinceClass> loadProvinces(const string& filename) {
    vector<provinceClass> provinces;
    map<string, int> buildings;
    map<string, string> names;
    map<int, int> coordinates;
    ifstream file(filename);
    string line;

    while (getline(file, line)) {
        istringstream ss(line);
        string token;
        vector<string> tokens;

        while (getline(ss, token, ';')) {
            tokens.push_back(token);
        }

        if (tokens.size() == 8) {
            int id = stoi(tokens[0]);
            int red = stoi(tokens[1]);
            int green = stoi(tokens[2]);
            int blue = stoi(tokens[3]);
            string type = tokens[4];
            bool coastal = (tokens[5] == "true");
            string terrain = tokens[6];
            int continent = stoi(tokens[7]);

            string hexadecimal;
            stringstream redHex; stringstream greenHex; stringstream blueHex;
            redHex << hex << red; greenHex << hex << green; blueHex << hex << blue;
            
            if((redHex.str()).size()==1){hexadecimal+="0";}
            hexadecimal+=redHex.str();
            if((greenHex.str()).size()==1){hexadecimal+="0";}
            hexadecimal+=greenHex.str();
            if((blueHex.str()).size()==1){hexadecimal+="0";}
            hexadecimal+=blueHex.str();
            

            provinces.emplace_back(id, hexadecimal, type, coastal, terrain, continent, 0, 0, buildings,0, names, coordinates);
        }
    }
    return provinces;
}

stateClass::stateClass(int id, vector<int>provinces, map<string, int> resources, bool impassable, int manpower
        , string stateCategory,map<string, string> dateInfo, string owner, vector<string> cores, vector<string> claims, vector<string> stateFlags, map<string, int> buildings, map<string, string> names)
    :id(id), provinces(provinces), resources(resources), impassable(impassable), manpower(manpower), stateCategory(stateCategory), 
    dateInfo(dateInfo), owner(owner), cores(cores), claims(claims), stateFlags(stateFlags), buildings(buildings), names(names) {}

vector <stateClass> loadStates(const filesystem::path& historyStatesPath, vector<provinceClass>& provincesArray) {
    //Create templates and create state '0'
    vector<stateClass> states;
    int id = -1;
    vector<int> provs;
    map<string, int> resources;
    bool impassable = false;
    int manpower = 0;
    string stateCategory = "";
    map<string, string> dateInfo;
    string owner;
    vector<string> cores;
    vector<string> claims;
    vector<string> stateFlags;
    map<string, int> buildings;
    map<string, string> names;
    states.emplace_back(0,provs,resources,false,0,"",dateInfo, owner, cores, claims, stateFlags, buildings, names);


    auto BEGIN = sregex_iterator();
    auto END = sregex_iterator();
    regex nameValueRegex("(\\w+)\\s*=\\s*(\\d+)");
    smatch nameValueMatch;
    

    //Go through files
    for (const auto& file : filesystem::directory_iterator(historyStatesPath)) {
        if (file.is_regular_file() && file.path().extension() == ".txt") {
            ifstream currentFile(file.path());
            string fileContent((istreambuf_iterator<char>(currentFile)), istreambuf_iterator<char>());
            regex whiteSpaceRegex("\\s+");
            fileContent = regex_replace(fileContent, whiteSpaceRegex, " ");

            
            string historyContent = returnBetweenBrackets(fileContent, "history");
            int historyContentPosition = fileContent.find(historyContent);
            fileContent.erase(fileContent.begin()+historyContentPosition,fileContent.begin()+historyContentPosition+historyContent.size());
            regex historyRegex("history\\s*=\\s*\\{\\s*\\}\\s*");
            fileContent = regex_replace(fileContent, historyRegex, "");

            string buildingsContent = returnBetweenBrackets(historyContent, "buildings");
            int buildingsContentPosition = historyContent.find(buildingsContent);
            historyContent.erase(historyContent.begin()+buildingsContentPosition,historyContent.begin()+buildingsContentPosition+buildingsContent.size());
            regex buildingsRegex("buildings\\s*=\\s*\\{\\s*\\}\\s*");
            historyContent = regex_replace(historyContent, buildingsRegex, "");
            

            regex idRegex("id\\s*=\\s*(\\d+)");
            smatch idMatch;
            if (regex_search(fileContent, idMatch, idRegex)) {
                id = stoi(idMatch[1]);
            }
            fileContent = regex_replace(fileContent, idRegex, "");

            string provincesString = returnBetweenBrackets(fileContent, "provinces");
            stringstream iss(provincesString);
            int province;
            while ( iss >> province ){
                provincesArray[province].state = id;
                provs.push_back(province); 
            }
            int provincesPosition = fileContent.find(provincesString);
            fileContent.erase(fileContent.begin()+provincesPosition,fileContent.begin()+provincesPosition+provincesString.size());
            regex provincesRegex("provinces\\s*=\\s*\\{\\s*\\}\\s*");
            fileContent = regex_replace(fileContent, provincesRegex, "");

            regex resourcesRegex("resources\\s*=\\s*\\{\\s*(.*?)\\s*\\}");
            smatch resourcesMatch;
            if (regex_search(fileContent, resourcesMatch, resourcesRegex)) {
                string resourcesString = resourcesMatch.str(1);
                BEGIN = sregex_iterator(resourcesString.begin(), resourcesString.end(), nameValueRegex);
                END = sregex_iterator();
                for (sregex_iterator i = BEGIN; i != END; ++i) {
                    smatch resoursesMatch2 = *i;
                    resources.insert(make_pair(resoursesMatch2[1],stoi(resoursesMatch2[2])));
                }
            }
            fileContent = regex_replace(fileContent, resourcesRegex, "");
            
            regex impassableRegex("impassable\\s*=\\s*(\\w+)");
            smatch impassableMatch;
            if (regex_search(fileContent, impassableMatch, impassableRegex)) {
                if (impassableMatch[1] == "yes"){ impassable = true; }
            }
            fileContent = regex_replace(fileContent, impassableRegex, "");

            regex manpowerRegex("manpower\\s*=\\s*(\\d+)");
            smatch manpowerMatch;
            if (regex_search(fileContent, manpowerMatch, manpowerRegex)) {
                manpower = stoi(manpowerMatch[1]);
            }
            fileContent = regex_replace(fileContent, manpowerRegex, "");

            regex stateCategoryRegex("state_category\\s*=\\s*(\\w+)");
            smatch stateCategoryMatch;
            if (regex_search(fileContent, stateCategoryMatch, stateCategoryRegex)) {
                stateCategory = stateCategoryMatch[1];
            }
            fileContent = regex_replace(fileContent, stateCategoryRegex, "");
            //cout << fileContent << endl << historyContent<< endl;

            //Only accept dates in the format "YYYY.M(M).D(D)"
            regex dateInfoRegex("(\\d{4})\\.(\\d{1,2})\\.(\\d{1,2})");
            BEGIN = sregex_iterator(historyContent.begin(), historyContent.end(), dateInfoRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                //Create map of string date and string of the info between the brackets after the date
                //This allows for multiple dates
                //E.G an item in the map might be ["2022.1.1", "owner = DON controller = DON add_core_of = DON"]
                string dateInfoString = returnBetweenBrackets(historyContent,(*i).str());
                dateInfo.insert(make_pair((*i).str(),dateInfoString));

                int dateInfoContentPostion = historyContent.find(dateInfoString);
                historyContent.erase(historyContent.begin()+dateInfoContentPostion,historyContent.begin()+dateInfoContentPostion+dateInfoString.size());
            }
            regex dateInfoRegexRemove("(\\d{4})\\.(\\d{1,2})\\.(\\d{1,2})\\s*=\\s*\\{\\s*\\}");
            historyContent = regex_replace(historyContent, dateInfoRegexRemove, "");

            regex ownerRegex("owner\\s*=\\s*(\\w+)");
            smatch ownerMatch;
            if (regex_search(historyContent, ownerMatch, ownerRegex)) {
                //cout << ownerMatch.str(0) << ", " << ownerMatch.str(1);
                owner = ownerMatch[1];
            }
            historyContent = regex_replace(historyContent, ownerRegex, "");

            regex coresRegex("add_core_of\\s*=\\s*(\\w+)");
            BEGIN = sregex_iterator(historyContent.begin(), historyContent.end(), coresRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                smatch coreMatch = *i;
                cores.push_back(coreMatch[1].str());
            }
            historyContent = regex_replace(historyContent, coresRegex, "");

            regex claimsRegex("add_claim_by\\s*=\\s*(\\w+)");
            BEGIN = sregex_iterator(historyContent.begin(), historyContent.end(), claimsRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                smatch claimMatch = *i;
                claims.push_back(claimMatch[1].str());
            }
            historyContent = regex_replace(historyContent, claimsRegex, "");

            regex stateFlagRegex("set_state_flag\\s*=\\s*(\\w+)");
            BEGIN = sregex_iterator(historyContent.begin(), historyContent.end(), stateFlagRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                smatch stateFlagMatch = *i;
                stateFlags.push_back(stateFlagMatch[1].str());
            }
            historyContent = regex_replace(historyContent, stateFlagRegex, "");

            regex victoryPointRegex("victory_points\\s*=\\s*\\{\\s*(\\d+)\\s*(\\d+)\\s*\\}");
            BEGIN = sregex_iterator(historyContent.begin(), historyContent.end(), victoryPointRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                smatch victoryPointMatch = *i;
                int vpID = stoi(victoryPointMatch[1].str());
                int vpIValue = stoi(victoryPointMatch[2].str());
                provincesArray[vpID].victoryPoints = vpIValue;
            }
            historyContent = regex_replace(historyContent, victoryPointRegex, "");

            regex provinceBuildingsRegex("(\\d+)\\s*=\\s*\\{(.*?)\\}");
            BEGIN = sregex_iterator(buildingsContent.begin(), buildingsContent.end(), provinceBuildingsRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                smatch provinceBuildingMatch = *i;
                //cout << id << " - " << provinceBuildingMatch[1].str() << ", " << provinceBuildingMatch[2].str() << endl;
                string provinceBuildingsString = provinceBuildingMatch[2].str();
                int provinceID = stoi(provinceBuildingMatch[1].str());
                auto BEGIN2 = sregex_iterator(provinceBuildingsString.begin(), provinceBuildingsString.end(), nameValueRegex);
                auto END2 = sregex_iterator();
                for (sregex_iterator i = BEGIN2; i != END2; ++i) {
                    smatch provinceBuildingMatch2 = *i;
                    provincesArray[provinceID].buildings.insert(make_pair(provinceBuildingMatch2[1],stoi(provinceBuildingMatch2[2])));
                }
            }
            buildingsContent = regex_replace(buildingsContent, provinceBuildingsRegex, "");

            BEGIN = sregex_iterator(buildingsContent.begin(), buildingsContent.end(), nameValueRegex);
            END = sregex_iterator();
            for (sregex_iterator i = BEGIN; i != END; ++i) {
                smatch buildingMatch = *i;
                buildings.insert(make_pair(buildingMatch[1],stoi(buildingMatch[2])));
            }

            //if(id==354){ cout << id << " - " << fileContent << endl << historyContent << << endl; }

            states.emplace_back(id,provs,resources,impassable,manpower,stateCategory,dateInfo, owner, cores, claims, stateFlags, buildings, names);
            provs.clear(); resources.clear(); dateInfo.clear(); cores.clear(); claims.clear(); stateFlags.clear(); buildings.clear(); impassable = false;
        }
    }
    return states;
}

strategicRegionClass::strategicRegionClass(int id, vector<int>provinces, string name)
    : id(id), provinces(provinces), name(name) {}

vector <strategicRegionClass> loadStrategicRegions(const filesystem::path& strategicRegionsPath, vector<provinceClass>& provincesArray) {
    //Create templates and create strategic region '0'
    vector<strategicRegionClass> strategicRegion;
    int id = -1;
    vector<int> provs;
    string name;
    strategicRegion.emplace_back(0,provs,"");

    //Go through files
    for (const auto& file : filesystem::directory_iterator(strategicRegionsPath)) {
        if (file.is_regular_file() && file.path().extension() == ".txt") {
            ifstream currentFile(file.path());
            string fileContent((istreambuf_iterator<char>(currentFile)), istreambuf_iterator<char>());
            regex whiteSpaceRegex("\\s+");
            fileContent = regex_replace(fileContent, whiteSpaceRegex, " ");

            regex idRegex("id\\s*=\\s*(\\d+)");
            smatch idMatch;
            if (regex_search(fileContent, idMatch, idRegex)) {
                id = stoi(idMatch[1]);
            }

            regex nameRegex("name\\s*=\\s*\"(.*?)\"");
            smatch nameMatch;
            if (regex_search(fileContent, nameMatch, nameRegex)) {
                name = nameMatch[1].str();
            }



            string provincesString = returnBetweenBrackets(fileContent, "provinces");
            stringstream iss(provincesString);
            int province;
            while ( iss >> province ){
                provincesArray[province].strategicRegion = id;
                provs.push_back(province); 
            }

            strategicRegion.emplace_back(id,provs,name);
            provs.clear();
        }
    }
    return strategicRegion;
}