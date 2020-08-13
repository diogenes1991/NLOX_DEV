#include <iostream>
#include <cstdlib>
#include <vector> 
#include <string> 
#include <map>
#include <functional>

class Tile{
    
    public:
        Tile(int t);
        ~Tile();
        bool ok_to(Tile other);
//         virtual bool ok_from(Tile other);
        inline int get_id(){return id;}
        bool is_neighbor(Tile other);
        void set_as_neighbor(Tile* other){neighbors.push_back(other);}
        void show_neighbors(){for(auto i : neighbors){std::cout<<i->get_id()<<std::endl;}}
        
    private:
        int id;
        std::vector<Tile*> neighbors;
        std::vector<std::vector<Tile*>> Directions;
    
};

bool Tile::is_neighbor(Tile other){
    bool is_neighbor = false;
    for (auto i:neighbors){
        if (other.get_id() == i->get_id()) is_neighbor = true;
    }
    return is_neighbor;
}

Tile::Tile(int t){
    id = t;
}

Tile::~Tile(){

}

class Game{
    
    unsigned int N,M;
    
    public:
        std::vector<Tile> Board;
        std::vector<int> Active;
        Game(unsigned int N, unsigned int M);
        ~Game();
    
        
        bool is_active(int id){
            for(auto i : Active){
                if(id==i)return true;
                }
                return false;
            }
            
        bool done(){return true;}
        
        void get_play(){
            //Print message for player
            // stdin << play
            // validate 
            // if_ok -> play()
            // else print error
            int next_id;
            for(int i=0;i<=1;){
            std::cout << "Next Play?"<<std::endl;
            std::cin >> next_id;
            bool allow = false;
            for ( auto i : Active ){
                if (Board[next_id].is_neighbor(Board[i])){
                    allow = true;
                }
            }
            
            
            
            bool constraint = true;
            if(allow and !is_active(next_id)){
                std::cout<<"This is an unocupied neighbor of an active tile" << std::endl;
                std::cout<<"Now checking constraints" << std::endl;
                for(auto i : Constraint){
                    if(i.first(next_id) and i.second==0){
                        constraint = false;
                        }
                }
                if(constraint){
                    std::cout << "This play respects all constraints saving it!" << std::endl; 
                    Active.push_back(next_id);
                    for(auto i : Constraint){
                        if(i.first(next_id)){
                            i.second -= 1;
                        }
                    }
                }
                
                else{ 
                    std::cout<<"This play does not respect some constraints, I'm done"<<std::endl;
                    i=1;
                }  
            }
            else std::cout<<"This is either:\n-An ocupied tile\n-Not a neighbor of an active tile\nPlay not allowed"<<std::endl;
            }
        }

        
        
        
        void Link_Board();
        std::vector<std::pair<std::function<bool(int)>,int>> Constraint;
     
//         class T (*)(class U) throw ()
//         Pointer to a function that eats a class U instance 
//         and throws a class T instance
//         
        
//         int c = 0;
//         for (auto f : Constraint){
//             if (f(previous->id)!=f(this->id)){
//                 break;
//             }
//             c++;
//         }
//         
//         out = true;
//         switch:
//             case 1: // 90 degree now
//                 if(Constraint[c](next->id)!=Constraint[c](this->id)){
//                     out = false;
//                 }
//                 break;
//             case 2: // 90 degrees next or before
//                 if(Constraint[c](previous->previous->id)    )
                
                
        
        
};

void Game::Link_Board(){
    for (int i=0;i<Board.size();i++){
        for (int j=i;j<Board.size();j++){
//             std::cout << Board[i].get_id() << " " << Board[j].get_id() << std::endl;
            bool is_neighbor = false;
            
            int ic = ((Board[i].get_id()-1)%M);       // Column 
            int ir = int((Board[i].get_id()-1)/M)%N; // Row   
            
            int jc = ((Board[j].get_id()-1)%M);        // Column
            int jr = int((Board[j].get_id()-1)/M)%N;  // Row   
            
//             std::cout << ic << " " << ir << " " << jc << " " << jr << std::endl;
            // (Same Row and Columns differ by 1) or (Same Column and Rows differ by 1)
            
            is_neighbor = ((jr==ir) and ((ic+1)==jc or (ic-1)==jc)) or ((jc==ic)and((ir+1)==jr or (ir-1)==jr));
            
//             std::cout << (is_neighbor?"True":"False")<<std::endl;
            
            if (is_neighbor){
                Board[i].set_as_neighbor(&Board[j]);
                Board[j].set_as_neighbor(&Board[i]);
            }
        }
    }
}

Game::Game(unsigned int n, unsigned int m){
    
    N = n;
    M = m;
    
    for(int i=1;i<=n*m;i++){
        Tile T = Tile(i);
        Board.push_back(T);
    }
    
//     Creates topology
//     for (int i=1;i<=n*m;i++){
//         for (int j=1;j<=n*m;j++){
//             // j can go into i if i divides j
//             if ( i%j==0 and i!=j ) Board[i-1].set_as_neighbor(&Board[j-1]);
//         }
//     }
    
    for (int i=1;i<=n;i++){
        auto glambda = [i,n](int x){return ((x%n)==i);};
        std::pair<std::function<bool(int)>,int> J(glambda,6);
        Constraint.push_back(J);
    }
    
    for (int i=1;i<=m;i++){
        auto glambda = [i,m](int x){return ((x%m)==i);};
        std::pair<std::function<bool(int)>,int> J(glambda,3);
        Constraint.push_back(J);
    }
    
    Active.push_back(1);
    
    
}

Game::~Game(){
    
}


int main(){

    Game G = Game(5,8);
    G.Link_Board();
//     for (int i=0;i<G.Board.size();i++) {
//         std::cout << "Node #"<<i+1<<" has for neighbors:"<<std::endl;
//         G.Board[i].show_neighbors();
//     }
//     

    G.get_play();
    
return 0;
}
