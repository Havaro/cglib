#ifndef GAME_OPERATORS_H
#define GAME_OPERATORS_H

#include "Game.h"

namespace cg {

std::ostream& operator<<(std::ostream& os, const Game& g);
Game operator-(const Game& g);
Game operator+(const Game& g, const Game& h);
Game operator-(const Game& g, const Game& h);
Game operator*(const int n, const Game& g);
bool operator==(const Game& g, const Game& h);

Game inverse(const Game& g);
Game add(const Game& g, const Game& h);
Game subtract(const Game& g, const Game& h);
Game times(const int n, const Game& g);
Game norton(const Game& g, const Game& u);

bool geqZero(const Game& g);
bool leqZero(const Game& g);
bool ginZero(const Game& g);
bool linZero(const Game& g);

bool gtrZero(const Game& g);
bool lssZero(const Game& g);
bool equalZero(const Game& g);
bool incomparableZero(const Game& g);

bool geq(const Game& g, const Game& h);
bool leq(const Game& g, const Game& h);
bool gin(const Game& g, const Game& h);
bool lin(const Game& g, const Game& h);

bool gtr(const Game& g, const Game& h);
bool lss(const Game& g, const Game& h);
bool equal(const Game& g, const Game& h);
bool incomparable(const Game& g, const Game& h);

} // cg

#endif
