#include <curses.h>		//ncurses库
#include <stdlib.h>	
#include <pthread.h>	//线程库
#include <unistd.h>	
 
#define UP     1
#define DOWN  -1
#define LEFT   2
#define RIGHT -2

typedef struct snakes{
        int row;		//行
        int col;		//列
        struct snakes* next;
}snake,*psnake;

psnake head=NULL;		//全局变量蛇头
psnake tail=NULL;		//全局变量蛇尾

int key;
int dir;
snake food;

/*定义食物位置*/
void initFood(){
        int x=rand()%20;	/*根据界面大小判断随机数对20求余可以让食物在所画的界面范围内*/
        int y=rand()%20;
        food.row=x;
        food.col=y;
}

void initNcure(){
        initscr();
        keypad(stdscr,1);
        noecho();		//防止乱码出现
}

/*确定坐标节点*/
int whetherSnakeNode(int i,int j){
        psnake p;
        p=head;
        while(p!=NULL){
                if(p->row==i && p->col==j){
                        return 1;
                }
                        p=p->next;
        }
                        return 0;
}

/*确定食物坐标节点*/
int whetherSnakeFood(int i,int j){
 
        if(food.row==i && food.col==j){
                return 1;
        }
                return 0;
}

/*定义游戏界面（范围边界）*/
void gameInterFace(){
        int row;		//定义行
        int col;		//定义列
        move(0,0);		//移动光标，用来刷新界面
        for(row=0;row<20;row++){
                if(row==0){
                        for(col=0;col<20;col++){
                                printw("--");
                        }
                                printw("\n");
                }
                if(row>=0 && row<=19){
                        for(col=0;col<=20;col++){
                                if(col==0 || col==20){
                                        printw("|");
                                }
                                else if(whetherSnakeNode(row,col)){	//扫描输出
                                        printw("[]");
                                }
                                else if(whetherSnakeFood(row,col)){
                                        printw("##");
                                }
                                else{
                                        printw("  ");
                                }
                        }
                                printw("\n");
                }
                if(row==19){
                        for(col=0;col<20;col++){
                                printw("--");
                        }
                        printw("\n");
                        printw("By Leo,key=%d\n",key);
                        printw("food.row=%d food.col=%d\n",food.row,food.col);
                }
        }
}

/*增减关于蛇的身子节点*/
void addNode(){
        psnake new=NULL;
        new=(psnake)malloc(sizeof(snake));
        new->next=NULL;
        switch(dir){	//控制蛇身上下左右
                case UP :
                        new->row=tail->row-1;
                        new->col=tail->col;
                        break;
                case DOWN:
                        new->row=tail->row+1;
                        new->col=tail->col;
                        break;
                case LEFT :
                        new->row=tail->row;
                        new->col=tail->col-1;
                        break;
                case RIGHT :
                        new->row=tail->row;
                        new->col=tail->col+1;
                        break;
        }
        tail->next=new;
        tail=new;
}

/*初始化蛇身*/
void initSnake(){
        psnake p=NULL;
        dir=RIGHT;
        while(head!=NULL){
                p=head;
                head=head->next;
                free(p);	//重新开始后需要释放空间
        }
        initFood();			//初始化食物
        head=(psnake)malloc(sizeof(snake));
        head->row=1;
        head->col=1;
        head->next=NULL;
        tail=head;
        /*增加蛇身的初始化长度*/
        addNode();			
        addNode();
        addNode();
}

/*删除一个头节点*/
void deleteSnake(){
        psnake p=NULL;
        p=head;
        head=head->next;
        free(p);		//释放空间，避免空间泄漏
}

/*判断蛇的死亡条件*/
int ifSnakeDie(){
        psnake p=NULL;
        p=head;
        if(tail->row<0 || tail->col==0 || tail->row==20 || tail->col==20){	//判断是否撞墙
 
                return 1;
        }
        while(p->next!=NULL){//
                if(p->row==tail->row && p->col==tail->col){					//判断节点是否重合，及是否撞到自己
                        return 1;
                }
                        p=p->next;
        }
                        return 0;
}

/*移动蛇*/
void moveSnake(){
        addNode();	//增加一个节点
        if(whetherSnakeFood(tail->row,tail->col)){	//判断是否有食物
                initFood();
        }
        else{
                deleteSnake();//删除一个节点，实现蛇身移动
        }
        if(ifSnakeDie()){	//判断是否死亡
                initSnake();
        }
}

/*刷新游戏界面*/
void* refreshGameFace(){
        while(1){
                moveSnake();	//移动蛇身
                gameInterFace();
                refresh();		//刷新界面
                usleep(100000); //为了不警报，最后在添加<unistd.h>头文件
        }
}

/*使蛇身不能同时上下或者左右移动*/
void turn (int direction){
        if(abs(dir) != abs(direction)){
                dir=direction;
        }
 
}

/*方向键*/
void* changeDirection(){
        while(1){
                key=getch();	//等待输入键值
                switch(key){
                        case KEY_DOWN:
                                turn(DOWN);
                                break;
                        case KEY_UP:
                                turn(UP);
                                break;
                        case KEY_LEFT:
                                turn(LEFT);
                                break;
                        case KEY_RIGHT:
                                turn(RIGHT);
                                break;
                }
        }
}

int main(){
        pthread_t k1;	//linux线程标志
        pthread_t k2;
        initNcure();	//初始化函数
        initSnake();	//初始化蛇身
        gameInterFace();//游戏界面
        pthread_create(&k1,NULL,refreshGameFace,NULL);	//线程1,刷新界面
        pthread_create(&k2,NULL,changeDirection,NULL);	//线程2,改变方向
        while(1);	//主线程
        getch();
        endwin();
        return 0;
}
