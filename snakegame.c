#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>

typedef struct{

    int x;
    int y;
    char diraction;
}coordinate;

coordinate snake_cords[14*14];
int snake_length = 2;

void initializing_map(char map[14][14]);
void render(char map[14][14]);
void moving_rest(char map[14][14]);
void moving_head(char map[14][14], char key);



int main() {
    
    char map[14][14];

    initializing_map(map);
    render(map);

   while (1) {
        if (_kbhit()) {
            char key = _getch();

            Sleep(500);

            moving_head(map, key);
            render(map);
        } else {
            
            Sleep(500);

            moving_head(map, snake_cords[0].diraction);
            render(map);
        }
    }

    return 0;
}



void initializing_map(char map[14][14]){
    //filling the map with empty spaces
    for (int i = 0; i < 14; i++) {
            for (int j = 0; j < 14; j++) {
                map[i][j] = 'e';
            }
    }

    //making the boundaries of the map 
    for (int i = 0; i < 14; i++) {
        map[i][0] = '+';
        map[i][13] = '+';

        map[0][i] = '+';
        map[13][i] = '+';
    }

    // snake head and tail
    map[6][6] = '>';
    map[5][6] = 'O';

    //snake cords in the map
    snake_cords[0].x = 6;   snake_cords[0].y = 6;   snake_cords[0].diraction = 'd';
    
    snake_cords[1].x = 5;   snake_cords[1].y = 6;   snake_cords[1].diraction = 'd';
    
        
}

void render(char map[14][14]){
    //printing the map
    system("cls");
    for (int j = 0; j < 14; j++) {
        for (int i = 0; i < 14; i++) {
           if (map[i][j] != 'e') {
                if(map[i][j] == 'w'){
                    
                    printf("n  ");
                } 
                else if(map[i][j] == 's'){
                    
                    printf("V  ");
                }  
                else{
                    
                    printf("%c", map[i][j]);
                    printf("  ");
                }     
                
            } 
            else {
                printf("   ");
           }
        }
        printf("\n");  
    }
}

void moving_rest(char map[14][14]){
    
    map[snake_cords[snake_length - 1].x][snake_cords[snake_length - 1].y] = 'e';
    

    for(int i = snake_length - 1; i > 0; i-- ){
        
        snake_cords[i].x = snake_cords[i - 1].x;    snake_cords[i].y = snake_cords[i - 1].y;  
        snake_cords[i].diraction = snake_cords[i - 1].diraction;  

        map[snake_cords[i].x][snake_cords[i].y] = 'O';      
    }
}

void moving_head(char map[14][14], char key){

    moving_rest(map);
    if ((key == 'w' || key == 'W') && snake_cords[0].diraction != 's'){

        snake_cords[0].y -= 1;
        snake_cords[0].diraction = 'w';
        map[snake_cords[0].x][snake_cords[0].y] = 'w';
    }
    else if ((key == 's' || key == 'S') && snake_cords[0].diraction != 'w'){

        
        snake_cords[0].y += 1;
        snake_cords[0].diraction = 's';
        map[snake_cords[0].x][snake_cords[0].y] = 's';
    }
    else if ((key == 'd' || key == 'D') && snake_cords[0].diraction != 'a'){

        
        snake_cords[0].x += 1;
        snake_cords[0].diraction = 'd';
        map[snake_cords[0].x][snake_cords[0].y] = '>';
    }
    else if ((key == 'a' || key == 'A') && snake_cords[0].diraction != 'd'){

        
        snake_cords[0].x -= 1;
        snake_cords[0].diraction = 'a';
        map[snake_cords[0].x][snake_cords[0].y] = '<';
    }
    
}