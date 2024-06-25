#ifndef LOAD_MAP_HPP
#define LOAD_MAP_HPP

#include <string>
#include <vector>
#include <filesystem>
#include <map>
using namespace std;

class provinceClass {
    public:
        int id;
        string hexadecimal;
        string type;
        bool coastal;
        string terrain;
        int continent;
        int state;
        int victoryPoints;
        map<string, int> buildings;
        int strategicRegion;
        map<string, string> names;
        map<int, int> coordinates;

        provinceClass(int id, string hexadecimal, string type, bool coastal, string terrain, int continent, int state, 
        int victoryPoints, map<string, int>buildings, int strategicRegion, map<string, string> names, map<int, int> coordinates);
};
class stateClass {
    public:
        int id;
        vector <int> provinces;
        map<string, int> resources;
        bool impassable;
        int manpower;
        string stateCategory;
        map<string, string> dateInfo;
        string owner;
        vector<string> cores;
        vector<string> claims;
        vector<string> stateFlags;
        map<string, int> buildings;
        map<string, string> names;

        stateClass(int id, vector<int>provinces, map<string, int>resources, bool impassable, int manpower, string stateCategory, 
        map<string, string> dateInfo, string owner, vector<string> cores, vector<string> claims, vector<string> stateFlags, map<string, int> buildings, map<string, string> names);
};
class strategicRegionClass {
    public:
        int id;
        vector <int> provinces;
        string name;

       strategicRegionClass(int id, vector<int>provinces, string name);
};

vector<provinceClass> loadProvinces(const string& filename);
vector<stateClass> loadStates(const filesystem::path& historyStatesPath, vector<provinceClass>& provincesArray);
vector<strategicRegionClass> loadStrategicRegions(const filesystem::path& strategicRegionsPath, vector<provinceClass>& provincesArray);

#endif // LOAD_MAP_HPP