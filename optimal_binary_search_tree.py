# Author: Karthik Reddy Pagilla

import copy
import sys
import math
from collections import deque

class Node:
    def __init__(self, key, probability):
        self.key = key
        self.probability = float(probability)

    def __lt__(self, other):
        return self.probability < other.probability

class Tree:
    def __init__(self, probability, key=None, right=None, left=None):
        self.right = right
        self.left = left
        self.key = key
        self.probability = probability
    
    def toString(self):
        print("Key: " + str(self.key))
        print("Probability: " + str(self.probability))
        if self.left != None:
            print("Left: " + self.left.key)
        else:
            print("Left: None")
        if self.right != None:
            print("Right: " + self.right.key)
        else:
            print("Right: None")

def cost_root_tree_generator(nodes):
    n = len(nodes) - 1
    cost_table = [['   ']*(n+1) for i in range(n+2)]
    root_table = [['   ']*(n+1) for i in range(n+1)]

    for i in range(1, n + 1):
        cost_table[i][i - 1] = 0.00
        cost_table[i][i] = nodes[i].probability
        root_table[i][i] = i
    cost_table[n + 1][n] = 0.00

    for d in range(1, n):
        for i in range(1, n - d + 1):
            j = d + i
            min = 99999
            probability_sum = 0
            for l in range(i, j + 1):
                q = cost_table[i][l - 1] + cost_table[l + 1][j]
                if q < min:
                    min = q
                    root_table[i][j] = l
                if min == 99999 and q == min:
                    root_table[i][j] = l
                probability_sum += nodes[l].probability
            cost_table[i][j] = round(min + probability_sum, 3)

    return [cost_table, root_table]

def generate_tree(roots, nodes):
    n = len(nodes) - 1
    tree_root = Tree(key=nodes[roots[1][n]].key, probability=nodes[roots[1][n]].probability)
    stack = deque()
    stack.append((tree_root, 1, n))

    while len(stack) > 0:
        (u, i, j) = stack.pop()
        l = roots[i][j]
        if l < j:
            v = Tree(key=nodes[roots[l + 1][j]].key, probability=nodes[roots[l + 1][j]].probability)
            u.right = v
            stack.append((v, l+1, j))
        if i < l:
            v = Tree(key=nodes[roots[i][l - 1]].key, probability=nodes[roots[i][l - 1]].probability)
            u.left = v
            stack.append((v, i, l-1))

    return tree_root

def preorder_traversal(root):
 
    if root:
        root.toString()
        print()
        
        preorder_traversal(root.left)

        preorder_traversal(root.right)

# Reading the input file
input_file = open(sys.argv[1], 'r')

input_file = open('/content/input', 'r')

n = int(input_file.readline().strip())

line = input_file.readline().split(" ")
nodes = []

while len(line) != 0 and line[0] != '':
    key = line[0]
    probability = line[1].rstrip()
    nodes.append(Node(key, probability))
    line = input_file.readline().split(" ")

nodes.sort(key=lambda x:x.key)
nodes.insert(0, '---')

input_file.close()

result = cost_root_tree_generator(nodes)

print("Cost Table:")
print()
for i in result[0][1:]:
    print("[ ", end="")
    for j in i[0:]:
        if j == '   ':
            print("{:^10}".format(j), end="")
        else:
            print("{:^10}".format(format(j,".3f")), end="")
    print(" ]")
print()

print("Root Table:")
print()
for i in result[1][1:]:
    print("[", end="")
    for j in i[1:]:
        if j == '   ':
            print("{:^12}".format(j), end="")
        else:
            print("{:^12}".format(str(j) + " (" + str(nodes[int(j)].key) + ")"), end="")
    print("  ]")
print()

root = generate_tree(result[1], nodes)

preorder_traversal(root)