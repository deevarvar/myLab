/*
 * =====================================================================================
 *
 *       Filename:  1.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  2014/09/12 15时33分52秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zhihua Ye (varvar), zhihuaye@gmail.com
 *   Organization:  NGO
 *
 * =====================================================================================
 */
#include <stdio.h>
#include <string.h>


int main(void){
	char dst[100] = "abcdefghijk";
	char src[100] = "123456";
	char *r = strncpy(dst+1, src, 3);

	printf("%s, %s.\n", r, dst);


}
