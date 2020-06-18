#ifndef _Complex_H
#define _Complex_H

#include <iostream>
#include <cmath>



template <class>
class Complex {
    /// Components ///
    private:
    long double  r,i;
    /// Printing Function ///
    friend std::ostream &operator<<(std::ostream &, const Complex&);
    
    public:
       /// Constructors ///
       Complex();
       Complex(const long double ,const long double );
       Complex(const Complex&); /// Copy Constructor ///  

       /// Assignment Operator ///
       Complex& operator=(const Complex&);
       Complex& operator=(const long double &);
       
       /// Deconstructor ///
       ~Complex();       

       /// Member Functions ///
       long double  get_r() const;
       long double  get_i() const;
       void set_r(const long double ); 
       void set_i(const long double );

       /// Overloaded Operators ///
       Complex operator+(const Complex&) const;
       Complex operator-(const Complex&) const;
       Complex operator*(const Complex&) ;
       Complex operator/(Complex) ;
       Complex operator!();
       
       /// Negative ///
       Complex operator-();
             
       /// Overloaded comparison operators ///
       bool operator==(const Complex&) const;
       bool operator!=(const Complex&) const;
       


};

/// Very Useful to reserve this character  ///



/// Printing Function ///

std::ostream &operator<<(std::ostream &output, const Complex& c)
{
  long double  re = c.get_r();
  long double  im = c.get_i();
  if (!(re == 0.)) output << re;
  if (!(im == 0.)) 
  {
      if( im > 0.)
        {
            if(re == 0.)  
            {
                if( im == 1. ) output << "i";
                else output << im << "i";
            }
            else 
            {
                if ( im == 1. ) output << " + i";
                else output << " + " << im << "i";
                
            }
            
        }
      else 
        {
            if(re == 0.) 
            {
                if ( im == -1. ) output << "-i";
                else output << im << "i";
                
                
            } 
            else 
            {
                if ( im == -1.) output << "-i";
                else output << " - " << -im << "i";
                
            }
            
        }
    }
    if ((re == 0.) && (im == 0.) ) output << 0;
    return output;

}

/// Constructors, deconstructor, and assignment operator ///

Complex::Complex() 
{
  r = i = 0.;
}

Complex::Complex(const long double  re, const long double  im) 
{
  r = re;
  i = im;
}

Complex::Complex(const Complex& c) 
{
  r = c.get_r();
  i = c.get_i();
  
}

Complex::~Complex() 
{
  r = i = 0.;
}

Complex& Complex::operator=(const Complex& c) 
{
  r = c.get_r();
  i = c.get_i();
  return *this;
}

Complex& Complex::operator=(const long double & c)
{
  set_r(c);
  set_i(0.);
  return *this;
}


/// Member functions ///

long double  Complex::get_r() const {return r;}
long double  Complex::get_i() const {return i;}

void Complex::set_r(const long double  re) {r = re;}
void Complex::set_i(const long double  im) {i = im;}

/// Overloaded operators ///

/// Sum ///

Complex Complex::operator+(const Complex& z) const 
{
  Complex sum(r + z.get_r(), i + z.get_i());
  return sum;  
}

/// Subtraction ///

Complex Complex::operator-(const Complex& z) const 
{
  Complex sub(r - z.get_r(), i - z.get_i());
  return sub;  
}

/// Multiplication ///

Complex Complex::operator*(const Complex& z)
{
  Complex prod( r * z.get_r() - i * z.get_i(), r * z.get_i() + i * z.get_r());
  return prod;
  
}

/// Conjugation ///

Complex Complex::operator!()
{
  Complex cong(r,-i);  
  return cong;
}

/// Negative ///

Complex Complex::operator-()
{
  Complex neg (-r,-i);
  return neg;
  
}



/// Division ///

Complex Complex::operator/(Complex z)
{
  long double  mod = (z * !z).get_r();  
  Complex num(r/mod,i/mod);
  Complex div = num * !z;
  return div;
}


///  Mixed Operators  ///

Complex operator * (long double  rhs, Complex lhs)
{
    Complex out(rhs*lhs.get_r(),rhs*lhs.get_i());
    return out;
    
    
    
    
}

Complex operator * (Complex rhs, long double  lhs)
{
    Complex out(lhs*rhs.get_r(),lhs*rhs.get_i());
    return out;
    
    
    
    
}

Complex operator + (long double  rhs, Complex lhs)
{
    Complex out(rhs+lhs.get_r(),lhs.get_i());
    return out;
    
    
    
    
}

Complex operator + (Complex rhs, long double  lhs)
{
    Complex out(rhs.get_r()+lhs,rhs.get_i()); 
    return out;
    
}

Complex operator - (Complex rhs, long double  lhs)
{
    Complex out(rhs.get_r()-lhs,rhs.get_i()); 
    return out;
    
}

Complex operator - (long double  rhs, Complex lhs)
{
    Complex out(rhs-lhs.get_r(),-lhs.get_i());
    return out;
    
    
    
    
}

Complex operator / (long double  rhs, Complex lhs)
{
    Complex out(rhs,0.0);
    return out / lhs;
    
}

Complex operator / (Complex rhs, long double  lhs)
{
    Complex out(1./lhs,0.);
    return out*rhs;
    
    
}


/// Overloaded comparison operators ///

bool Complex::operator==(const Complex& c) const 
{
    long double  re1 = c.get_r();
    long double  im1 = c.get_i();
    long double  re2 = r;
    long double  im2 = i;
    
    int re_ent1,re_dec1,im_ent1,im_dec1;
    int re_ent2,re_dec2,im_ent2,im_dec2;
    
    re_ent1 = re1;
    im_ent1 = im1;
    re_ent2 = re2;
    im_ent2 = im2;    
    
    re_dec1 = re1 - re_ent1;
    im_dec1 = im1 - im_ent1;
    re_dec2 = re2 - re_ent2;
    im_dec2 = im2 - im_ent2;    
    
    re_dec1 = 1000000000000 * re_dec1;
    im_dec1 = 1000000000000 * im_dec1;
    re_dec2 = 1000000000000 * re_dec2;
    im_dec2 = 1000000000000 * im_dec2;
    
    bool cond = ( (re_ent1 == re_ent2)  &&  (re_dec1 == re_dec2)  );
    int dis1,dis2;
    dis1 = std::abs( re_dec1 - re_dec2 );
    dis2 = std::abs( im_dec1 - im_dec2 );
    bool cond2 = ( (dis1 < 2) && (dis2 < 2) );
    return cond && cond2;
    
}

bool Complex::operator!=(const Complex& c) const 
{
    return (r != c.get_r()) || (i != c.get_i());
}


///////////  Some extra functions   /////////////////////////

long double  Phase(Complex a)
{
    long double  re = a.get_r();
    long double  im = a.get_i();
    long double  phi = atan(im/re);
    long double  pi = acos(-1.0);
    if (re == 0  && im == 0) {return 0;}
    if (re >  0  && im >  0) {return phi;}
    if (re <  0  && im >= 0) {return pi-phi;}
    if (re <  0  && im <  0) {return pi+phi;}
    if (re >= 0  && im <  0) {return (2*pi)+phi;}
}


Complex Sqrt(Complex a)
{
    long double mod = (!a*a).get_r();
    long double re = a.get_r();
    long double im = a.get_i();
    if (im == 0) 
    {
        if(re > 0)
        {
            Complex root(sqrt(re),0);
            return root;
               
        }
        
        else 
        {   
            Complex root(0,sqrt(-re));
            return root;
            
        }
                
    }
    else 
    {
        long double ar,ai;
        ar = sqrt( sqrt(mod) + re );
        ai = sqrt( sqrt(mod) - re );
        Complex root ( ar/sqrt(2.) , ai/sqrt(2.) );
        return root;
    }
        
        
}





const Complex i(0,1);


























#endif
