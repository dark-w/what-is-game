#include "../inc/map.h"
#include "../inc/man.h"
#include <stdlib.h>
#include <stdio.h>

int8_t man_x;
int8_t man_y;

void init_man()
{
    test_map[man_base_x][man_base_y] = 1;
    man_x = man_base_x;
    man_y = man_base_x;
}

static void man_claer()
{
    test_map[man_x][man_y] = 0;
}

static void man_disp()
{
    if (man_x > 9) man_x = 9;
    if (man_y > 9) man_y = 9;
    if (man_x < 0) man_x = 0;
    if (man_y < 0) man_y = 0;
    test_map[man_x][man_y] = 1;
}

static int32_t man_get_key()
{
    int32_t tmp_char;

    system("stty -echo");
    system("stty -icanon");
    tmp_char = getchar();
    system("stty icanon");
    system("stty echo");

    return tmp_char;
}

void man_move()
{
    man_claer();
    
    int32_t tmp_char = man_get_key();
    switch (tmp_char) {
    case 'w':
        man_x -= 1;
        break;
    case 's':
        man_x += 1;
        break;
    case 'a':
        man_y -= 1;
        break;
    case 'd':
        man_y += 1;
        break;
    default:
        break;
    }
    man_disp();
}