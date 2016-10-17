/*
  @author: zhihuaye
  @description: find the longest string

*/


#include <stdio.h>
#include <stdlib.h>

int lengthOfLongestSubstring(char* s) {
	int hash[256];
 	int i = 0;
	for(i=0; i < 256; i++)
		hash[i] = 0;
	int count = 0;
	int tmpcount = 0;
	int val = 0;
	int previndex = 0;
	int currindex = 0;
	char *p = s;
	int extra = 0;
	int existflag = 100;
	while(*p){
		val = (int)*p;
		if(hash[val]){
			//once it exists, calc the count and reset
			
			//get the extra value
			previndex = hash[val] - existflag;	
			currindex = p - s;
			printf("val is %c,prev is %d, curr is %d.\n", val, previndex, currindex);
			extra = currindex - previndex - 1;
			
			//reset first
			for(i=0; i < 256; i++)
                		hash[i] = 0;
			//update the value
			for(i = previndex + 1; i <= currindex;i++){
				hash[*(s+i)] = existflag + i;
				printf("update %c to %d.\n", *(s+i), i);
			}

			if(tmpcount >= count)
				count = tmpcount;
			hash[val] = existflag + currindex;
			tmpcount = 1 + extra;
		}else{
			//record prev index
			hash[val] = existflag + p - s;
			tmpcount++;
		}
		p++;
	}

	if(tmpcount >= count)
		count = tmpcount;	
	return count;

}

int main(void)
{

	char *a = "abcabcbb";
	char *b = "bbbbbb";
	char *c = "pwwkew";
	char *d = "dvdf";
	char *e = "abba";
	int ret1 = lengthOfLongestSubstring(a);
	int ret2 = lengthOfLongestSubstring(b);
	int ret3 = lengthOfLongestSubstring(c);
	int ret4 = lengthOfLongestSubstring(d);
	int ret5 = lengthOfLongestSubstring(e);
	printf("%d, %d, %d, %d, %d.\n", ret1, ret2, ret3, ret4, ret5);
	char *f = "abc'\"#$5acefgh";
	int ret6 = lengthOfLongestSubstring(f);
	printf("%d.\n", ret6);

	return 0;
}



