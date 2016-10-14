/*
 @author: zhihuaye
Write a function to delete a node (except the tail) in a singly linked list, given only access to that node.
 @cases:

*/

#include <stdio.h>
#include <stdlib.h>


struct ListNode {
     int val;
     struct ListNode *next;
};


void deleteNode(struct ListNode* node) {
	if(node->next == NULL){
		printf("can not delete last node.\n");
		return;
	}
	struct ListNode *next = node->next;
	node->val = next->val;
	node->next = next->next;
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
void iterateList(struct ListNode* list){
	printf("########start iterate.\n");
	while(list){
		printf("%d.\n", list->val);
		list = list->next;
	}
	printf("#######end iterate.\n");
}


int main(void){
	struct ListNode* list = NULL;
	list = addToList(list, 5);
	list = addToList(list, 4);
	list = addToList(list, 3);
	list = addToList(list, 2);
	list = addToList(list, 1);
	iterateList(list);
	
	struct ListNode* deleteone = NULL;
	deleteone = addToList(deleteone, 4);
	//deleteNode(deleteone);
	if(list){
		iterateList(list);
		free(list);	
	}

	if(deleteone)
		free(deleteone);
	return 0;
}





