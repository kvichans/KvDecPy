"""
Tests for DecPy

Author: Andrey Kvichansky, github.com/kvichans
"""

import math
from math import sqrt

import pytest

from decpy import var,lazyfun

# Тесты для примеров из книги 
#   БИБЛИОТЕКА DECPY
#   Декларативное программирование на Python

def test_book_1_2_ex1_pithagor():
    a,b = var(2)
    pithagor=(a**2+b**2)**0.5
    a(3);b(4)
    assert pithagor==5.0
    a(5);b(12)
    assert pithagor==13.0

def test_book_1_2_ex2_pithagor():
    a,b = var(2)
    pithagor=(a**2+b**2)**0.5
    assert pithagor(3,4)==5.0
    assert pithagor(5,12)==13.0

def test_book_1_2_ex3():
    a,b = var(2)
    f=a**2+a*b+a+1
    assert f(2,3)==13

def test_book_1_3_ex1():
    a,b,c=var(3)
    f=a+b
    a(1);b(2);c(3)
    g=c+f
    assert g==6
    a(4)
    assert g==9
    
def test_book_1_3_ex2():
    a,b,c=var(3)
    f=a+b
    a(1);b(2);c(3)
    g=c+f()
    assert g==6
    a(4)
    assert g==6

def test_book_1_4_ex1_pithagor():
    def sqrt(x):
        return x**0.5
    a,b = var(2)
    pithagor=sqrt(a**2+b**2)
    assert pithagor(3,4)==5.0

def test_book_1_4_ex2_pithagor_lazyfun():
    sqrt=lazyfun(math.sqrt)
    a,b = var(2)
    pithagor=sqrt(a**2+b**2)
    assert pithagor(3,4)==5.0
    
    @lazyfun
    def sqrt(x):
        return math.sqrt(x)
    a,b = var(2)
    pithagor=sqrt(a**2+b**2)
    assert pithagor(3,4)==5.0

def test_book_1_4_ex3_exp_lazyfun():
    @lazyfun
    def exp(n):
        return 2**n
    x = var()
    f = x + exp(x)
    assert f(3)==11
    
    x = var()
    f = x + lazyfun(lambda x: 2**x)(x)
    assert f(3)==11

def test_book_1_5_ex1_dist():
    class point:
        def __init__(self,x=0,y=0):
            self.x=x;self.y=y
    A,B=var(2)
    dist=((A.x-B.x)**2+(A.y-B.y)**2)**0.5
    
    p1=point(0,0);p2=point(3,4);p3=point(5,12)
    assert dist(p1,p2)==5.0
    assert dist(p1,p3)==13.0
    
    A(point(0,0));B(point(3,4))
    assert dist==5.0
    B(point(5,12))
    assert dist==13.0
    
    A(point(0,0))
    p=point(3,4)
    B(p)
    assert dist==5.0
    p.x=5;p.y=12
    assert dist==13.0

def test_book_1_6_ex1_dist():
    v=var()
    mod=(v[0]**2+v[1]**2+v[2]**2)**0.5
    assert mod([2,3,6])==7.0
    assert mod([1,4,8])==9.0

def test_book_1_7_ex1_prm():
    class point:
        def __init__(self,x=0,y=0):
            self.x=x;self.y=y
    ABC = var()
    perimeter = (((ABC[0].x-ABC[1].x)**2+(ABC[0].y-ABC[1].y)**2)**0.5+
                 ((ABC[1].x-ABC[2].x)**2+(ABC[1].y-ABC[2].y)**2)**0.5+
                 ((ABC[2].x-ABC[0].x)**2+(ABC[2].y-ABC[0].y)**2)**0.5)
    assert perimeter([point(0,0),point(0,4),point(3,0)])==12
    
    def dist(A,B):
        return ((A.x-B.x)**2+(A.y-B.y)**2)**0.5
    ABC = var()
    perimeter = dist(ABC[0],ABC[1]) + dist(ABC[1],ABC[2]) + dist(ABC[2],ABC[0])
    assert perimeter([point(0,0),point(0,4),point(3,0)])==12

def test_book_2_1_ex1_lazy_cond():
    el=var()
    L=[10,20,30,40,50]
    M=var(L)[el>15]
    assert M==[20,30,40,50]
    L.append(60)
    assert M==[20,30,40,50,60]

def test_book_2_1_ex2_y2000():
    curr_year=2025
    class person:
        def __init__(self,name,year):
            self.name=name;self.year=year
#       def __str__(self):
#           return f"{self.name} {curr_year-self.year}"
        def __repr__(self):
           #return self.name+" "+str(curr_year-self.year)
            return f"'{self.name} {curr_year-self.year}'"
    p1=person("Василий",1990)
    p2=person("Иван",2000)
    p3=person("Мария",2001)
    people=[p1,p2,p3]
    el=var()
    youth=var(people)[el.year>=2000]
    pass;                      #print()
    pass;                      #print(f'{people =}')
    pass;                      #people_=["Василий 35","Иван 25","Мария 24"]
    pass;                      #print(f'{people_=}')
    pass;                      #assert repr(people)==repr(["Василий 35","Иван 25","Мария 24"])
    pass;                      #return 
    pass;                       assert str(people)==str(["Василий 35","Иван 25","Мария 24"])
#   assert people==["Василий 35","Иван 25","Мария 24"]  # Fail! Why?
    pass;                       assert str(youth)==str(["Иван 25","Мария 24"])
#   assert youth==["Иван 25","Мария 24"]                # Fail! Why?
    p4=person("Андрей",2024)
    people.append(p4)
    pass;                       assert str(people)==str(["Василий 35","Иван 25","Мария 24","Андрей 1"])
#   assert people==["Василий 35","Иван 25","Мария 24","Андрей 1"]
    pass;                       assert str(youth)==str(["Иван 25","Мария 24","Андрей 1"])
#   assert youth==["Иван 25","Мария 24","Андрей 1"]

def test_book_2_1_ex3_notlazy_cond():
    el=var()
    L=[10,20,30,40,50]
    M=var(L)[el>15]()   # see ()
    assert M==[20,30,40,50]
    L.append(60)
    assert M==[20,30,40,50]

def test_book_2_1_ex4_lazy_set_cond():
    el=var()
    L={10,20,30,40,50}
    M=var(L)[el>15]
    assert M=={20,30,40,50}
    L.add(60)
    assert M=={20,30,40,50,60}

###########
# Run as 
#   py13 -m pytest -q tests/test_var.py
#   uv run  pytest -q tests/test_var.py