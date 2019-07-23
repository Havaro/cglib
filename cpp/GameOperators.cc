#include "GameOperators.h"
#include <iostream>     //TODO: Remove

namespace cg {

std::ostream& operator<<(std::ostream& out, const Game& g) {
    out << g.getCGN();
    return out;
}

//Swaps recursively the options for Left and Right
Game inverse(const Game& g) {
    Game inv = g.copy();
    std::swap(inv.leftOptions, inv.rightOptions);
    for(auto it = inv.leftOptions.begin(); it != inv.leftOptions.end(); ++it)
        *it = inverse(*it);
    for(auto it = inv.rightOptions.begin(); it != inv.rightOptions.end(); ++it)
        *it = inverse(*it);
    return inv;
}

Game operator-(const Game& g) {
    return inverse(g);
}

//Sum two games
Game add(const Game& g, const Game& h) {
    Game s;
    for(auto it = g.leftOptions.begin(); it != g.leftOptions.end(); ++it)
        s.leftOptions.push_back(add(*it, h));    
    for(auto it = h.leftOptions.begin(); it != h.leftOptions.end(); ++it)
        s.leftOptions.push_back(add(g, *it));
    for(auto it = g.rightOptions.begin(); it != g.rightOptions.end(); ++it)
        s.rightOptions.push_back(add(*it, h));    
    for(auto it = h.rightOptions.begin(); it != h.rightOptions.end(); ++it)
        s.rightOptions.push_back(add(g, *it));
    return s;
}

Game operator+(const Game& g, const Game& h) {
    return add(g, h);
}

//Subtract two games
Game subtract(const Game& g, const Game& h) {
    return add(g, inverse(h));
}

Game operator-(const Game& g, const Game& h) {
    return subtract(g, h);
}

Game times(const int n, const Game& g) {
    Game t;
    for(int i = 0; i < n; i++)
        t = t + g;
    return t;
}

Game operator*(const int n, const Game& g) {
    return times(n, g);
}

//TODO: Test
Game norton(const Game& g, const Game& u) {
    Game n;

    // Assert u > 0
    if(!gtrZero(u)) {
        std::cerr << "U must be greater than 0 to in Norton product." << std::endl;
        return n;
    }

    // Special case if G is an integer -> return G copies of u
    if(g.isInteger()) {
        std::cout << "G is an integer..." << std::endl;
        Game minOne = Game("-1");
        Game counter = g.copy();
        while(gtrZero(counter)) {
            std::cout << "Counter is " << counter << std::endl;
            n = n + u;
            counter = (counter + minOne).toCanonicalForm();
        }
        return n;
    }

    // Get all incentives of U
    std::list<Game> uIncentives = u.getLeftIncentives();
    uIncentives.splice(uIncentives.end(), u.getRightIncentives());
    std::cout << "Computing norton product of " << g << " and " << u << std::endl;
    // Loop incentives
    for(auto iterInc = uIncentives.begin(); iterInc != uIncentives.end(); ++iterInc) {
        std::cout << "Incentive " << iterInc->toCanonicalForm() << std::endl;
        // Loop Left options of G
        // Left options for N are {G^L*U+U+Incentives}
        for(auto iterL = g.leftOptions.begin(); iterL != g.leftOptions.end(); ++iterL) {
            auto temp = norton(*iterL, u) + u + *iterInc;
            std::cout << "Computed L " << *iterL << "*" << u << "+" << u << "+" << *iterInc << "=" << temp << std::endl;
            n.leftOptions.push_back(temp);
        }

        // Loop Right options of G
        // Right options for N are {G^R*U-U-Incentives}
        for(auto iterR = g.rightOptions.begin(); iterR != g.rightOptions.end(); ++iterR) {
            auto temp = norton(*iterR, u) - u - *iterInc;
            std::cout << "Computed R " << *iterR << "*" << u << "-" << u << "-" << *iterInc << "=" << temp << std::endl;
            n.rightOptions.push_back(temp);
        }
    }
    std::cout << "Product is " << n << std::endl;
    return n;
}

//Greater than or equal to zero (right starts -> loses)
//None of Right's options can be leqZero
bool geqZero(const Game& g) {
    for(auto it = g.rightOptions.begin(); it != g.rightOptions.end(); ++it)
        if(leqZero(*it))
            return false;
    return true;
}

//Less than or equal to zero (left starts -> loses)
//None of Left's options can be geqZero
bool leqZero(const Game& g) {
    for(auto it = g.leftOptions.begin(); it != g.leftOptions.end(); ++it)
        if(geqZero(*it))
            return false;
    return true;
}

//Greater than or incomparable to zero (left starts -> wins)
//There must be a Left option geqZero
bool ginZero(const Game& g) {
    for(auto it = g.leftOptions.begin(); it != g.leftOptions.end(); ++it)
        if(geqZero(*it))
            return true;
    return false;
}

//Less than or incomparable to zero (right starts -> wins)
//There must be a Right option leqZero
bool linZero(const Game& g) {
    for(auto it = g.rightOptions.begin(); it != g.rightOptions.end(); ++it)
        if(leqZero(*it))
            return true;
    return false;
}

//Greater than zero (Left player win)
bool gtrZero(const Game& g) {
    return geqZero(g) && ginZero(g);
}

//Less than zero (Right player win)
bool lssZero(const Game& g) {
    return leqZero(g) && linZero(g);
}

//Equal to zero (second player win)
bool equalZero(const Game& g) {
    return geqZero(g) && leqZero(g);
}

//Incomparable to zero (first player win)
bool incomparableZero(const Game& g) {
    return ginZero(g) && linZero(g);
}

//Check whether G>=H, true when G-H>=0
bool geq(const Game& g, const Game& h) {
    return geqZero(g - h);
}

//Check whether G<=H, true when G-H<=0
bool leq(const Game& g, const Game& h) {
    return leqZero(g - h);
}

//Check whether G>~H, true when G-H>~0
bool gin(const Game& g, const Game& h) {
    return ginZero(g - h);
}

//Check whether G<~H, true when G-H<~0
bool lin(const Game& g, const Game& h) {
    return linZero(g - h);
}

//Check whether G>H, true when G-H>0
bool gtr(const Game& g, const Game& h) {
    return gtrZero(g - h);
}

//Check whether G<H, true when G-H<0
bool lss(const Game& g, const Game& h) {
    return lssZero(g - h);
}

//Check whether G=H, true when G-H=0
bool equal(const Game& g, const Game& h) {
    return equalZero(g - h);
}

bool operator==(const Game& g, const Game& h) {
    return equal(g, h);
}

//Check whether G~H, true when G-H~0
bool incomparable(const Game& g, const Game& h) {
    return incomparableZero(g - h);
}

} // cg
