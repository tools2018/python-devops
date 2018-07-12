#!/usr/bin/env python
def funcA(A):
    print("function A")

def funcB(B):
    print(B(5))
    print("function B")

# @funcA
@funcB
def func(c):
    print("function C")
    return c**2
