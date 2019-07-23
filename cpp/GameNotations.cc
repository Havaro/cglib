#include <string>
#include <iostream>
#include "GameNotations.h"

namespace cg {

// String replace function from https://stackoverflow.com/a/3418285
void replace_all(std::string& str, const std::string& from, const std::string& to) {
    if(from.empty())
        return;
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
}

std::string expandCGN(const std::string cgn) {
    std::string exp = cgn;

    // Words to characters
    replace_all(exp, "up", "^");
    replace_all(exp, "down", "v");
    replace_all(exp, "star", "*");
    replace_all(exp, "zero", "0");

    // Characters to games
    replace_all(exp, "-1", "{|0}");
    replace_all(exp, "1", "{0|}");
    replace_all(exp, "^*", "{0,*|0}");
    replace_all(exp, "v*", "{0|0,*}");
    replace_all(exp, "^", "{0|*}");
    replace_all(exp, "v", "{*|0}");
    replace_all(exp, "*", "{0|0}");
    replace_all(exp, "0", "{|}");
    return exp;
}

std::string compressCGN(std::string cgn) {
    std::string comp = cgn;
    replace_all(comp, "{|}", "0");
    replace_all(comp, "{0|}", "1");
    replace_all(comp, "{|0}", "-1");
    replace_all(comp, "{0|0}", "*");
    replace_all(comp, "{0|*}", "^");
    replace_all(comp, "{*|0}", "v");
    replace_all(comp, "{0,*|0}", "^*");
    replace_all(comp, "{0|0,*}", "v*");
    replace_all(comp, "{*,0|0}", "^*");
    replace_all(comp, "{0|*,0}", "v*");
    return comp;
}

bool isValidCGN(const std::string cgn) {
    int left = 0;
    int center = 0;
    int right = 0;

    for(const char& c : expandCGN(cgn))
        if(c == '{')
            left++;
        else if(c == '|')
            center++;
        else if(c == '}')
            right++;
        else if(c == ',')
            continue;
        else
            return false;
    return left == center && center == right;
}

bool isValidPreorder(const std::string po) {
    for(const char& c : po)
        if(c != 'P' && c != 'G' && c != 'M' && c != 'R' && c != 'L')
            return false;
    return true;
}

} // cg
