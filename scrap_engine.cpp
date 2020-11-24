#include<iostream>
#include<sys/ioctl.h> //ioctl() and TIOCGWINSZ
#include<unistd.h> // for STDOUT_FILENO
//using namespace std;
// This should be scrap_engine, but just in c++, I don't know, why I'm doing this shit, it's just pain...
// C++ is the greatest crap I ever witnessed in my live...

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
    std::string a;
    for (int i=0; i<height; i++){
      for (int j=0; j<width; j++){
        a+=map[j][i];
      }
      a+="\n";
    }
    //std::cout << a;
    printf("%s", a.c_str());
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
    backup=(*map).map[x][y];
    map->map[x][y]=character;
  }
  void set(int ix, int iy){
    if (!added){
      return;
    }
    map->map[x][y]=backup;
    backup=map->map[ix][iy];
    map->map[ix][iy]=character;
    x=ix;
    y=iy;
  }
};

// some tests
int main(){
  struct winsize size;
  ioctl(STDOUT_FILENO, TIOCGWINSZ, &size);

  Map map(size.ws_row-1, size.ws_col, ' ');
  map.show();
  sleep(1);
  Object ob('h');
  ob.add(&map, 3, 4);
  map.show();
  sleep(1);
  while (true){
    ob.set(2, 2);
    map.show();
    usleep(100000);
    ob.set(5, 5);
    map.show();
    usleep(100000);
  }
  ob.set(2, 2);
  map.show();
  sleep(1);
  return 0;
}
