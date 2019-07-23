#include <iostream>
#include <string>
#include <vector>
#include "Game.h"
#include "GameOperators.h"
#include "GameNotations.h"
using namespace std;
using namespace cg;

void testNorton();
void testOperators();
void computeCombinations(vector<vector<Game>>& sets);
void G30();
void G20();

int main() {
    G30();
    return 0;
}

void createNonDominatedSubsets(vector<Game>& prevs) {
    
}

void G20() {
    vector<vector<Game>> sets;
    sets.push_back(vector<Game>{Game("0")});
    sets.push_back(vector<Game>{Game("*")});
    sets.push_back(vector<Game>{Game("0"), Game("*")});

    computeCombinations(sets);
}

void G30() {
    vector<vector<Game>> sets;
    sets.push_back(vector<Game>{Game("^")});
    sets.push_back(vector<Game>{Game("^*")});
    sets.push_back(vector<Game>{Game("^"), Game("^*")});
    sets.push_back(vector<Game>{Game("^"), Game("*")});
    sets.push_back(vector<Game>{Game("^*"), Game("0")});
    sets.push_back(vector<Game>{Game("0")});
    sets.push_back(vector<Game>{Game("{*,0|*,0}")}); //*2
    sets.push_back(vector<Game>{Game("*")});
    sets.push_back(vector<Game>{Game("v")});
    sets.push_back(vector<Game>{Game("v*")});
    sets.push_back(vector<Game>{Game("0"), Game("{*,0|*,0}")}); //0, *2
    sets.push_back(vector<Game>{Game("0"), Game("*")});
    sets.push_back(vector<Game>{Game("{*,0|*,0}"), Game("*")}); //*2, *
    sets.push_back(vector<Game>{Game("0"), Game("*"), Game("{*,0|*,0}")}); //0, *, *2
    sets.push_back(vector<Game>{Game("0"), Game("v*")});
    sets.push_back(vector<Game>{Game("*"), Game("v")});
    sets.push_back(vector<Game>{Game("v"), Game("v*")});

    computeCombinations(sets);
}

void computeCombinations(vector<vector<Game>>& sets) {

    vector<Game> canons;
    vector<Game> uniq;

    // All sets as Left and Right options
    for(vector<Game> ls: sets) {
        for(vector<Game> rs: sets) {
            Game g;
            // Add all options from the sets to the game
            for(Game lo: ls) {
                g.leftOptions.push_back(lo);
            }
            // Also for Right
            for(Game ro: rs) {
                g.rightOptions.push_back(ro);
            }
            canons.push_back(g.toCanonicalForm());
        }
    }
    cout << "Canons: " << canons.size() << endl;

    // Remove duplicates
    for(Game c: canons) {
        bool shouldAdd = true;
        for(Game u: uniq) {
            if(c == u) {
                // Already in u
                shouldAdd = false;
                break;
            }
        }
        if(shouldAdd)
            uniq.push_back(c);
    }

    // Print uniques
    for(Game u: uniq)
        cout << u << endl;
    cout << "Unique: " << uniq.size() << endl;

}

void testNorton() {
    Game r;
    for(int i = 0; i < 4; i++)
        r = r + Game("1");
    r.toCanonicalForm();
    Game s = Game("^");
    cout << "Game s=" << s << endl;
    cout << "Game r=" << r << endl;
    cout << "Norton r.s=" << norton(r, s).toCanonicalForm() << endl;

    auto incL = Game("1").getLeftIncentives();
    for(auto it = incL.begin(); it != incL.end(); ++it)
        cout << it->toCanonicalForm() << endl;
    cout << "---" << endl;
    auto incR = Game("1").getRightIncentives();
    for(auto it = incR.begin(); it != incR.end(); ++it)
        cout << it->toCanonicalForm() << endl;
    cout << "---" << endl;
    cout << (norton(Game("1"), Game("up"))).toCanonicalForm() << endl;
}

void testOperators() {
    Game g = Game("^");
    Game h = Game("v");
    cout << "G:\t" << g << endl;
    cout << "H:\t" << h << endl;
    cout << "-H:\t" << -h << endl;
    cout << "G+H:\t" << (g+h) << endl;

    cout << "H geq 0: " << geqZero(h) << endl;
    cout << "H leq 0: " << leqZero(h) << endl;
    cout << "H gin 0: " << ginZero(h) << endl;
    cout << "H lin 0: " << linZero(h) << endl;

    cout << "H > 0: " << gtrZero(h) << endl;
    cout << "H < 0: " << lssZero(h) << endl;
    cout << "H = 0: " << equalZero(h) << endl;
    cout << "H ~ 0: " << incomparableZero(h) << endl;

    cout << "G geq H: " << geq(g, h) << endl;
    cout << "G leq H: " << leq(g, h) << endl;
    cout << "G gin H: " << gin(g, h) << endl;
    cout << "G lin H: " << lin(g, h) << endl;

    cout << "G > H: " << gtr(g, h) << endl;
    cout << "G < H: " << lss(g, h) << endl;
    cout << "G = H: " << equal(g, h) << endl;
    cout << "G ~ H: " << incomparable(g, h) << endl;
}
