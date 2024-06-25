#include <string>
#include <iostream>
using namespace std;

string returnBetweenBrackets(string fullStr, string str){
    int startBracketPos = fullStr.find(str);
    fullStr.erase(fullStr.begin(), fullStr.begin()+startBracketPos);
    startBracketPos = fullStr.find("{");
    fullStr.erase(fullStr.begin(), fullStr.begin()+startBracketPos+1);

    int i = 0;
    int bracketBalance = 1;
    while(bracketBalance!=0){
        if (fullStr[i] == '{') { bracketBalance+=1; }
        else if (fullStr[i] == '}') { bracketBalance-=1; }
        i+=1;
    }

    fullStr.erase(i-1);
    return fullStr;
}

int hexToDenary(string str){
    int number = stoull(str, nullptr, 16);
    return number;
}