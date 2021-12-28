#include <stdlib.h>
#include "inc/map.h"
#include "inc/man.h"
#include "inc/disp.h"
#include "inc/user.h"
#include <curses.h>		//ncurses库
#include <pthread.h>	//线程库
#include <unistd.h>	

void initNcure()
{
    initscr();
    keypad(stdscr, 1);
    noecho();		//防止乱码出现
}

int main(int argc,char *argv[])
{
    pthread_t k1;
    pthread_t k2;

    initNcure();
    init_user(argc, argv[1]);
    init_map();
    init_man();
    disp_show();
    
    pthread_create(&k1, NULL, thread_show, NULL);
    pthread_create(&k2, NULL, man_move, NULL);
    while(1);
    getch();
    endwin();
    return 0;

    
}

