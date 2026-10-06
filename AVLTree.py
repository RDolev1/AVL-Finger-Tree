"""A class representing a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        # Complexity: O(1)
        return self.key is not None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        #Complexity: O(1)
        self.root = None
        self.max = None #updated during each function (regular/finger insert, join, split, delete)
        self.Tree_size = 0 #updated during each function mentioned above except split (not required)

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key):
        #Complexity: O(log(n))
        x = self.root
        e = 0

        if self.root is None:
            return None, 1

        while x is not None and x.is_real_node():
            e += 1
            if key == x.key:                        ##check if key was reached
                return x,e
            elif key < x.key:                       ##check if in left subtree
                x = x.left
            else:                                   ##if not left/found, go to right subtree
                x = x.right

        return None, e

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def finger_search(self, key):
        #Complexity: O(log(d)), where d is the number of elements between the maximum and the key.
        curr = self.max
        e = 0

        if self.root is None:                               #Edgescases: Empty Tree OR Key larger than max
            return None, 1
        if key > self.max.key:
            return None, 1

        while curr.parent is not None:                      ## check if we hit root
            e += 1
            if key == curr.key: return curr, e
            elif key > curr.key:                            ##check if we overshoot nodes
                break
            curr = curr.parent

        while curr.is_real_node():
            e += 1
            if key == curr.key:                             ##check if key was reached
                return curr,e
            elif key < curr.key:                             ##check if in left subtree
                curr = curr.left
            else:                                           ##if not left/found, go to right subtree
                curr = curr.right

        return None, e

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def insert(self, key, val):
        #Complexity: O(log(n))
        ##General variables
        node = AVLNode(key, val)                             ##initialize key, val fields
        node.left = AVLNode(None, None)             ##initialize fake children -> left and right fields
        node.right = AVLNode(None, None)
        parent_node = None
        curr = self.root
        edges = 0
        self.Tree_size += 1                                 ##Update size

        ##Update/Create Max field
        if self.max is None:
            self.max = node
        elif self.max.key < node.key:
            self.max = node

        ##General BST insert
        while curr is not None and curr.is_real_node():
            edges += 1
            parent_node = curr
            if node.key < curr.key:                     ##Check key according to current key and move accordingly
                curr = curr.left
            else: curr = curr.right

        node.parent = parent_node                       ##initialize parent field

        if parent_node is None:                         ##Check parent for child assignment
            self.root = node
        elif node.key < parent_node.key:
            parent_node.left = node
        else:
            parent_node.right = node

        self.update_height(node)

        promote = self.rebalance(parent_node)

        return node, edges, promote

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def finger_insert(self, key, val):
        #Complexity: O(log(n))
        ##General variables
        node = AVLNode(key, val)                        ##initialize key, val fields
        node.left = AVLNode(None, None)        ##initialize fake children -> left and right fields
        node.right = AVLNode(None, None)
        node.height = 0
        parent_node = None
        curr = self.max
        edges = 0
        self.Tree_size += 1                             ##Update size

        ##Edgecase - Empty Tree:
        if self.root is None:
            self.root = node
            self.max = node
            return node, 1, 0

        ##Edgecase - New Max:
        if key > self.max.key:
            old_max = self.max
            old_max.right = node
            node.parent = old_max
            self.max = node
            promote = self.rebalance(old_max)
            return node, 1, promote

        ##General BST finger insert
        while curr.parent is not None:                  ## check if we hit root
            if key > curr.key:                          ##check if we overshoot nodes
                break
            curr = curr.parent
            edges += 1

        while curr.is_real_node():                     ## check if we hit leaf
            edges += 1
            parent_node = curr
            if key < curr.key:                        ##check if in left subtree
                curr = curr.left
            else:
                curr = curr.right

        node.parent = parent_node                    ##initialize parent field

        if key < parent_node.key:                   ##Check parent for child assignment
            parent_node.left = node
        else:
            parent_node.right = node

        self.update_height(node)

        promote = self.rebalance(parent_node)

        return node, edges, promote

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        #Complexity: O(log(n))
        self.Tree_size -= 1                                                             ##Update size
        if self.Tree_size == 0 or self.max is None or self.root is None:                ##Edgecase 1: Tree becomes empty
            self.max = None
            self.root = None
            return

        if self.max.key == node.key:                                                    ##Edgecase 2: Delete Max
            new_max = self.predecessor(node)
            self.max = new_max
            child = node.left
            parent = node.parent
            if parent is not None:                                                     ##Check parent for root problems
                if parent.right == node:
                    parent.right = child
                else:
                    parent.left = child

                child.parent = parent
                self.rebalance(parent)
            else:
                self.root = child
                child.parent = None
            return

        if  not node.right.is_real_node() and not node.left.is_real_node():                         ##Case 1
            new_node = AVLNode(None, None)
            if node.parent.left == node:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
                new_node.parent = node.parent

            new_node.parent = node.parent
            self.rebalance(node.parent)

        elif not node.right.is_real_node() or not node.left.is_real_node():                        ##Case 2
            child = node.left if node.left.is_real_node() else node.right
            parent = node.parent
            if parent is not None:
                if parent.left == node:
                    parent.left = child
                else:
                    parent.right = child
                child.parent = parent
                self.rebalance(parent)
            else:
                self.root = child
                child.parent = None

        else:                                                                                    ##Case 3
            successor = self.successor(node)
            succ_right = successor.right
            succ_parent = successor.parent
            if succ_parent == node:                                            ##check if the successor is a right child
                balance_start_node = successor
            else:
                balance_start_node = succ_parent

            if succ_parent != node:
                if succ_parent.left == successor:
                    succ_parent.left = succ_right
                else:
                    succ_parent.right = succ_right

                if succ_right is not None and succ_right.is_real_node():
                    succ_right.parent = succ_parent

            successor.height = node.height
            successor.parent = node.parent

            if node.parent is None:                                                ##Edgecase 3: delete node is the root
                self.root = successor
            elif node == node.parent.left:                                         ##Continue by case 3 algorithm
                node.parent.left = successor
            else:
                node.parent.right = successor

            successor.left = node.left
            successor.left.parent = successor

            if successor == node.right:                                           ##Realign pointers
                successor.right = succ_right
                if successor.right is not None:
                    successor.right.parent = successor
            else:
                successor.right = node.right
                successor.right.parent = successor
            self.rebalance(balance_start_node)
        return

    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """

    def join(self, tree2, key, val):
        #Complexity: O(|height(self)-height(tree2)| + 1) where height(self) is tree.root.height
        if self.Tree_size == 0:                             ##Edgecase 1: one or both trees are empty
            if tree2.Tree_size != 0:
                self.root = tree2.root
                self.max = tree2.max
                self.Tree_size = tree2.Tree_size
            self.insert(key, val)
            return
        elif tree2.Tree_size == 0:
            self.insert(key, val)
            return

        mid_node = AVLNode(key, val)
        h1 = self.root.height
        h2 = tree2.root.height
        self.Tree_size += 1 + tree2.Tree_size

        if tree2.max.key > self.max.key:                                    ##fix max pointer in self
            self.max = tree2.max

        def join_left(t1_node, node, t2_node):
            # Input: 2 subtrees and a connecting node
            # Output: combined subtree
            # Function: implementing the join algorithm under the assumption "t1_node.height<t2_node.height"
            # Complexity: O(|height(self)-height(tree2)| + 1)

            while t2_node.is_real_node() and t2_node.height > t1_node.height:  ##walk down the left spine till t1 height is reached
                t2_node = t2_node.left

            node.parent = t2_node.parent
            if t2_node.parent is None:
                self.root = node
            else: t2_node.parent.left = node

            node.right = t2_node
            t2_node.parent = node
            node.left = t1_node
            t1_node.parent = node

            self.rebalance(node)
            return

        def join_right(t1_node, node, t2_node):
            # Input: 2 subtrees and a connecting node
            # Output: combined subtree
            # Function: implementing the join algorithm under the assumption "t1_node.height>t2_node.height"
            # Complexity: O(|height(self)-height(tree2)| + 1)

            while t2_node.is_real_node() and t2_node.height > t1_node.height:  ##walk down the right spine till t1 height is reached
                t2_node = t2_node.right

            node.parent = t2_node.parent
            if t2_node.parent is None:
                self.root = node
            else: t2_node.parent.right = node
            node.left = t2_node
            t2_node.parent = node
            node.right = t1_node
            t1_node.parent = node

            self.rebalance(node)
            return

        ##Assign the correct join function by tree order according to key and height
        if self.root.key < tree2.root.key:
            if h1 > h2:
                join_right(tree2.root, mid_node, self.root)
            else:
                join_left(self.root, mid_node, tree2.root)
        else:
            if h1 < h2:
                join_right(self.root, mid_node, tree2.root)
            else:
                join_left(tree2.root, mid_node, self.root)

        return

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, node):
        #Complexity: O(log(n))
        if self.Tree_size == 1:     ##Edgecase 1: root only Tree (smallest option by instructions in this function)
            return AVLTree(),AVLTree()

        og_max = self.max

        ##Define AVLTrees for the output
        t1 = AVLTree()
        t2 = AVLTree()

        ##Check for virtual nodes before assigning pointers
        if node.left.is_real_node():
            t1.root = node.left
            t1.root.parent = None
            t1.max = t1.Max(t1.root) ##Max won't change in this subtree (this max is the largest key in the original tree)
            t1.Tree_size = 1

        if node.right.is_real_node():
            t2.root = node.right
            t2.root.parent = None
            t2.max = t2.Max(t2.root) ##Temporary max to avoid pointer issues
            t2.Tree_size = 1

        curr = node

        ##Travel up the tree and add subtrees to t1/t2 according to relation to node
        while curr.parent is not None:
            parent = curr.parent
            key = parent.key
            val = parent.value
            temp_tree = AVLTree()


            if parent.right == curr:
                if parent.left.is_real_node():
                    ##Update temp_tree pointers to avoid errors in join
                    temp_tree.root = parent.left
                    temp_tree.root.parent = None
                    temp_tree.max = temp_tree.root
                    temp_tree.Tree_size = 1

                t1.join(temp_tree, key, val)
            else:
                if parent.right.is_real_node():
                    ##Update temp_tree pointers to avoid errors in join
                    temp_tree.root = parent.right
                    temp_tree.root.parent = None
                    temp_tree.max = temp_tree.root
                    temp_tree.Tree_size = 1

                t2.join(temp_tree, key, val)

            curr = parent

        ##Assign the max regardless of what happened during Travel up the tree
        if t2.root is not None:
            t2.max = og_max

        return t1, t2

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        # Complexity: O(n)
        ordered_array = []
        root = self.root

        ##General in_order recursive algorithm
        def in_order(node,lst):
            if node is not None and node.is_real_node():
                in_order(node.left,lst)
                lst.append((node.key,node.value))
                in_order(node.right, lst)

            return lst

        return in_order(root,ordered_array)

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self):
        #Complexity: O(1)
        #Bypass function by creating a max field, check for edge case only
        if self.root is None: return None
        return self.max

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        #Complexity: O(1)
        # Bypass function by creating a size field
        return self.Tree_size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        #Complexity: O(1)
        return self.root

    def update_height(self, node):
        # Input: node pointer
        # Output: none
        # Function: used children's height to update node's height. updated during insert with virtual node height of -1
        # so that each child will ALWAYS have a height field
        # Complexity: O(1)

        if node is None:
            return

        left_h = node.left.height
        right_h = node.right.height

        node.height = 1 + max(left_h, right_h)
        return

    def get_bf(self, node):
        # Input: node pointer
        # Output: height difference - balance factor
        # Function: used children's height to determine node's balance factor.
        # Complexity: O(1)

        return node.left.height - node.right.height

    def rebalance(self, curr_node):
        # Input: node pointer
        # Output: promote - number of height changes according to instructions
        # Function: checks if bf was broken and if height was changed.
        # if bf was broken - calls do rotation, if not but height changed - go up one node. in neither - break
        # Complexity: O(log(n))
        promote = 0
        while curr_node is not None:
            bf = self.get_bf(curr_node)  ##Step 3.1
            temp_height = curr_node.height
            self.update_height(curr_node)
            curr_height = curr_node.height
            if abs(bf) < 2 and temp_height == curr_height:  ##Step 3.2
                break
            elif abs(bf) < 2 and temp_height != curr_height:  ##Step 3.3
                promote += 1
                curr_node = curr_node.parent
            else:
                self.do_rotation(curr_node, bf)  ##Step 3.4
                if curr_node.parent is not None:
                    curr_node = curr_node.parent.parent ##Handles the case where the parent moves as well
                else:
                    curr_node = None
        return promote

    def do_rotation(self, node, bf):
        # Input: node pointer, balance factor(number)
        # Output: None
        # Function: assigns which rotation should be applied according to the algorithm studied in class
        # Complexity: O(1)

        if bf > 1:
            if self.get_bf(node.left) == -1:
                self.rotate_left(node.left)
                self.rotate_right(node)

            elif self.get_bf(node.left) == 1 or self.get_bf(node.left) == 0:
                self.rotate_right(node)

        elif bf < -1:
            if self.get_bf(node.right) == -1 or self.get_bf(node.right) == 0:
                self.rotate_left(node)

            elif self.get_bf(node.right) == 1:
                self.rotate_right(node.right)
                self.rotate_left(node)

        return

    def rotate_right(self, node):
        # Input: node pointer
        # Output: None
        # Function: does the right rotation according to the algorithm studied
        # Complexity: O(1)

        B = node
        A = node.left
        B.left = A.right
        B.left.parent = B
        A.right = B
        A.parent = B.parent

        if A.parent is not None:
            if A.parent.left == B:                      ##check if B is a left or right child or root
                A.parent.left = A
            else:
                A.parent.right = A
        else:
            self.root = A

        B.parent = A

        self.update_height(B)
        self.update_height(A)
        return

    def rotate_left(self, node):
        # Input: node pointer
        # Output: None
        # Function: does the left rotation according to the algorithm studied
        # Complexity: O(1)

        B = node
        A = node.right
        B.right = A.left
        B.right.parent = B
        A.left = B
        A.parent = B.parent

        if A.parent is not None:
            if A.parent.left == B:                      ##check if B is a left or right child or root
                A.parent.left = A
            else:
                A.parent.right = A
        else:
            self.root = A

        B.parent = A

        self.update_height(B)
        self.update_height(A)
        return

    def Min(self, node):
        # Input: node pointer
        # Output: pointer to the min node
        # Function: finds the node with the smallest key in the subtree
        # Complexity: O(log(n))

        while node.left is not None and node.left.is_real_node():
            node = node.left
        return node

    def Max(self, node):
        # Input: node pointer
        # Output: pointer to the max node
        # Function: finds the node with the largest key in the subtree
        # Complexity: O(log(n))

        while node.right is not None and node.right.is_real_node():
            node = node.right
        return node

    def successor(self, node):
        # Input: node pointer
        # Output: pointer to the successor of node
        # Function: Travels up the tree searching for the smallest node larger than the pointer key
        # Complexity: O(log(n))

        if node.right is not None and node.right.is_real_node():
            return self.Min(node.right)
        curr = node.parent
        while curr is not None and node == curr.right:
            node = curr
            curr = node.parent
        return curr

    def predecessor(self, node):
        # Input: node pointer
        # Output: pointer to the successor of node
        # Function: Travels up the tree searching for the largest node smaller than the pointer key
        # Complexity: O(log(n))

        if node.left is not None and node.left.is_real_node():
            return self.Max(node.left)
        curr = node.parent
        while curr is not None and node == curr.left:
            node = curr
            curr = node.parent
        return curr