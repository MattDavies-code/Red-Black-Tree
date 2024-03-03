
# File:     red_black.py
# Author:   John Longley
# Date:     October 2022

# Template file for Inf2-IADS (2022-23) Coursework 1, Part B
# Implementation of dictionaries by red-black trees: space-saving version

# Provided code:

Red, Black = True, False

def colourStr(c):
    return 'R' if c==Red else 'B'

Left, Right = 0, 1

def opposite(branch):
    return 1 - branch

branchLabels = ['l','r'] # = [0,1] Changed according to email

class Node():
    
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.colour = Red
        self.left = None
        self.right = None
        
    def getChild(self,branch):
        if branch==Left:
            return self.left
        else:
            return self.right

    def setChild(self,branch,y):
        if branch==Left:
            self.left = y
        else:
            self.right = y

    def __repr__(self):
        return str(self.key) +':'+ str(self.value) +':'+ colourStr(self.colour)

# Use None for all trivial leaf nodes

def colourOf(x):
    if x is None:
        return Black
    else:
        return x.colour


class RedBlackTree():

    def __init__ (self):
        self.root = None
        self.stack = []


# TODO: Task 1.
    def lookupHelper(self,root,key):
        if root == None:
            return None
        if root.key == key:
            return root.value       
        elif key < root.key:
            return root.lookupHelper(root.left,key) #Go left
        else:                 
            return root.lookupHelper(root.right,key) #Go right

    def lookup(self,key):
        return self.lookupHelper(self.root,key)

# TODO: Task 2.
    def plainInsertHelper(self,root,key,value):
        if root.key == key:
            root.value = value #Replace value if key is already present
            self.stack.append(root)
        elif key < root.key:
            if root.left == None:
                root.left = Node(key,value) #Create node to left of parent
                self.stack.append(root)
                self.stack.append(0)
                self.stack.append(root.left) #Add new Node to stack
            else:
                self.stack.append(root)
                self.stack.append(0)
                self.plainInsertHelper(root.left,key,value) #Go Left
        else:
            if root.right == None:
                root.right = Node(key,value) #Create node to right of parent
                self.stack.append(root)
                self.stack.append(1)
                self.stack.append(root.right) #Add new Node to stack
            else:
                self.stack.append(root)
                self.stack.append(1)
                self.plainInsertHelper(root.right,key,value) #Go right

    def plainInsert(self,key,value):
        if self.root == None:
            self.root = Node(key,value) #Create new tree
            self.stack.append(self.root) #Add new Node to stack
        else:
            return self.plainInsertHelper(self.root,key,value)

# TODO: Task 3.
    def tryRedUncle(self):
        if len(self.stack) < 5: #3 nodes + 2 branches needed for grandad, parent and child
            return False
        child = self.stack[-1]
        parent = self.stack[-3]
        grandfather = self.stack[-5]
        uncle = Node.getChild(grandfather,opposite(self.stack[-4])) #Get child of Grandfather, using opposite branch to parent
        if uncle == None: #Checks if uncle node exists
            return False
        if (colourOf(child) == Red) and (colourOf(parent) == Red) and (colourOf(uncle) == Red): #check if self & parent & uncle node is red
            grandfather.colour = Red
            parent.colour = Black
            uncle.colour = Black
            self.stack.pop(-1) #pop parent and child
            self.stack.pop(-1) 
            self.stack.pop(-1) 
            self.stack.pop(-1) 
            return True
        else:   
            return False

    def repeatRedUncle(self):
        while self.tryRedUncle()==True:
            self.tryRedUncle()
        
# Provided code to support Task 4:

    def toNextBlackLevel(self,node):
        # inspect subtree down to the next level of blacks
        # and return list of components (subtrees or nodes) in L-to-R order
        # (in cases of interest there will be 7 components A,a,B,b,C,c,D).
        if colourOf(node.left)==Black:  # node.left may be None
            leftHalf = [node.left]
        else:
            leftHalf = self.toNextBlackLevel(node.left)
        if colourOf(node.right)==Black:
            rightHalf = [node.right]
        else:
            rightHalf = self.toNextBlackLevel(node.right)
        return leftHalf + [node] + rightHalf

    def balancedTree(self,comps):
        # build a new (balanced) subtree from list of 7 components
        [A,a,B,b,C,c,D] = comps
        a.colour = Red
        a.left = A
        a.right = B
        c.colour = Red
        c.left = C
        c.right = D
        b.colour = Black
        b.left = a
        b.right = c
        return b


# TODO: Task 4.
    def endgame(self):
        #endgame 1: Tree is legal
        #endgame 2: Red pushed to root
        if self.root.colour == Red:
            self.root.colour = Black
        #endgame 3: Replace 'black with 4 nearest black children' with balanced tree
        elif len(self.stack) >= 5:
            if self.stack[-1].colour == Red and self.stack[-3].colour == Red:
                if self.stack[-5] == self.root: #If no great grandfather exists to attach subtree to
                    subTree = self.balancedTree(self.toNextBlackLevel(self.stack[-5]))
                    self.root = subTree
                else: 
                    subTreeBranch = self.stack[-6] #Branch to root of subtree
                    subTree = self.balancedTree(self.toNextBlackLevel(self.stack[-5])) #Takes grandfather as parameter
                    if subTreeBranch == 0:
                        self.stack[-7].left = subTree
                    elif subTreeBranch == 1:
                        self.stack[-7].right = subTree
      
    def insert(self,key,value):
        self.stack = [] #clears stack
        self.plainInsert(key,value)
        self.repeatRedUncle()
        self.endgame()

# Provided code:

    # Printing tree contents
    
    def __str__(self,x):
        if x==None:
            return 'None:B'
        else:
            leftStr = '[ ' + self.__str__(x.left) + ' ] '
            rightStr = ' [ ' + self.__str__(x.right) + ' ]'
            return leftStr + x.__str__() + rightStr

    def __repr__(self):
        return self.__str__(self.root)

    def showStack(self):
        return [x.__str__() if isinstance(x,Node) else branchLabels[x]
                for x in self.stack]

    # All keys by left-to-right traversal
    
    def keysLtoR_(self,x):
        if x==None:
            return []
        else:
            return self.keysLtoR_(x.left) + [x.key] + self.keysLtoR_(x.right)

    def keysLtoR(self):
        return self.keysLtoR_(self.root)

# End of class RedBlackTree


# Creating a tree by hand:

sampleTree = RedBlackTree()
sampleTree.root = Node(2,'two')
sampleTree.root.colour = Black
sampleTree.root.left = Node(1,'one')
sampleTree.root.left.colour = Black
sampleTree.root.right = Node(4,'four')
sampleTree.root.right.colour = Red
sampleTree.root.right.left = Node(3,'three')
sampleTree.root.right.left.colour = Black
sampleTree.root.right.right = Node(6,'six')
sampleTree.root.right.right.colour = Black

# For fun: sorting algorithm using trees
# Will remove duplicates

def TreeSort(L):
    T = RedBlackTree()
    for x in L:
        T.insert(x,None)
    return T.keysLtoR()

# End of file
