#include <stdio.h>
#include <stdlib.h>

int height;
int width;

int setup(char grid[height][width]){
	int i;
	int j;
	int k;
	printf("   ");
	for(int i=0;i<width;i++){
		printf("%d ",i);
	}
	printf("\n");
	for(int j=0;j<height;j++){
		printf("%d: ",j);
		for(int k=0;k<width;k++){
			printf("%c ",grid[i][j]);
		}
		printf("\n");
	}
	return 0;
};

int main(int argc,char* argv){
	char grid[height][width];
	for(int i=0;i<height;i++){
		for(int j=0;j<width;j++){
			grid[i][j]=' ';
		}
	}
	int x=0;
	int y=0;
	grid[0][0]='x';
	printf("Let's Play Etch-a-Sketch!\n");
	printf("Here are the instructions:\n");
	printf("w->up  s->down  a->left  d->right c->clear x->exit\n")

	int flag;
	while(flag=1){
		char input;
		scanf(" %c",&input);

		if(input=='w'){
			if(y>0){
				y--;
				grid[y][x]='x';
			}
		}
		if(input=='s'){
			if(y<height-1){
				y++;
				grid[y][x]='x';
			}
		}
		if(input=='a'){
			if(x>0){
				x--;
				grid[y][x]='x';
			}
		}
		if(input=='d'){
			if(x<width-1){
				x++;
				grid[y][x]='x';
			}
		}
		if(input=='c'){
			for(int i=0;i<height;i++){
				for(int j=0;j<width;j++){
					grid[i][j]=' ';
				}
			}
		}
		if(input=='x'){
			x=0;
			y=0;
			flag=0;
		}
	}
	return 0;
}