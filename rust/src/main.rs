// Scrap_engine attempt in rust

struct Map{
    map: Vec<Vec<String>>,
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
        Map{map, width, height, background}
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

fn main(){
    let mut map:Map = Map::new(10, 5, "a".to_string());
    map.show();
}
