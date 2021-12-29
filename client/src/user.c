#include <stdio.h>
#include <stdlib.h>
#include <curses.h>	
#include "../inc/define.h"
#include "../inc/user.h"

void init_user(int32_t tmp_data, int8_t *tmp_char)
{
    if (tmp_data == 1) {
        printw("Please add the user name at the end of the running program.\n");
        printw("For example: ./demo aa.\n");
        getch();
        endwin();
        exit(0);
    }
    user_attributes.name = tmp_char;
}