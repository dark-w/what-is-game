#include <stdio.h>
#include "../inc/define.h"
#include "../inc/map.h"

void disp_base(const uint8_t tmp_date)
{
    switch (tmp_date) {
    case 0:
        printf("  ");
        break;
    case 1:
        printf("人");
        break;
    default:
        break;
    }
}

void disp_line()
{
    printf("\n");
}

void disp_show()
{
    for (uint8_t i = 0; i < map_length; i++) {
        for (uint8_t j = 0; j < map_width; j++) {
            disp_base(test_map[i][j]);
        }
        disp_line();
    }
}