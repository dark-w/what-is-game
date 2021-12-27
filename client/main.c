#include <stdlib.h>
#include "inc/map.h"
#include "inc/man.h"
#include "inc/disp.h"

int main()
{
    init_map();
    init_man();

    while (1) {
        disp_show();
        man_move();
        
        system("clear");
    }
}