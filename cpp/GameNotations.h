#include "Game.h"

namespace cg {

bool isValidCGN(const std::string cgn);
std::string expandCGN(const std::string cgn);
std::string compressCGN(const std::string cgn);

bool isValidPreorder(const std::string po);
std::string preorderFromName(const std::string name);

} // cg
