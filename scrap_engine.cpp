#include<iostream>
//using namespace std;

class Map{
public:
  int height, width;
  char background, map[1000][1000];
  Map(int h, int w, char b){
    height=h;
    width=w;
    background=b;
    map[width][height]={};
    for (int i=0; i<height; i++){
      for (int j=0; j<width; j++){
        map[j][i]=background;
      }
    }
  }
  void show(){
    for (int i=0; i<height; i++){
      for (int j=0; j<width; j++){
        std::cout << map[j][i];
      }
      std::cout << std::endl;
    }
  }
};

class Object{
public:
  int x, y;
  char character, backup;
  Map *map;
  std::string state;
  bool added=false;
  Object(char c, std::string s="solid"){
    character=c;
    state=s;
  }
  void add(Map *m, int ix, int iy){
    map=m;
    x=ix;
    y=iy;
    added=true;
    backup=map->map[x][y];
    map->map[x][y]=character;
  }
};


int main(){
  Map map(5, 10, '#');
  map.show();
  Object ob('h');
  ob.add(&map, 3, 4);
  map.show();
  return 0;
}
