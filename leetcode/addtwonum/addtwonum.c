/*
 @author: zhihuaye
 @cases:
1. try this one 7->8->9, 5->3->3
2. 1->2->3, 4->5->6
3. 9->9->9, 3
4. 1->4, 0

*/

#include <stdio.h>
#include <stdlib.h>


struct ListNode {
     int val;
     struct ListNode *next;
};

//define a new structure to record the revert array.
struct intArray{
	int *array;
	int count;
};


struct ListNode* deleteNode(struct ListNode *list, int val){


}



//add element into the list
struct ListNode* addToList(struct ListNode* list, int val){
	struct ListNode *new = calloc(1, sizeof(struct ListNode));
	if(new == NULL){
		printf("calloc failed when init a list!\n");
		return list;
	}
	new->val = val;
	new->next = NULL;
	if(list){
		struct ListNode *templist = list;
		while(templist){
			if(templist->next){
				templist = templist->next;	
			}else{
				templist->next = new;
				break;
			}
		}	

	}else{
		list = new;
	}

	return list;
}


//iterate the list, return a integer array.
struct intArray *iterateList(struct ListNode* list){
	struct intArray *retarray = calloc(1, sizeof(struct intArray));
	if(retarray == NULL){
		printf("calloc intArray failed.\n");
		return NULL;
	}

	int **ret = &retarray->array;
	int *tmp = NULL; //incase realloc failed.
	int count = 1;
	while(list){
		tmp = realloc(*ret, count*sizeof(int));
		if(tmp){
			*ret = tmp;
			*(*ret + count -1) = list->val;	
		}else{
			printf("realloc failed when count is %d.\n", count);
		}
		list = list->next;
		count++;
	}
	retarray->count = count - 1;
	return retarray;
}

//reverse the list
struct ListNode* reverseList(struct ListNode* list){
	struct ListNode* prev = NULL;
	struct ListNode* head = list;
	struct ListNode* temp = NULL;

	while(head){
		temp = head;
		head = head->next;
		temp->next = prev;
		prev = temp;
	}
	return prev;
}
struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
	if(l1 == NULL || l2 == NULL)
		return NULL;
	
	struct ListNode* l3 = NULL;
	struct intArray *arrayl1 = iterateList(l1);
	struct intArray *arrayl2 = iterateList(l2); 
	int len1 = arrayl1->count;
	int len2 = arrayl2->count;
	struct intArray *big = NULL;
	struct intArray *small = NULL;
	int len = 0;
	int extra = 0;
	//choose the shorter len
	if(len1 >= len2){
		len = len2;
		extra = len1 - len;
		big = arrayl1;
		small = arrayl2;
	}else {
		len = len1;
		extra = len2 - len;
		big = arrayl2;
		small = arrayl1;
	}
	
	int i = 0;
	int carry = 0;
	int temp, base = 0;
	for(; i < len ; i++){
		temp = big->array[i] + small->array[i] + carry;
		base = temp % 10;
		carry =  temp / 10;
		l3 = addToList(l3, base);
	}
	
	for(i=1; i <= extra; i++){
		temp = big->array[len-1 + i] + carry;
		base = temp % 10;
		carry = temp / 10;
		l3 = addToList(l3, base);
	}
	
	if(carry)
		l3 = addToList(l3, carry);


	return l3;
  
}




int main(void){
	struct ListNode* list = NULL;
	struct ListNode* rlist = NULL;
	int i = 0;	
	list = addToList(list, 5);
	list = addToList(list, 4);
	list = addToList(list, 3);
	list = addToList(list, 2);
	list = addToList(list, 1);
	struct intArray *arrayval = iterateList(list);
	if(arrayval){
		printf("start to iterate.\n");	
		for(i=0; i < arrayval->count; i++){
			printf("%d\n", arrayval->array[i]);
		}
		printf("end iterate.\n");		
		free(arrayval->array);
		free(arrayval);
	}
	rlist = reverseList(list);
	arrayval = iterateList(rlist);
	if(arrayval){
		for(i=0; i < arrayval->count; i++){
			printf("%d\n", arrayval->array[i]);
		}		
		free(arrayval->array);
		free(arrayval);
	}
	if(list)
		free(list);	

	struct ListNode* listone = NULL;
	struct ListNode* listtwo = NULL;
	
	int arrayone[] = {7, 4, 9, 9, 9};
	int arraytwo[] = {5, 6, 4};
//	int arrayone[] = {1, 4};
//	int arraytwo[] = {0};
	int arrayonelen = sizeof(arrayone)/sizeof(arrayone[0]);
	int arraytwolen = sizeof(arraytwo)/sizeof(arraytwo[0]);
	for(i = 0; i < arrayonelen; i++){
		listone = addToList(listone, arrayone[i]);	
	}
	for(i = 0; i < arraytwolen; i++){
		listtwo = addToList(listtwo, arraytwo[i]);	
	}

	struct ListNode* listthree = NULL;
	listthree = addTwoNumbers(listone, listtwo);

	if(listone)
		free(listone);

	if(listtwo)
		free(listtwo);


	if(listthree){
		struct intArray * threearray = iterateList(listthree);
		if(threearray){
			for(i=0; i < threearray->count; i++){
				printf("%d\n", threearray->array[i]);
			}		
			free(threearray->array);
			free(threearray);
		}
		
		free(listthree);
	}


	return 0;
}





