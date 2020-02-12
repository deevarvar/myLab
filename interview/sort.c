/*
 * =====================================================================================
 *
 *       Filename:  sort.c
 *
 *    Description:  sort algorithm for baidu
 *
 *        Version:  1.0
 *        Created:  2014/10/21 16时28分38秒
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
#include "array.h"

void BubbleSort(int array[], int array_len);
void QuickSort(int array[], int low, int high);
int Partition(int array[], int low, int high);


int main(int argc,char *argv[]) {
	int array_len = sizeof(array)/sizeof(array[0]);  
	printf("array size is %d.\n", array_len);
	int i = 0;
	printf("before sort is :\n");
	for(i=0; i < array_len; i++)
      printf("%d, ", array[i]);	
	printf("\n");

//	BubbleSort(array, array_len);
	QuickSort(array, 0, array_len - 1);

	printf("after sort is :\n");
	for(i=0; i < array_len; i++)
      printf("%d, ", array[i]);	
	printf("\n");


	return 0;
}


void BubbleSort(int array[], int array_len){
	int outer_index = 0;
	int inner_index = 0; 
	int temp = -1;

	for(; outer_index < array_len; outer_index++)
		for(inner_index = 0; inner_index < array_len - outer_index - 1;inner_index++)
		{
			if(array[inner_index] >= array[inner_index+1])
			{
			  temp = array[inner_index];
			  array[inner_index] = array[inner_index+1];
			  array[inner_index+1] = temp;	
			  printf("%d %d.\n", array[inner_index], array[inner_index+1]);
			}
		}

}

int Partition(int array[], int low, int high){
	int hole = (low + high)/2;
	int temp;
	int refer = array[hole];
	//compare with the hole one
	while(low < high){
		while(low < high && array[low]< refer) low++;

		array[hole] = array[low];
		hole = low;	
		while(low < high && array[high] >= refer) high--;
		array[hole] = array[high];
		hole = high;
	}

	array[hole] = refer;
	return hole;

}

void QuickSort(int array[], int low, int high){
	int pivot = 0;
	if(low < high){
		pivot = Partition(array, low, high);
		QuickSort(array, low, pivot - 1);
		QuickSort(array, pivot + 1, high);
		
	}

}
