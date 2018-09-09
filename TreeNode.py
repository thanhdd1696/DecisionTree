from util import *
from random import randint


'''
This function computes and finds max Information Gain among attributes
@param: X_examples, Y_examples: set of examples 
@param: selected_attributes: a list of boolean values indicating whether an attribute is already selected or not
@return: the attribute that has highest Information Gain value
'''
def max_gain(X_examples, Y_examples, selected_attributes):
    max = -1
    max_index = -1
    num_of_positive_ex = 0
    num_of_negative_ex = 0
    #count the number of positive and negative values
    for i in range(0, len(Y_examples)):
        if (Y_examples[i] == 0):
            num_of_negative_ex += 1
        else:
            num_of_positive_ex += 1
    H_current_attr = B(num_of_positive_ex / (num_of_positive_ex + num_of_negative_ex))     
    
    #find the maximum information gain attribute
    for i in range(0, 37):
        if (not selected_attributes[i]):
            potential_left = []
            potential_right = []
            ones_on_left = 0
            ones_on_right = 0
            for j in range(0, len(X_examples)):
                if (X_examples[j][i] == 0):
                    potential_left.append(Y_examples[j]) 
                    if (Y_examples[j] == 1):
                        ones_on_left += 1
                else:
                    potential_right.append(Y_examples[j])
                    if (Y_examples[j] == 1):
                        ones_on_right += 1
            a = len(potential_left) + len(potential_right)
            b = len(potential_left)
            c = len(potential_right)
            if (b == 0 and c != 0):
                Remainder = (c/a)*B(ones_on_right/c)
            elif (c == 0 and b != 0):
                Remainder =  (b/a)*B(ones_on_left/b)
            else:
                Remainder =  (b/a)*B(ones_on_left/b) + (c/a)*B((ones_on_right/c)) 
            Gain = H_current_attr - Remainder
            if (Gain > max):
                max = Gain
                max_index = i
    return max_index
            

'''
Implementation of a node in Decision Tree
'''
class Decision_Tree_Node:
    
    '''
    Contructor of a node
    @param value: the value(or label) of a node, refers to the order number of an attribute( 0 to 37)
    @param curr_depth: the current depth of a node in Decision Tree
    @param depth_limit: depth limit of decision tree
    @param: X_examples, Y_examples: set of examples 
    @param: selected_attributes: a list of boolean values indicating whether an attribute is already selected or not
    @param parent_X_examples, parent_Y_examples: set of examples of the parent node
    '''
    def __init__(self, value, curr_depth, depth_limit, X_examples, Y_examples, selected_attr, parent_X_examples, parent_Y_examples):
        self.value = value
        self.current_depth = curr_depth
        self.depth_limit = depth_limit
        self.X_examples = X_examples
        self.Y_examples = Y_examples
        self.selected_attributes = selected_attr
        self.parent_X_examples = parent_X_examples
        self.parent_Y_examples = parent_Y_examples
        self.left_node = None
        self.right_node = None
        
    def train_by_information_gain(self):
        empty = []
        
        #If the node reaches depth limit, update the value of node and return
        if (self.current_depth == self.depth_limit):
            self.value = plurality_value(self.Y_examples) - 2
            return
        else:
            #if all attributes are empty then return plurality_value(examples)
#            if (no_attributes(self.selected_attributes)):
#                self.value = plurality_value(self.Y_examples) - 2
#                print("96")
#                return
            #r is chosen
            left_X_examples = []
            left_Y_examples = []
            right_X_examples = []
            right_Y_examples = []
            left_selected_attr = self.selected_attributes
            right_selected_attr = self.selected_attributes
            for i in range(0,len(self.X_examples)):
                #count the number of examples that has attribute[r] == 1, then push them in right subtree
                if (self.X_examples[i][self.value] == 1):
                    right_X_examples.append(self.X_examples[i])
                    right_Y_examples.append(self.Y_examples[i])
                #count the number of examples that has attribute[r] == 0, then push them in left subtree
                else:
                    left_X_examples.append(self.X_examples[i])
                    left_Y_examples.append(self.Y_examples[i])
                    
            #Applying on right subtree
            if (not right_X_examples): #if examples are None then return PLURALITY_VALUE(Parents)
                value = plurality_value(self.parent_Y_examples) - 2
                self.right_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, right_selected_attr, self.X_examples, self.Y_examples)
            elif (same_classification(right_Y_examples)): #if all classification are the same, then return PLURALITY_VALUE(examples)
                value = int(right_Y_examples[0]) - 2
                self.right_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, right_selected_attr, self.X_examples, self.Y_examples)
            else:
                #otherwise, create a new subtree, then recursively train the subtree
                r = max_gain(self.X_examples, self.Y_examples, right_selected_attr)
                left_selected_attr[r] = True
                value = r
                self.right_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, right_X_examples, right_Y_examples, right_selected_attr, self.X_examples, self.Y_examples)
                self.right_node.train_by_information_gain()
                
            #Applying on right subtree
            if (not left_X_examples): #if examples are None then return PLURALITY_VALUE(Parents)
                value = plurality_value(self.parent_Y_examples) - 2
                self.left_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, left_selected_attr, self.X_examples, self.Y_examples)
            elif (same_classification(left_Y_examples)):  #if all classification are the same, then return PLURALITY_VALUE(examples)
                value = int(left_Y_examples[0]) - 2
                self.left_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, left_selected_attr, self.X_examples, self.Y_examples)
            else:
                #otherwise, create a new subtree, then recursively train the subtree
                #selecting r using information gain
                r = max_gain(self.X_examples, self.Y_examples, left_selected_attr)
                left_selected_attr[r] = True
                value = r
                self.left_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, left_X_examples, left_Y_examples, left_selected_attr, self.X_examples, self.Y_examples)
                self.left_node.train_by_information_gain()
                
    
    '''
    train_randomly is almost the same as train_by_information_gain, the only difference is randomly selecting the r attribute to classify examples
    '''
    def train_randomly(self):     
        empty = []
        if (self.current_depth >= self.depth_limit):
            self.value = plurality_value(self.Y_examples) - 2
        else:        
            left_X_examples = []
            left_Y_examples = []
            right_X_examples = []
            right_Y_examples = []
            left_selected_attr = self.selected_attributes
            right_selected_attr = self.selected_attributes
            for i in range(0,len(self.X_examples)):
                if (self.X_examples[i][self.value] == 1):
                    right_X_examples.append(self.X_examples[i]) 
                    right_Y_examples.append(self.Y_examples[i])
                else: 
                    left_X_examples.append(self.X_examples[i]) 
                    left_Y_examples.append(self.Y_examples[i])
                    
            if (not right_X_examples): #if examples are None then return PLURALITY_VALUE(Parents)
                value = plurality_value(self.parent_Y_examples) - 2
                self.right_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, right_selected_attr, self.X_examples, self.Y_examples)
            elif (same_classification(right_Y_examples)):
                value = int(right_Y_examples[0]) - 2
                self.right_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, right_selected_attr, self.X_examples, self.Y_examples)
            else:
                #randomly select an attribute r
                if (no_attributes(right_selected_attr)):
                    value = plurality_value(self.Y_examples) - 2
                else:
                    while (True):
                        r = randint(0, 37)
                        if (right_selected_attr[r] == False):
                            right_selected_attr[r] = True
                            value = r
                            break
                self.right_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, right_X_examples, right_Y_examples, right_selected_attr, self.X_examples, self.Y_examples)
                self.right_node.train_randomly()

            if (not left_X_examples): #if examples are None then return PLURALITY_VALUE(Parents)
                value = plurality_value(self.parent_Y_examples) - 2
                self.left_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, left_selected_attr, self.X_examples, self.Y_examples)
            elif (same_classification(left_Y_examples)):
                value = int(left_Y_examples[0]) - 2
                self.left_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, empty, empty, left_selected_attr, self.X_examples, self.Y_examples)
            else:
                #randomly select an attribute r
                if (no_attributes(left_selected_attr)):
                    value = plurality_value(self.Y_examples) - 2
                else:
                    while (True):
                        r = randint(0, 37)
                        if (left_selected_attr[r] == False):
                            left_selected_attr[r] = True
                            value = r
                            break
                self.left_node = Decision_Tree_Node(value, self.current_depth + 1, self.depth_limit, left_X_examples, left_Y_examples, left_selected_attr, self.X_examples, self.Y_examples)
                self.left_node.train_randomly()
            