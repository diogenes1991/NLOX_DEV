#include "Complex.h"
#include <complex>




int main(){
    
  
  std::complex<int> Z1(3,1);
  std::complex<int> Z2(5,-1);
  Complex z1(3,1);
  Complex z2(5,-1);
    
  std::cout << Z1*Z2 << std::endl;
  std::cout << z1*z2 << std::endl;

  std::cout << z1.get_r() << std::endl; 

  Complex g;
  Complex h(z1);
  
  g.set_r(33);
  g.set_i(-22);
  
  std::cout << g*g << std::endl;
}
