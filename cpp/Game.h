#ifndef GAME_H
#define GAME_H

#include <list>
#include <string>

namespace cg {

class Game {
private:
    void clear();
    char getPreorderLetter() const;
    void setPreorder(const std::string& preorder, int& index);
    void setCGN(const std::string& notation, int& index);
    void getCGN(std::string& prev) const;
    void getPreorder(std::string& prev) const;
    int getDot(std::string& dot, int& index, const char notation) const;

public:
    std::list<Game> leftOptions;
    std::list<Game> rightOptions;

    Game();
    Game(const std::string str);
    ~Game();
    Game copy() const;

    Game& fromCGN(const std::string cgn);
    Game& fromPreorder(const std::string po);

    //std::list<Game> const& getLeftOptions() const;
    //std::list<Game> const& getRightOptions() const;

    std::string getPreorder() const;
    std::string getCGN() const;
    std::string getDotPreorder() const;
    std::string getDotCGN() const;
    std::string getDot() const;
    int removeDominated();
    int replaceReversible();
    Game& toCanonicalForm();
    std::list<Game> getLeftIncentives() const;
    std::list<Game> getRightIncentives() const;
    bool isInteger() const;

};

} // cg

#endif
