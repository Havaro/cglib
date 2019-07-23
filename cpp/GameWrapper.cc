#include "Game.h"

extern "C" {
    cg::Game* Game_new() {
        return new cg::Game("1");
    }

    void Game_delete(cg::Game* g) {
        delete g;
    }

    const char* Game_cgn(cg::Game* g) {
        return g->getCGN().c_str();
    }

}
