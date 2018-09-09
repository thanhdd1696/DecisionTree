from random import randint
from TreeNode import *
from util import *
import sys

def read_datafile(fname, attribute_data_type = 'integer'):
    inf = open(fname,'r')
    lines = inf.readlines()
    inf.close()
    #--
    X = []
    Y = []
    for l in lines:
        ss=l.strip().split(',')
        temp = []
        for s in ss:
            if attribute_data_type == 'integer':
                temp.append(int(s))
            elif attribute_data_type == 'string':
                temp.append(s)
            else:
                print("Unknown data type");
                exit();
        X.append(temp[:-1])
        Y.append(int(temp[-1]))
    return X, Y

        
class DecisionTree :
    def __init__(self, split_random, depth_limit, X_train, Y_train, curr_depth = 0, default_label = 1):
        self.split_random = split_random # if True splits randomly, otherwise splits based on information gain 
        self.depth_limit = depth_limit
        empty_example = []
        selected_attributes = [False] * 38
        if (split_random):
            root_value = randint(0,37)
            selected_attributes[root_value] = True
        else:
            root_value = max_gain(X_train, Y_train, selected_attributes)
            selected_attributes[root_value] = True
        #root is a Decision_Tree_Node, implemented in TreeNode.py
        self.root = Decision_Tree_Node(root_value, curr_depth, depth_limit, X_train, Y_train, selected_attributes, empty_example, empty_example) 
        
    def train(self):
        if (self.split_random):
            self.root.train_randomly()
        else:
            self.root.train_by_information_gain()
        
    def predict(self, X_train):
        r = self.root
        v = r.value
        while (v >= 0):
            if (X_train[v] == 1):        
                v = r.right_node.value
                r = r.right_node
            else:
                v = r.left_node.value
                r = r.left_node
        return (v+2)
            

#===	   
def compute_accuracy(dt_classifier, X_test, Y_test):
    numRight = 0
    for i in range(len(Y_test)):
        x = X_test[i]
        y = Y_test[i]
        if y == dt_classifier.predict(x) :
            numRight += 1
    return (numRight*1.0)/len(Y_test)

#==============================================
#==============================================
test_file = sys.argv[4]
output_file = sys.argv[5]
depth_limit = int(sys.argv[3])

X_train, Y_train = read_datafile('train.txt')
X_test, Y_test = read_datafile('test.txt')
fo = open(output_file, "w")
if (sys.argv[2] == 'R'):
	split_random = True
	#if split_random then execute 100 times
	for i in range(0,100):
		myTree = DecisionTree(split_random, depth_limit, X_train, Y_train)
		myTree.train()
		result = compute_accuracy(myTree, X_test, Y_test)
		print(result)
		fo.writelines(str(result) + '\n')
else:
	split_random = False
	myTree = DecisionTree(split_random, depth_limit, X_train, Y_train)
	myTree.train()
	result = compute_accuracy(myTree, X_test, Y_test)
	print(result)
	fo.writelines(str(result) + '\n')

fo.close()

