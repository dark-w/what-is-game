#include "../inc/map.h"

void init_map()
{
    for (int i = 0; i < map_width; i++) {
        test_map[0][i] = 2;
    }
    for (int i = 0; i < map_width; i++) {
        test_map[map_length - 1][i] = 2;
    }
    for (int i = 1; i < map_length; i++) {
        test_map[i][0] = 3;
    }
    for (int i = 1; i < map_length; i++) {
        test_map[i][map_width - 1] = 3;
    }
    for (int i = 10; i < map_length; i++) {
        test_map[i][map_width / 2] = 3;
    }
     for (int i = 1; i < 10; i++) {
        test_map[i][map_width / 4] = 3;
    }
}