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
        std::vector<Tile*> neighbors;
        
    private:
        int id;
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

struct pair{
    std::function<bool(int)> cls;
    int val;
};

class Game{
    
    unsigned int N,M;
    std::vector<Tile> Board;
    std::vector<int> Active;
    std::vector<int> Topology;
    
    public:
//         std::vector<std::pair<std::function<bool(int)>,int>> Constraint;
        
        std::vector<pair> Constraint;
        
        Game(unsigned int N, unsigned int M);
        ~Game();
        
        bool is_active(int id);
        bool done();
        void print_constraints();
        void get_play();
        void Link_Board();
        void print_cross_sections();
        void print_neraness();
        void show_active();
        bool lost();
             
        
};

void Game::Link_Board(){
    for (int i=0;i<Board.size();i++){
        for (int j=i;j<Board.size();j++){
//             std::cout << Board[i].get_id() << " " << Board[j].get_id() << std::endl;
            bool is_neighbor = false;
            
            int ic = (Board[i].get_id()%M);       // Column 
            int ir = int((Board[i].get_id())/M)%N; // Row   
            
            int jc = (Board[j].get_id()%M);        // Column
            int jr = int(Board[j].get_id()/M)%N;  // Row   
            
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

void Game::get_play(){
            //Print message for player
            // stdin << play
            // validate 
            // if_ok -> play()
            // else print error
            int next_id;
            while(true){
            if(done()){ 
                std::cout << "Congratulations, you Win!" << std::endl;
                break;
            }
            if(lost()){
                std::cout << "No more plays can be made: Game Over!"<<std::endl;
                break;
            }
            print_cross_sections();
//             print_constraints();
            show_active();
            std::cout << "Next Play?"<<std::endl;
            std::cin >> next_id;
            bool allow = false;
            for ( auto i : Active ){
                if (Board[next_id].is_neighbor(Board[i])){
                    allow = true;
                }
            }
            
            bool constraint = true;
            if( allow and !is_active(next_id) ){
                std::cout<<"This is an unocupied neighbor of an active tile" << std::endl;
                std::cout<<"Now checking constraints" << std::endl;
                for(auto i : Constraint){
                    if(i.cls(next_id) and i.val==0){
                        constraint = false;
                        }
                }
                if(constraint){
                    std::cout << "This play respects all constraints saving it!" << std::endl; 
                    Active.push_back(next_id);
                    for(int k=0;k<Constraint.size();k++){
                        if(Constraint[k].cls(next_id)){
                            Constraint[k].val -= 1;
                        }
                        
                    }
                }
                
                else{ 
                    std::cout<<"This play does not respect some constraints!"<<std::endl;
                }  
            }
            else std::cout<<"This is either:\n-An ocupied tile\n-Not a neighbor of an active tile\nPlay not allowed"<<std::endl;
            }
}

bool Game::is_active(int id){
            for(auto i : Active){
                if(id==i)return true;
                }
                return false;
}

void Game::print_cross_sections(){
    for(auto i:Constraint){
        std::cout<<"These tiles are grouped by a constraint:\n{ ";
        for(auto j:Board){
            if(i.cls(j.get_id())) std::cout<<j.get_id()<<" ";
        }
        std::cout<<"}"<<std::endl;
        std::cout<<"Only \033[31m"<<i.val<<"\033[0m more can be active at the time"<<std::endl;
    }
}

void Game::print_neraness(){
    for(auto i:Board){
        std::cout<<"The tile "<<i.get_id()<<" has for neighbors:\n";
        i.show_neighbors();
    }
}

bool Game::done(){
    bool done = true;
    for (auto i:Constraint){
        if(i.val!=0) done = false;
    }
    return false;
}

void Game::show_active(){
    std::cout<<"The active tiles are: { ";
    for(auto i: Active){
        std::cout<<i<<" ";
    }
    std::cout<<"}"<<std::endl;
}

Game::Game(unsigned int n, unsigned int m){
    
    N = n;
    M = m;
    
    for(int i=0;i<n*m;i++){
        Tile T = Tile(i);
        Board.push_back(T);
    }
    
    for (int i=0;i<m;i++){
        auto glambda = [i,m](int x){return (((x)%m)==i);};
        pair K;
        K.cls = glambda;
        K.val = 3;
        std::pair<std::function<bool(int)>,int> J(glambda,3);
        Constraint.push_back(K);
    }
    
    for (int i=0;i<n;i++){
        auto glambda = [i,m,n](int x){return ((int((x)/m)%n)==i);};
        pair K;
        K.cls = glambda;
        K.val = 3;
        std::pair<std::function<bool(int)>,int> J(glambda,3);
        Constraint.push_back(K);
    }
    
    Active.push_back(1);
    
    
}

Game::~Game(){
    
}

bool Game::lost(){  
    bool lost = true;
    for (auto j: Board){
        bool allow = true;
        // First we check if there are tiles that can be filled 
        for (auto c: Constraint){
            if(c.cls(j.get_id()) and c.val!=0) {
                for (auto a: Active){
                    allow = allow and (a!=j.get_id());
                }
            }
        }
        lost = (lost and !allow);
        if(allow) std::cout << "A Play into "<<j.get_id()<<" is allowed!"<<std::endl;
    }
    return lost;
}

int main(){
    
    Game G = Game(8,8);
    G.Link_Board();
    G.get_play();
    
    return 0;
}
