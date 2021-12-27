#include <stdio.h>
#include <stdlib.h>
#include "../inc/define.h"
#include "../inc/user.h"

void init_user(int32_t tmp_data, int8_t *tmp_char)
{
    if (tmp_data == 1) {
        printf("请在运行程序后面添加用户名\n");
        exit(1);
    }
    user_attributes.name = tmp_char;
}