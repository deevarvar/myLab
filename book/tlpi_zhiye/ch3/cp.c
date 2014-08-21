/*
 * =====================================================================================
 *
 *       Filename:  cp.c
 *
 *    Description:  simple code to copy files
 *
 *        Version:  1.0
 *        Created:  2014/08/19 17时07分55秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zhihua Ye (varvar), zhihuaye@gmail.com
 *   Organization:  NGO
 *			 Note: 
 *					1. ssize_t
 *					2. mode_t
 *					3. fread() does not distinguish between end-of-file and error
 * =====================================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <string.h>
#include <errno.h>


// define a macro to debug
//TODO: add debug level
#ifndef NODEBUG
#define DBG(fmt,...) fprintf(stderr, "%d "fmt"\n", (int)time(NULL),##__VA_ARGS__)
#endif

void Usage(){
	fprintf(stderr, "Usage: ./cp src_file dst_file\n");
}


int main(int argc, char *argv[]){

	if(argc != 3){
		Usage();
		return -1;
	}else{
		DBG(" src is %s, dst is %s.", argv[1], argv[2]);	
	}
	
	char buffer[BUFSIZ] = {0};
	char *src_file = argv[1];
	char *dst_file = argv[2];

	DBG("buffer size is %d.", BUFSIZ);

	//use open, fread do not distingish file eof.

	int src_fd = open(src_file, O_RDONLY);
	if(src_fd == -1){
		DBG("Can not open %s.", src_file);
		DBG("errno/errmsg is %d/%s.", errno, strerror(errno));
		return -1;
	}


	int dst_openflags = O_CREAT | O_RDWR | O_TRUNC;
	mode_t dst_file_permission = S_IRUSR | S_IWUSR | S_IRGRP |
								 S_IWGRP | S_IROTH | S_IWOTH;
	ssize_t numRead;	
	ssize_t numWrite;

	int dst_fd = open(dst_file, dst_openflags, dst_file_permission);
	if(dst_fd == -1){
		DBG("Can not open %s.", dst_file);
		DBG("errno/errmsg is %d/%s.", errno, strerror(errno));
		return -1;
	}

	while((numRead = read(src_fd,buffer, BUFSIZ)) > 0){
		DBG("read %d bytes, and content is %s.", numRead, buffer);
		numWrite = write(dst_fd, buffer, numRead);
 		DBG("write %d bytes.", numWrite);
		if(numWrite != numRead){
			DBG("write %s error.\n", dst_file);
			DBG("errno/errmsg is %d/%s.", errno, strerror(errno));
			return -1;
		}
	}   



	if(close(src_fd)){
		DBG("errno/errmsg is %d/%s.", errno, strerror(errno));
		return -1; 
	}

	if(close(dst_fd)){
		DBG("errno/errmsg is %d/%s.", errno, strerror(errno));
		return -1;
	}

	return 0;
}



