#include <iostream>
#include <string>
#include <regex>
#include "Game.h"
#include "GameOperators.h"
#include "GameNotations.h"

namespace cg {

Game::Game() {}

Game::Game(const std::string str) {     // TODO: Detect game by name (or do we do this in 'fromCGN'?)
    if(isValidCGN(str))
        fromCGN(str);
    else if(isValidPreorder(str))
        fromPreorder(str);
    else
        std::cerr << "Unknown game format." << std::endl;
}

Game::~Game() {
    clear();
}

void Game::clear() {
    leftOptions.clear();
    rightOptions.clear();
}

Game& Game::fromCGN(const std::string cgn) {
    int idx = 1;
    std::string expanded = expandCGN(cgn);
    clear();
    if(!isValidCGN(cgn)) {
        std::cerr << "Invalid notation." << std::endl;
        return *this;
    }
    setCGN(expanded, idx);
    return *this;
}

void Game::setCGN(const std::string& notation, int& index) {
    char letter = notation[index];
    bool currentlyLeft = true;
    while(letter != '}') {
        if(letter == '{') {
            // New game appears
            Game opt;
            opt.setCGN(notation, ++index);
            if(currentlyLeft)
                leftOptions.push_back(opt);
            else
                rightOptions.push_back(opt);
        }
        else if(letter == '|')
            currentlyLeft = false;
        
        // In the other cases (',' or '}'), do nothing
        // Go to the next letter
        letter = notation[++index];
    }
}

std::string Game::getCGN() const {
    std::string notation;
    getCGN(notation);
    return compressCGN(notation);
}

void Game::getCGN(std::string& prev) const {
    prev.push_back('{');

    // Add all Left options followed by a comma
    for(auto it = leftOptions.begin(); it != leftOptions.end(); ++it) {
        it->getCGN(prev);
        prev.push_back(',');
    }
    // Remove the last comma if there were any options
    if(!leftOptions.empty())
        prev.pop_back();

    prev.push_back('|');

    // Add all Right options followed by a comma
    for(auto it = rightOptions.begin(); it != rightOptions.end(); ++it) {
        it->getCGN(prev);
        prev.push_back(',');
    }

    // Remove the last comma if there were any options
    if(!rightOptions.empty())
        prev.pop_back();
    
    prev.push_back('}');
}

Game& Game::fromPreorder(const std::string po) {
    int idx = 0;
    clear();
    if(!isValidPreorder(po)) {
        std::cerr << "Invalid notation." << std::endl;
        return *this;
    }
    setPreorder(po, idx);
    return *this;
}

void Game::setPreorder(const std::string& preorder, int& index) {
    char letter = preorder[index];
    if(letter == 'G' || letter == 'L') {
        //Count the number of M's
        int m = 0;
        while(preorder[index+m+1] == 'M')
            m++;

        //Add the next m+1 options
        index += m;
        for(int i = 0; i <= m; i++) {
            Game option;
            option.setPreorder(preorder, ++index);
            leftOptions.push_back(option);
        }
    }
    if(letter == 'G' || letter == 'R') {
        //Count the number of M's
        int m = 0;
        while(preorder[index+m+1] == 'M')
            m++;
        
        //Add the next m+1 options
        index += m;
        for(int i = 0; i <= m; i++) {
            Game option;
            option.setPreorder(preorder, ++index);
            rightOptions.push_back(option);
        }
    }
}

char Game::getPreorderLetter() const {
    if(leftOptions.empty() && rightOptions.empty())
        return 'P';
    else if(leftOptions.empty())
        return 'R';
    else if(rightOptions.empty())
        return 'L';
    return 'G';
}

std::string Game::getPreorder() const {
    std::string preorder;
    getPreorder(preorder);
    return preorder;
}

void Game::getPreorder(std::string& prev) const {
    //Add the character of this game
    prev.push_back(getPreorderLetter());
    
    //Add as many 'M's as there are Left options
    for(auto it = leftOptions.begin(); it != leftOptions.end(); ++it)
        prev.push_back('M');
    
    if(!leftOptions.empty()) {
        //Remove the last 'M'
        prev.pop_back();
        //Output the left options
        for(auto it = leftOptions.begin(); it != leftOptions.end(); ++it)
            it->getPreorder(prev);
    }

    //Add as many 'M's as there are Right options
    for(auto it = rightOptions.begin(); it != rightOptions.end(); ++it)
        prev.push_back('M');

    if(!rightOptions.empty()) {
        //Remove the last 'M'
        prev.pop_back();
        //Output the right options
        for(auto it = rightOptions.begin(); it != rightOptions.end(); ++it)
            it->getPreorder(prev);
    }
}

std::string Game::getDotPreorder() const {
    int i = 0;
    std::string dotstr = std::string("digraph Game {\n");
    getDot(dotstr, i, 'p');
    return dotstr + "}";
}

int Game::getDot(std::string& dot, int& index, const char notation) const {
    int myNodeIndex = index;
    std::string label;

    // Create node and set label
    if(notation == 'c')
        label = getCGN();
    else if(notation == 'p')
        label = getPreorderLetter();
    else
        std::cerr << "Invalid notation" << std::endl;

    dot += std::to_string(myNodeIndex) + "[label=\"" + label + "\"];\n";

    //Append Left games
    for(auto it = leftOptions.begin(); it != leftOptions.end(); ++it)
        dot += std::to_string(myNodeIndex) + " -> " + std::to_string(it->getDot(dot, ++index, notation)) + "[label=\"L\"];\n";

    //Append Right games
    for(auto it = rightOptions.begin(); it != rightOptions.end(); ++it)
        dot += std::to_string(myNodeIndex) + " -> " + std::to_string(it->getDot(dot, ++index, notation)) + "[label=\"R\"];\n";
    
    return myNodeIndex;
}

std::string Game::getDotCGN() const {
    int i = 0;
    std::string dotstr = std::string("digraph Game {\n");
    getDot(dotstr, i, 'c');
    return dotstr + "}";
}

std::string Game::getDot() const {
    return getDotCGN();
}

//Creates a copy of the current game using a tree traversal
Game Game::copy() const {
    Game h;     //New game that will be the copy

    //Copy all Left options
    for(auto it = leftOptions.begin(); it != leftOptions.end(); ++it)
        h.leftOptions.push_back(it->copy());
    
    //Copy all Right options
    for(auto it = rightOptions.begin(); it != rightOptions.end(); ++it)
        h.rightOptions.push_back(it->copy());
    
    //Return the copy
    return h;
}

//Remove all dominated options and return a count of how many this were
int Game::removeDominated() {
    int removed = 0;    //Counter
    
    //Remove dominated Left options
    //If iterA >= iterB -> iterA dominates iterB, remove iterB
    for(auto iterA = leftOptions.begin(); iterA != leftOptions.end(); ++iterA)
        for(auto iterB = leftOptions.begin(); iterB != leftOptions.end(); ++iterB)
            if(iterA != iterB && geq(*iterA, *iterB)) {
                iterB = leftOptions.erase(iterB);
                removed++;
            }
    
    //Remove dominated Right options
    //If iterA <= iterB -> iterA dominates iterB, remove iterB
    for(auto iterA = rightOptions.begin(); iterA != rightOptions.end(); ++iterA)
        for(auto iterB = rightOptions.begin(); iterB != rightOptions.end(); ++iterB)
            if(iterA != iterB && leq(*iterA, *iterB)) {
                iterB = rightOptions.erase(iterB);
                removed++;
            }
    
    return removed;
}

//Replace all reversible options and return a count of how many this were
int Game::replaceReversible() {
    int replaced = 0;   //Counter

    //Replace reversible Left options
    //Loop all Left options of G
    for(auto iterL = leftOptions.begin(); iterL != leftOptions.end(); ++iterL)
        //Loop all Right options of iterL
        for(auto iterLR = iterL->rightOptions.begin(); iterLR != iterL->rightOptions.end(); ++iterLR)
            //Check whether iterLR <= G
            if(leq(*iterLR, *this)) {
                //iterL is reversible trough iterLR, replace it with iterLR's Left options
                leftOptions.splice(iterL, iterLR->leftOptions);
                iterL = leftOptions.erase(iterL);
                replaced++;
                break;      //End the iterLR iterator, since its list was spliced
            }
    
    //Replace reversible Right options
    //Loop all Right options of G
    for(auto iterR = rightOptions.begin(); iterR != rightOptions.end(); ++iterR)
        //Loop all Left options of iterR
        for(auto iterRL = iterR->leftOptions.begin(); iterRL != iterR->leftOptions.end(); ++iterRL)
            //Check whether iterRL >= G
            if(geq(*iterRL, *this)) {
                //iterR is reversible trough iterRL, replace it with iterRL's Right options
                rightOptions.splice(iterR, iterRL->rightOptions);
                iterR = rightOptions.erase(iterR);
                replaced++;
                break;      //End the iterRL iterator, since its list was spliced
            }
    
    return replaced;
}

//Transforms the game into canonical form
//Traverses the gametree in postorder and replaces reversible and removes dominated options
Game& Game::toCanonicalForm() {
    for(auto iterL = leftOptions.begin(); iterL != leftOptions.end(); ++iterL)
        iterL->toCanonicalForm();
    for(auto iterR = rightOptions.begin(); iterR != rightOptions.end(); ++iterR)
        iterR->toCanonicalForm();

    // TODO: According to http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.107.6036&rep=rep1&type=pdf
    // On page 112, it is claimed that we can first iteratively bypass reversible and then remove dominated
    // "The steps need not be repeated, since eliminating dominated options can never introduce new reversible moves."
    while(replaceReversible() || removeDominated());
    return *this;
}

std::list<Game> Game::getLeftIncentives() const {
    std::list<Game> incentives;
    for(auto iterL = leftOptions.begin(); iterL != leftOptions.end(); ++iterL)
        incentives.push_back(*iterL - *this);
    return incentives;
}

std::list<Game> Game::getRightIncentives() const {
    std::list<Game> incentives;
    for(auto iterR = rightOptions.begin(); iterR != rightOptions.end(); ++iterR)
        incentives.push_back(*this - *iterR);
    return incentives;
}

// A game G is not an integer when it has both a Left and Right incentive >-1
// From Siegel, page 80, Theorem 3.27
bool Game::isInteger() const {
    std::list<Game> li = getLeftIncentives();
    std::list<Game> ri = getRightIncentives();

    Game minOne = Game("-1");

    bool hasLeftGtrMinOne = false;
    bool hasRightGtrMinOne = false;

    // No left incentives >-1 -> is integer
    for(auto iterLi = li.begin(); iterLi != li.end(); ++iterLi)
        if(gtr(*iterLi, minOne)) {
            hasLeftGtrMinOne = true;
            break;
        }

    if(!hasLeftGtrMinOne)
        return true;

    // No right incentives >-1 -> is integer
    for(auto iterRi = ri.begin(); iterRi != ri.end(); ++iterRi)
        if(gtr(*iterRi, minOne)) {
            hasRightGtrMinOne = true;
            break;
        }

    if(!hasRightGtrMinOne)
        return true;
    
    // There are left and right incentives >-1, so this is not an integer
    return false;
    
}

} // cg
