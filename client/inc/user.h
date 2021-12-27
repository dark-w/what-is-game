#ifndef __USER_H_
#define __USER_H_

#include "../inc/define.h"

struct user
{
    char *name;
};

void init_user(int32_t tmp_data, int8_t *tmp_char);

struct user user_attributes;
#endif