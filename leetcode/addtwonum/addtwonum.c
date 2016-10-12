/*


*/

#include <stdio.h>
#include <stdlib.h>


struct ListNode {
     int val;
     struct ListNode *next;
};


struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
    
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


//iterate the list
void iterateList(struct ListNode* list){
	while(list){
		printf("value is %d.\n", list->val);
		list = list->next;
	}

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

int main(void){
	struct ListNode* list = NULL;
	
	list = addToList(list, 5);
	list = addToList(list, 4);
	list = addToList(list, 3);
	list = addToList(list, 2);
	list = addToList(list, 1);
	iterateList(list);
	list = reverseList(list);
	iterateList(list);
	if(list)
		free(list);	

	return 0;
}





