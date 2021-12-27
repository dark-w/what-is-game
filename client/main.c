#include <stdlib.h>
#include "inc/map.h"
#include "inc/man.h"
#include "inc/disp.h"
#include "inc/user.h"

int main(int argc,char *argv[])
{
    init_user(argc, argv[1]);
    init_map();
    init_man();
    system("clear");
    
    while (1) {
        disp_show();
        man_move();
        
        system("clear");
    }
}