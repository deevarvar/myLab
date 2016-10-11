/*
@auther: zhihuaye@gmail.com
@description: leetcode's two sum 

@Note: just forget the signed add/sub may overflow
see comment:
http://stackoverflow.com/questions/199333/how-to-detect-integer-overflow-in-c-c

*/


#include <stdio.h>
#include <stdlib.h>
#include "testarray.h"

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target) {
	//do iterate   
	int outerIndex = 0;
	int innerIndex = 0;
	int rightone = 0;
	for(; outerIndex < numsSize; outerIndex++ ){
		rightone = target - nums[outerIndex];
		for(innerIndex = 0; innerIndex < numsSize; innerIndex++){
			if (innerIndex == outerIndex)
				continue;
			if(rightone ==  nums[innerIndex]){
				int *result = calloc(2, sizeof(int));
				if(result){
					result[0] = outerIndex;
					result[1] = innerIndex;
					return result;			
				}else{
					printf("calloc error!.\n");
				}		
			
			}
		}

	} 
	
	//nothing matched.
	return NULL;
}

int main(void)
{

	int numsSize = sizeof(testarray)/sizeof(testarray[0]);
	int *result = twoSum(testarray, numsSize, target);

	if(result){
		printf("target is %d.\n", target);
		printf("one is %d, the other is %d.\n", result[0], result[1]);
		free(result);
	}
	return 0;
}


