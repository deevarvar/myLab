/*
 * =====================================================================================
 *
 *       Filename:  strutil.c
 *
 *    Description:  string util function
 *
 *        Version:  1.0
 *        Created:  2014/10/28 22时36分57秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zhihua Ye (varvar), zhihuaye@gmail.com
 *   Organization:  NGO
 *
 * =====================================================================================
 */

#include <ctype.h>
#include <stdio.h>
#include <assert.h>
//strcpy
char *my_strcpy(char *dst, const char *src){
	assert((dst!=NULL&&src!=NULL));
	char *temp = dst;
	while((*dst++ = *src++)!=NULL);
	return temp;
}

//atoi
//assume that no additional chars are input
int my_atoi(const char *str){
	int value = 0;
	int sign = 1;

	assert( str != NULL );
	if(*str == '-'){
		sign = -1;
		str++;	
	}else if(*str == '+'){
		sign = 1;
		str++;
	}

	int temp = 0;

	while(isdigit(*str)){
		temp = *str - '0';
		value = 10*value+ temp;
		str++;
	}
		


	return value*sign;
}


//get from begin to end string of a string

char *my_cutoff(char *dst, char *src, int begin, int end){


	return dst;
}

//strcmp
//char default is not defined: maybe signed, or unsigned
// http://stackoverflow.com/questions/2054939/is-char-signed-or-unsigned-by-default
int strcmp(const char *str1, const char *str2){

	assert((str1!=NULL) && (str2!=NULL));
	const unsigned char *s1 = (const unsigned char *)str1;
    const unsigned char *s2 = (const unsigned char *)str2;
	while(*s1 && *s1==*s2){
		s1++;
		s2++;
	}	

	return *s1 - *s2;

}

void test_atoi(){

	printf("%d\n", my_atoi("123"));
	printf("%d\n", my_atoi("-123456"));
}


//strtol


//strstr
char *my_strstr(const char* s1, const char *s2){

	assert(s1 != NULL && s2 != NULL);
	char *ret = NULL;
	const char *start = NULL;

	while(*s1 != NULL){
		
		start = s1;
		while((*start == *s2)&&(*start != '\0')){
			start++;
			s2++;
		}

		if(*s2 != '\0'){
			s1++;
			continue;
		}else return s1; 

	}

	return ret;

}

void str_cases(const char *string, const char *key){

	printf("try to find %s in %s, result location is %s.\n", key, string , my_strstr(string, key));

}


void test_strstr(){

// s1 longer than s2
	str_cases("123 abc", "23");
	str_cases("123 abc", "ab");
	str_cases("123 abc", "e");	
	str_cases("123 abc", "12");
//s1 equal s2
	str_cases("123", "123");
	str_cases("abcdefg", "abcdefg");

//s1 shorter than s2
	str_cases("12", "123");

}

int main(int argc, char **argv){
	char *src = "Hello world!";
	char dst[256] = {0};
	my_strcpy(dst, src);
	printf("%s\n", dst);
	test_atoi();
	test_strstr();
	return 0;
}
