#include<iostream>
//using namespace std;

class Map{
public:
  int height, width;
  char background;
  char map[1000][1000];
  Map(int y, int x, char b){
    height=y;
    width=x;
    background=b;
    map[width][height]={};
    for (int i=0; i<width; i++){
      for (int j=0; j<height; j++){
        map[i][j]=background;
      }
    }
  }
  void show(){
    for (int i=0; i<width; i++){
      for (int j=0; j<height; j++){
        std::cout << map[i][j];
      }
      std::cout << std::endl;
    }
  }
};

int main(){
  Map map(5, 5, '#');
  map.show();
  return 0;
}
