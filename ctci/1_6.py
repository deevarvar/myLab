# -*- coding:utf-8 -*-
import unittest
class Transform:
    def transformImageMorespace(self, mat, n):
        # write code here
        newmat = [ [0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                newmat[j][n-1-i] = mat[i][j]
        return newmat
    def transformImage(self, mat, n):
        
        return mat

if __name__ == '__main__':
    t = Transform()
    n = 4
    mat = [ [ i+1+n*j for i in range(n)]for j in range(n)]
    print t.transformImageMorespace(mat, n)
