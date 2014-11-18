/*
 * =====================================================================================
 *
 *       Filename:  create_sparse.c
 *
 *    Description:  create sparse file
 *
 *        Version:  1.0
 *        Created:  2014/08/21 17时36分06秒
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
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>


int main(int argc, char *argv[]){
	int fd = open("./hello", O_CREAT | O_TRUNC | O_RDWR);
	lseek(fd, 10, SEEK_SET);
	write(fd, "world123", 16);
	close(fd);


	return 0;
}

