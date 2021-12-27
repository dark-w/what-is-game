#include <stdio.h>
#include "../inc/define.h"
#include "../inc/map.h"
#include "../inc/user.h"
#include <curses.h>
#include <unistd.h>

void disp_base(const uint8_t tmp_date)
{
    switch (tmp_date) {
    case 0:
        printw("  ");
        break;
    case 1:
        printw("%s", user_attributes.name);
        break;
    case 2:
        printw("==");
        break;
    case 3:
        printw("||");
        break;    
    default:
        break;
    }
}

void disp_line()
{
    printw("\n");
}

void disp_show()
{
    move(0,0);
    for (uint8_t i = 0; i < map_length; i++) {
        for (uint8_t j = 0; j < map_width; j++) {
            disp_base(test_map[i][j]);
        }
        disp_line();
    }
   
}

void *thread_show()
{
    while (1) {
        disp_show();
        refresh();		
        usleep(100000);
    }

}