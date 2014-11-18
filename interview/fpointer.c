/*
 * =====================================================================================
 *
 *       Filename:  fpointer.c
 *
 *    Description:  function pointer , call back function
 *
 *        Version:  1.0
 *        Created:  2014/10/22 02时04分45秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zhihua Ye (varvar), zhihuaye@gmail.com
 *   Organization:  NGO
 *
 * =====================================================================================
 */

#include <stdio.h>

typedef int (*integer_op)(int a, int b);


int add(int a, int b);
int multiply(int a, int b);


int main(int argc, char **argv){

	integer_op op_array[2] = {add, multiply};
	printf("add is %d.\n",op_array[0](1,2));
	printf("multiply is %d.\n",op_array[1](1,2));

	return 0;
}



int add(int a, int b){

	return a+b;

}

int multiply(int a, int b){

	return a*b;

}

