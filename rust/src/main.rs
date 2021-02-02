// Scrap_engine attempt in rust

struct Map{
    map: Vec<Vec<String>>,
    obmap: Vec<Vec<Vec<Object>>>,
    width: i32,
    height: i32,
    background: String,
}
impl Map{
    fn new(width: i32, height: i32, background: String) -> Map {
        let mut map:Vec<Vec<String>> = vec![];
        for i in 0..height as usize{
            map.push(vec![]);
            for j in 0..width as usize{
                map[i].push(background.clone());
            }
        }
        let mut obmap:Vec<Vec<Vec<Object>>> = vec![];
        for i in 0..height as usize{
            obmap.push(vec![]);
            for j in 0..width as usize{
                obmap[i].push(vec![]);
            }
        }
        Map{map, obmap, width, height, background}
    }
    fn show(&self){
        let mut line = String::new();
        for i in self.map.iter(){
            line = "".to_string();
            for j in i.iter(){
                line.push_str(j);
            }
            println!("{}", line)
        }
    }
}

struct Object{
    symbol: String,
    map: Map,
    x: i32,
    y: i32,
}

impl Object{
    fn new(map: Map, symbol: String) -> Object{
        Object{symbol, map, x: 0, y: 0}
    }
    fn add(&mut self, x: i32, y: i32){
        self.x = x;
        self.y = y;
        self.map.obmap[y as usize][x as usize].push(self.clone());
    }
}

fn main(){
    let mut map:Map = Map::new(10, 5, "a".to_string());
    map.show();
}
