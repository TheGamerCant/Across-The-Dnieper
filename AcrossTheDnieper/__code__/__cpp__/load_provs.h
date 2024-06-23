#ifndef LOAD_PROVS_H
#define LOAD_PROVS_H

#include <string>
#include <vector>
#include <filesystem>

class Province {
public:
    int id;
    int red;
    int green;
    int blue;
    std::string type;
    bool coastal;
    std::string terrain;
    int continent;

    Province(int id, int red, int green, int blue, const std::string& type, bool coastal, const std::string& terrain, int continent);
};

std::vector<Province> loadProvinces(const std::string& filename);

#endif // LOAD_PROVS_H