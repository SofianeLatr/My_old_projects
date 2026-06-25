#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct Node{
    char op[4];
    struct Node* next; 
    int out_parentheses;
}Node;

typedef struct treeNode{
    char data[10];
    struct treeNode* left;
    struct treeNode* right;
}treeNode;

typedef struct Stack{
    Node* head;
}Stack;

typedef struct binaryTree{
    treeNode* root;
}binaryTree;

void initializeTree(binaryTree* T){
    T->root = NULL;
}

void initialize(Stack* S){
    S->head = NULL;
}

void push(Stack* S, char str[4]){
    Node* tmp = S->head;
    S->head = malloc(sizeof(Node));
    if (S->head == NULL){
        printf("Can't allocate.");
        return;
    }
    strcpy(S->head->op, str);
    S->head->out_parentheses = 0;
    S->head->next = tmp;
}

Node pop(Stack* S){
    Node tmp = *(S->head);
    Node* freed = S->head;
    S->head = S->head->next;
    free(freed);
    return tmp;
}

void display (Stack* S){
    Node* current = S->head;
    while(current != NULL){
        printf("%s ", current->op);
        current = current->next;
    }   
}

void insertRight(treeNode* N, char str[10]){
    if(N->right == NULL){
        treeNode* new = malloc(sizeof(treeNode));
        N->right = new;
        N->left = NULL;
        strcpy(N->right->data, str);
    }else{
        strcpy(N->right->data, str);
    }
}

void insertLeft(treeNode* N, char str[10]){
    if(N->left == NULL){
        treeNode* new = malloc(sizeof(treeNode));
        N->left = new;
        N->right = NULL;
        strcpy(N->left->data, str);
    }else{
        strcpy(N->left->data, str);
    }
}

void insert(treeNode* N, char str[10], int side){
    
    if(side == 1){
        insertLeft(N, str);
    }else{
        insertRight(N, str);
    }
}

int compare(char expression[], int index, char word[]){
    for(int i=0; i< (int)(strlen(word)); i++){
        if(expression[index++] != word[i]){
            return 0;
        }
    }
    return 1;
}

int equalDoubleComparison(char exp[], int i){
    if((exp[i] == '=' && exp[i+1] == '=')||(exp[i] == '!' && exp[i+1] == '=')
        ||(exp[i] == '<' && exp[i+1] == '=')||(exp[i] == '>' && exp[i+1] == '=')){
            return 1;
    }else{
            return 0;
    }
}

int equalLetterNumber(char exp[], int index){
    if ((exp[index] >= '0' && exp[index] <= '9') 
        || (exp[index] >= 'a' && exp[index] <= 'z')
        || (exp[index] >= 'A' && exp[index] <= 'Z')){
            return 1;
    }else{
        return 0;
    }
}

int fillTree(char postfix[], treeNode* current, int index, int side){
    if(postfix[index] == -1){
        return index;
    }
    if(postfix[index] == ' '){
        index--;
    }
    char tmp[10];

    if (compare(postfix, index, "AND")){
        insert(current, "AND\0", side);
        index = index-3;

    }else if(compare(postfix, index, "NOT")){
        insert(current, "NOT\0", side);
        index = index-3;
        index = fillTree(postfix, current, index, 1);
        return index;

    }else if(compare(postfix, index, "OR") || equalDoubleComparison(postfix, index)){
        tmp[0] = postfix[index-1]; tmp[1] = postfix[index]; tmp[2] = '\0';
        insert(current, tmp, side);
        index = index-2;

    }else if(postfix[index] == '<' || postfix[index] == '>'){
        tmp[0] = postfix[index]; tmp[1] = '\0';
        insert(current, tmp, side);
        index--;

    }else if(equalLetterNumber(postfix, index)){
        int k = index;
        int l = 0;
        while (k >= 0 && equalLetterNumber(postfix, k)) {
            tmp[l++] = postfix[k--];
        }
        tmp[l] = '\0';
        char tmp2[10];
        for (int a = 0; a < l; a++) tmp2[a] = tmp[l-1-a];
        tmp2[l] = '\0';
        insert(current, tmp2, side);
        return k;
    }
    
    index = fillTree(postfix, current, index, 2);
    index = fillTree(postfix, current, index, 1);
    return index;
    
}

void displayTree(treeNode* root, int level){
    if(root == NULL) return;

    displayTree(root->right, level + 1);

    for(int i = 0; i < level; i++){
        printf("    ");
    }
    printf("%s\n", root->data);

    displayTree(root->left, level + 1);
}

int main(){
    
    char expression[100];
    printf("Write the desired expression and then press ENTER.\nexpression: ");
    fgets(expression, 100, stdin);

    //Converting to postfix expression
    char postfix[100];
    postfix[0] = '\0';

    Stack* operations = malloc(sizeof(Stack));
    initialize(operations);
    
    int i=0;
    int j=0;
    int par = 0;

    while(expression[i] != '\0' && expression[i] != '\n'){
        
        /*for(int ii=0; ii<99 || expression[ii] == '\0' || expression[ii] == '\n'; ii++){
            if (expression[ii] == '(' && expression[ii+1] == '('){
                i++;
                expression[ii] = ' ';
                for (int jj = ii; jj < 99 || expression[jj] == '\0' || expression[jj] == '\n'; jj++){
                    int found = 0;
                    if (expression[jj] == ')'){
                        for(int kk=jj; kk<100 || expression[kk] == '\0' || expression[kk] == '\n'; kk++){
                            expression[kk] = expression[kk+1];
                        }
                        found = 1;
                    }
                    if(found){
                        break;
                    }   
                }       
            }
        } */
        
        if(((expression[i] == '=' && expression[i+1] == '=')
            || (expression[i] == '!' && expression[i+1] == '=')
            || (expression[i] == '<' && expression[i+1] == '=')
            || (expression[i] == '>' && expression[i+1] == '='))){
            
            char tmp[4];
            tmp[0] = expression[i++];
            tmp[1] = expression[i++];
            tmp[2] = '\0';
            push(operations, tmp);

        }else if(expression[i] == '<' || expression[i] == '>'){

            char tmp[4];
            tmp[0] = expression[i++];
            tmp[1] = '\0';
            push(operations, tmp);

        }else if (compare(expression, i, "NOT")
                || compare(expression, i, "not")){

            push(operations, "NOT\0");
            i = i+3;

        }else if((expression[i] == 'O' && expression[i+1] == 'R')
                || compare(expression, i, "or")){

            push(operations, "OR\0");
            i = i+2;

        }else if(compare(expression, i, "AND")
                || compare(expression, i, "and")){

            push(operations, "AND\0");
            i = i+3;
           
        }else if((expression[i] >= '0' && expression[i] <= '9') 
            || (expression[i] >= 'a' && expression[i] <= 'z')
            || (expression[i] >= 'A' && expression[i] <= 'Z')) {
            
            if(expression[i] >= '0' && expression[i] <= '9'){
                while(expression[i] >= '0' && expression[i] <= '9'){
                    postfix[j++] = expression[i++];
                }
            }else{
                postfix[j++] = expression[i++];
            }
            postfix[j++] = ' ';
            
            if (operations->head != NULL){
                if((((expression[i] == ' ' || expression[i] == '\0' 
                    || expression[i] == '\n' || expression[i] == ')') && operations->head->out_parentheses == 0))
                    || (expression[i] == ')' && compare(operations->head->op, 0, "NOT\0")))  {
                        Node popped = pop(operations);
                        //printf("%s.....%s\n", popped.op, postfix);
                        if(((popped.op[0] == '=' && popped.op[1] == '=')
                            || (popped.op[0] == '!' && popped.op[1] == '=')
                            || (popped.op[0] == '<' && popped.op[1] == '=')
                            || (popped.op[0] == '>' && popped.op[1] == '=')
                            || (popped.op[0] == 'O' && popped.op[1] == 'R'))){

                                postfix[j++] = popped.op[0];
                                postfix[j++] = popped.op[1];
                                postfix[j++] = ' ';
                        }else if(popped.op[0] == '<' || popped.op[0] == '>'){

                            postfix[j++] = popped.op[0];
                            postfix[j++] = ' ';
                        }else if((popped.op[0] == 'A' && popped.op[1] == 'N' && popped.op[2] == 'D')
                                || (popped.op[0] == 'N' && popped.op[1] == 'O' && popped.op[2] == 'T')){

                                    postfix[j++] = popped.op[0];
                                    postfix[j++] = popped.op[1];
                                    postfix[j++] = popped.op[2];
                                    postfix[j++] = ' ';
                        }
                        if(expression[i] == ')' && par != 0){ 
                            par--;
                        }
                }
            }
        }else if( operations->head != NULL && expression[i] == '('){

            operations->head->out_parentheses = 1;
            i++;
            par ++;
            
        }else if(expression[i] == ')' && par == 0 && operations->head != NULL){
            
            Node popped = pop(operations);
            if( (popped.op[0] == '=' && popped.op[1] == '=') ||
                (popped.op[0] == '!' && popped.op[1] == '=') ||
                (popped.op[0] == '<' && popped.op[1] == '=') ||
                (popped.op[0] == '>' && popped.op[1] == '=') ||
                (popped.op[0] == 'O' && popped.op[1] == 'R') ){

                postfix[j++] = popped.op[0];
                postfix[j++] = popped.op[1];
                postfix[j++] = ' ';
            }
            else if(popped.op[0] == '<' || popped.op[0] == '>'){
                postfix[j++] = popped.op[0];
                postfix[j++] = ' ';
            }else{
                postfix[j++] = popped.op[0];
                postfix[j++] = popped.op[1];
                postfix[j++] = popped.op[2];
                postfix[j++] = ' ';
            }           
            if(operations->head == NULL){
                i++;}
            
        }else{
            i++;
        }
        if(expression[i] == '\0' || expression[i] == '\n'){
            postfix[j] = '\0';
        }

    }
    printf("\noriginal: %s", expression);
    printf("\npostfix: %s", postfix);

    
    binaryTree* tree = malloc(sizeof(binaryTree));
    initializeTree(tree);

    int idx = j - 1;
    while (idx >= 0 && postfix[idx] == ' ') idx--;

    char temp[10];
    int t = 0;

    while (idx >= 0 && postfix[idx] != ' ') {
        temp[t++] = postfix[idx--];
    }
    temp[t] = '\0';

    for (int a = 0; a < t/2; a++) {
        char c = temp[a];
        temp[a] = temp[t-1-a];
        temp[t-1-a] = c;
    }

    tree->root = malloc(sizeof(treeNode));
    strcpy(tree->root->data, temp);
    tree->root->left = NULL;
    tree->root->right = NULL;

    fillTree(postfix, tree->root, idx, 1);
    
    displayTree(tree->root, 0);
    return 0;
}