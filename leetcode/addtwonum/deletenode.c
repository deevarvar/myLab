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



struct ListNode* deleteNode(struct ListNode *list, int val){
	struct ListNode *temp = list;
	struct ListNode *prev = NULL;
	while(temp){
		if(temp->val == val){
			if(prev)
				prev->next = temp->next;
			else list = temp->next;
			free(temp);
			break;
		}	
		prev = temp;	
		temp = temp->next;
	}
	return list;
}


/*linus's way*/
/*head, tail*/
void deleteNode2(struct ListNode **list, int val){
	struct ListNode **pp = list;
	struct ListNode *entry = *list;

	while(entry){
		if(entry->val == val){
			*pp = entry->next;
			free(entry);
			break;
		}
		pp = &entry->next;
		entry = entry->next;
	}


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
//	list = addToList(list, 3);
	list = addToList(list, 2);
	list = addToList(list, 1);
	iterateList(list);
	//list = deleteNode(list, 4);
	deleteNode2(&list, 4);
	if(list){
		iterateList(list);
		free(list);	
	}
	return 0;
}





