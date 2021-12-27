#include "../inc/map.h"

void init_map()
{
    for (int i = 0; i < map_width; i++) {
        test_map[0][i] = 2;
    }
    for (int i = 0; i < map_length; i++) {
        test_map[i][0] = 3;
    }
}