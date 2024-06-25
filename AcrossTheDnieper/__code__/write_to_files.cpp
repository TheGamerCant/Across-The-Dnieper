#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
#include <iomanip>
#include "load_map.hpp"
#include "func.hpp"
using namespace std;

void write_definition_csv(const filesystem::path& directory, vector<provinceClass>& provincesArray){
    filesystem::path outfile = directory / "definition.csv";
    ofstream file(outfile, ios::out | ios::binary);

    if (file.is_open()) {
        for (const auto& province : provincesArray) {
            string redStr = province.hexadecimal.substr(0,2);
            string greenStr = province.hexadecimal.substr(2,2);
            string blueStr = province.hexadecimal.substr(4,2);
            int redStr2 = hexToDenary(redStr);
            int greenStr2 = hexToDenary(greenStr);
            int blueStr2 = hexToDenary(blueStr);
        
            file << province.id << ";" <<
                    redStr2<< ";"
                    << greenStr2 << ";"
                    << blueStr2 << ";"
                    << province.type << ";"
                    << (province.coastal ? "true" : "false") << ";"
                    << province.terrain << ";"
                    << province.continent << "\r\n";        //Use "\r\n" instead of "\n" or endl tp make it have CRLF encoding
        }
        file.close();
    }
}

void write_scripted_effects_txt(const filesystem::path& directory, vector<provinceClass>& provincesArray, vector<stateClass>& statesArray){
    filesystem::path outfile = directory / "state_and_province_names_scripted_effects.txt";
    ofstream file(outfile, ios::out | ios::binary);

    if (file.is_open()) {
        for (const auto& state : statesArray) {
            if(state.id != 0){
                file << "update_state_" << state.id << "_names={";
                auto it = state.names.find("DEFAULT");
                if (it != state.names.end()){ file << "\t\t#" << it->second << "\n"; }
                auto stateNamesCopy = state.names;
                stateNamesCopy.erase("DEFAULT");
                if (!stateNamesCopy.empty()){
                    int i = 0;
                    file << "\t" << state.id << "={\n\t\t";
                    for (const auto& [key, value] : stateNamesCopy){
                        if (i!=0){ file << "\t\telse_";}
                        file << "if={\n\t\t\tlimit = { CONTROLLER = { " << key << " = yes } }\n\t\t\tset_state_name = STATE_"
                            << state.id << "_" << key << "\n\t\t}\n";
                        i+=1;
                    }
                    file << "\t\telse={\n\t\t\treset_state_name = yes\n\t\t}\n\t}";
                }

                for (const auto& province : state.provinces) {
                    auto currentProv = provincesArray[province];
                    if(currentProv.names.size() > 1){
                        string provDefaultName;
                        auto it = currentProv.names.find("DEFAULT");
                        if (it != currentProv.names.end()){ provDefaultName = it->second; }
                        auto provinceNamesCopy = state.names;
                        provinceNamesCopy.erase("DEFAULT");
                        if (!provinceNamesCopy.empty()){
                            int i = 0;
                            for (const auto& [key, value] : provinceNamesCopy){
                                file << "\n\t"; if (i!=0){ file << "else_";}
                                file << "if={\n\t\tlimit={ any_country={ controls_province = " << currentProv.id << " " << key << " = yes } }\t\t#" 
                                     << value << "\n\t\tset_province_name = { id = " << currentProv.id << " name = VICTORY_POINTS_" 
                                     << currentProv.id  << "_" << key << " }\n\t}";
                                i+=1;
                            }
                            file << "\n\telse={\t\t#"<< provDefaultName <<"\n\t\treset_province_name = " << currentProv.id << "\n\t}";
                        }
                    }
                }
                file << "\n}\n";
            }
        }
        file << "\n\nchange_city_names={";
        for (const auto& state : statesArray) {
            if(state.id!=0) {file << "\n\tupdate_state_" << state.id << "_names=yes";}
        }
        file << "\n}\n\nrevert_city_names_to_original={\n\tevery_state = { reset_state_name=yes }";
        for (const auto& state : statesArray) {
            auto it = state.names.find("IS_2016_DECOM");
            if (it != state.names.end()){
                file << "\n\t" << state.id << "={\n\t\tif={\n\t\t\tlimit={ IS_2016_DECOM = yes }\n\t\t\tset_state_name = STATE_"
                << state.id << "_IS_2016_DECOM\n\t\t}\n\t\telse={ reset_state_name = yes }\n\t}"; 
            }
        }
        for (const auto& prov : provincesArray) {
            if(prov.victoryPoints > 0){
                auto it = prov.names.find("IS_2016_DECOM");
                if (it != prov.names.end()){
                    file << "\n\tif={\n\t\tlimit = { IS_2016_DECOM = yes }\n\t\tset_province_name = { id = " << prov.id
                    << " name = VICTORY_POINTS_" << prov.id << "_IS_2016_DECOM }\n\t}\n\telse={\n\t\tset_province_name = { id = "
                    << prov.id << " name = VICTORY_POINTS_" << prov.id << " }\n\t}";
                }else{
                    file << "\n\tset_province_name = { id = " << prov.id << " name = VICTORY_POINTS_" << prov.id << " }";
                }
            }
        }
        file << "\n}" << "\r\n";
        file.close();
    }
}

void write_state_names(const filesystem::path& directory, vector<stateClass>& statesArray){
    filesystem::path outfile = directory / "state_names_l_english.yml";
    ofstream file(outfile, ios::out | ios::binary);

    if (file.is_open()) {
        unsigned char bom[] = {0xEF, 0xBB, 0xBF};
        file.write(reinterpret_cast<char*>(bom), sizeof(bom));
        file << "l_english: "; 
        for (const auto& state : statesArray) {
            if (state.id != 0){
                auto stateNames = state.names;
                for (const auto& [key, value] : stateNames){
                    if (key == "DEFAULT"){ 
                        file << "\n STATE_" << state.id << ":0 \"" << value <<"\"";
                    }else{
                        file << "\n STATE_" << state.id << "_" << key << ":0 \"" << value <<"\"";
                    }
                }
            }
        }
        file << "\r\n"; file.close();
    }
}

void write_victory_point_names(const filesystem::path& directory, vector<provinceClass>& provincesArray){
    filesystem::path outfile = directory / "victory_points_l_english.yml";
    ofstream file(outfile, ios::out | ios::binary);

    if (file.is_open()) {
        unsigned char bom[] = {0xEF, 0xBB, 0xBF};
        file.write(reinterpret_cast<char*>(bom), sizeof(bom));
        file << "l_english: "; 
        for (const auto& province : provincesArray) {
            if (province.victoryPoints > 0){
                auto provinceNames = province.names;
                for (const auto& [key, value] : provinceNames){
                    if (key == "DEFAULT"){ 
                        file << "\n VICTORY_POINTS_" << province.id << ":0 \"" << value <<"\"";
                    }else{
                        file << "\n VICTORY_POINTS_" << province.id << "_" << key << ":0 \"" << value <<"\"";
                    }
                }
            }
        }
        file << "\r\n"; file.close();
    }
}

void write_strategic_region_names(const filesystem::path& directory, vector<strategicRegionClass>& strategicRegionsArray){
    filesystem::path outfile = directory / "strategic_region_names_l_english.yml";
    ofstream file(outfile, ios::out | ios::binary);

    if (file.is_open()) {
        unsigned char bom[] = {0xEF, 0xBB, 0xBF};
        file.write(reinterpret_cast<char*>(bom), sizeof(bom));
        file << "l_english: "; 
        for (const auto& strategicRegion : strategicRegionsArray) {
            if (strategicRegion.id > 0){
                file << "\n " << strategicRegion.name << ":0 \t" << strategicRegion.name << "\"";
            }
        }
        file << "\r\n"; file.close();
    }
}

void write_state_files(const filesystem::path& directory, vector<provinceClass>& provincesArray, vector<stateClass>& statesArray){
    for (const auto& state : statesArray) {
        if(state.id!=0){
            filesystem::path outfile = directory / (to_string(state.id)+"-State_"+to_string(state.id)+".txt");
            ofstream file(outfile, ios::out | ios::binary);

            if (file.is_open()) {
                file << "state={\n\tid=" << state.id << "\n\tname=\"STATE_" << state.id << "\"\n";
                auto resourcesCopy = state.resources;
                if(!resourcesCopy.empty()){
                    file << "\tresources={\n";
                    for (const auto& [key, value] : resourcesCopy){
                        file << "\t\t" << key << " = " << value << "\n";
                    }
                    file << "\t}\n";
                }
                file << "\thistory={\n";

                auto ownerCopy = state.owner;
                if(!ownerCopy.empty()){file << "\t\towner = " << ownerCopy << "\n";}

                auto coresCopy = state.cores;
                if(!coresCopy.empty()){
                    for (const auto& core : coresCopy) {
                        file << "\t\tadd_core_of = " << core << "\n";
                    }
                }

                auto claimsCopy = state.claims;
                if(!claimsCopy.empty()){
                    for (const auto& claim : claimsCopy) {
                        file << "\t\tadd_claim_by = " << claim << "\n";
                    }
                }

                auto flagsCopy = state.stateFlags;
                if(!flagsCopy.empty()){
                    for (const auto& flag : flagsCopy) {
                        file << "\t\tset_state_flag = " << flag << "\n";
                    }
                }

                auto provsCopy = state.provinces;
                for (const auto& prov : provsCopy) {
                    auto currentProv = provincesArray[prov];
                    if (currentProv.victoryPoints!=0){
                        auto it = currentProv.names.find("DEFAULT");
                        string provName;
                        if (it != currentProv.names.end()){ provName = it->second; }

                        file << "\t\tvictory_points={ " << currentProv.id << " " << currentProv.victoryPoints << " }\t\t#" << provName << "\n";
                    }
                } 

                file << "\t\tbuildings={\n";
                auto buildingsCopy = state.buildings; 
                if(!buildingsCopy.empty()){
                    

                    for (const auto& prov : provsCopy) {
                        auto currentProv = provincesArray[prov];
                        auto provBuildingsCopy = currentProv.buildings;
                        if(!provBuildingsCopy.empty()){
                            file << "\t\t\t" << currentProv.id << " = { ";
                            for (const auto& [key, value] : provBuildingsCopy){
                                file << key << " = " << value << " ";
                            }
                            file << " }\n";
                        }
                    }

                    for (const auto& [key, value] : buildingsCopy){
                        file << "\t\t\t" << key << " = " << value << "\n";
                    }
                }
                file << "\t\t}\n";

                auto dateInfoCopy = state.dateInfo;
                if(!dateInfoCopy.empty()){
                    for (const auto& [key, value] : dateInfoCopy){
                        file << "\t\t" << key << "={" << value << "}\n";
                    }
                }

                file << "\t}\n\tprovinces={\n\t\t";
                for (const auto& prov : provsCopy) {
                    file << prov << " ";
                } 
                file << "\n\t}\n\tmanpower=" << state.manpower << "\n\tbuildings_max_level_factor=1.000\n\tlocal_supplies = 0.5\t\t#One unit of local_supplies is equal to 0.2 units of supply. If undefined, assumed to be 0."
                    <<"\n\tstate_category=" << state.stateCategory<< "\n";
                if (state.impassable == true){file << "\timpassable=yes\n";}

                file << "}"; file.close();
            }
        }
    }
}


void write_strategic_region_files(const filesystem::path& directory, vector<strategicRegionClass>& strategicRegionsArray){
    for (const auto& strategic_region : strategicRegionsArray) {
        if(strategic_region.id!=0){
            filesystem::path outfile = directory / (to_string(strategic_region.id)+"-"+strategic_region.name+".txt");
            ofstream file(outfile, ios::out | ios::binary);

            if (file.is_open()) {
                file << "strategic_region={\n\tid=" << strategic_region.id << "\n\tname=\"" << strategic_region.name << "\"\n\tprovinces={\n\t\t";
                auto provsCopy = strategic_region.provinces;
                for (const auto& prov : provsCopy) {
                    file << prov << " ";
                } 
                file << "\n\t}\n\tweather={\n\t}\n}"; file.close();
            }
        }
    }
}