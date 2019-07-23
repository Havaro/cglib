#include <list>
#include <string>
#include <iostream>
#include <fstream>
using namespace std;

// Read subsets from file
void read_subsets(list<string>& sub_list) {
    string path;
    path = "groups_research/results/inc_subsets_from_g03.txt";

    ifstream infile(path.c_str());
    string subset;
    while(infile >> subset) {
        sub_list.push_back(subset);
    }
    infile.close();
}

void export_games(list<string>& subsets) {
    string path;
    path = "groups_research/results/all_possible_g04.txt";

    ofstream outfile(path.c_str(), ofstream::out);
    string game;
    int progress = 1;

    // The 0-game
    outfile << "{|}\n";

    // All pairs of subsets
    int total_games = 109139809 + 1;
    for (list<string>::iterator left = subsets.begin(); left != subsets.end(); left++) {
        for (list<string>::iterator right = subsets.begin(); right != subsets.end(); right++) {
            progress++;
            outfile << "{" << *left << "|" << *right << "}\n";
            if(progress % 100000 == 0)
                cout << progress << "/" << total_games << " (" << ((double) progress) * 100 / total_games << "%)" << endl;
        }
    }
    outfile.close();
}

int main() {
    cout << "Starting" << endl;
    list<string> subsets;
    read_subsets(subsets);
    export_games(subsets);
    return 0;
}
