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
        int red;
        int green;
        int blue;
        string type;
        bool coastal;
        string terrain;
        int continent;
        int state;
        int victoryPoints;

        provinceClass(int id, int red, int green, int blue, string type, bool coastal, string terrain, int continent, int state, int victoryPoints);
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

        stateClass(int id, vector<int>provinces, map<string, int>resources, bool impassable, int manpower, string stateCategory,map<string, string> dateInfo, string owner, vector<string> cores, vector<string> claims, vector<string> stateFlags);
};

vector<provinceClass> loadProvinces(const string& filename);
vector<stateClass> loadStates(const filesystem::path& historyStatesPath, vector<provinceClass>& provincesArray);

#endif // LOAD_MAP_HPP