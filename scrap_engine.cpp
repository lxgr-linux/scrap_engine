#include<iostream>
#include<iomanip>
#include<vector>
#include<sys/ioctl.h> //ioctl() and TIOCGWINSZ
#include<unistd.h> // for STDOUT_FILENO
//using namespace std;
// This should be scrap_engine, but just in c++, I don't know, why I'm doing this shit, it's just pain...
// C++ is the greatest crap I ever witnessed in my live...

class Map{
public:
  int height, width;
  char background;
  char* backgroundptr = &background;
  std::vector<std::vector<char*>> map;
  Map(int height, int width, char background){
    this->height=height;
    this->width=width;
    this->background=background;
    map.resize(height);
    for (int i=0; i<height; i++){
      std::vector<char*> k (width, backgroundptr);
      map.at(i) = k;
    }
  }
  void show(){
    std::string a;
    printf("\033c");
    for (int i=0; i<height; i++){
      for (int j=0; j<width; j++){
        a+=*map[i][j];
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
  char character;
  char* characterptr = &character;
  char* backup;
  Map* map;
  std::string state;
  bool added=false;
  Object(char character, std::string state="solid"){
    this->character=character;
    this->state=state;
  }
  void add(Map *map, int x, int y){
    this->map=map;
    this->x=x;
    this->y=y;
    added=true;
    backup=(*map).map[x][y];
    map->map[x][y]=characterptr;
  }
  void set(int ix, int iy){
    if (!added){
      return;
    }
    map->map[x][y]=backup;
    backup=map->map[ix][iy];
    map->map[ix][iy]=characterptr;
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
    usleep(10000);
    ob.set(5, 5);
    // map.background='#';
    // std::cout << *map.backgroundptr << std::endl;
    map.show();
    usleep(10000);
  }
  ob.set(2, 2);
  map.show();
  sleep(1);
  return 0;
}
