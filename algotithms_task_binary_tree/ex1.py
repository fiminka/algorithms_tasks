class TreeNode:
    def __init__(self, key, value=1, right=None, left=None, parent=None):
        self.key = key
        self.payload = value
        self.rightChild = right
        self.leftChild = left
        self.parent = parent

    def hasRightChild(self):
        return self.rightChild

    def isRightChild(self):
        return self.parent and (self.parent.rightChild == self)

    def hasLeftChild(self):
        return self.leftChild

    def isLeftChild(self):
        return self.parent and (self.parent.leftChild == self)

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
            else:
                self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent
        elif self is not None:
            if self.isLeftChild():
                self.parent.leftChild = self.rightChild
            else:
                self.parent.rightChild = self.rightChild
            self.rightChild.parent = self.parent

    def findSuccessor(self):
        successor = None
        if self.hasRightChild():
            successor = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    successor = self.parent
                else:
                    self.parent.rightChild = None
                    successor = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return successor

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0
        self.tree_list = []
        self.max_level = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self, key, val=1):
        if not isinstance(val, int):
            raise ValueError('Value must be an positive integer!')
        elif val <= 0:
            raise ValueError('Value must be an positive integer!')
        elif self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, value=val, parent=currentNode)
        elif key == currentNode.key:
            currentNode.payload += val
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, value=val,  parent=currentNode)

    def __setitem__(self, k, v):
        self.put(k, val=v)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                if nodeToRemove.payload > 1:
                    nodeToRemove.payload -= 1
                else:
                    self.remove(nodeToRemove)
                    self.size = self.size-1
            else:
                raise KeyError('Error, key not in the tree')
        elif self.size == 1 and self.root.key == key and self.root.payload == 1:
            self.root = None
            self.size = self.size - 1
        elif self.size == 1 and self.root.key == key and self.root.payload > 1:
            self.root.payload -= 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    def remove(self, currentNode):
        if currentNode.isLeaf():
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else:
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key, currentNode.leftChild.payload,
                                                currentNode.leftChild.leftChild, currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key, currentNode.rightChild.payload,
                                                currentNode.rightChild.leftChild, currentNode.rightChild.rightChild)

    def visual_tree(self, tree_list, count, currentNode):
        if count > self.max_level:
            return
        try:
            tree_list[count]
        except:
            tree_list.append([])
        if currentNode is not None:
            tree_list[count].append(currentNode.key)
            self.visual_tree(tree_list, count + 1, currentNode.leftChild)
            self.visual_tree(tree_list, count + 1, currentNode.rightChild)
        else:
            tree_list[count].append([])
            self.visual_tree(tree_list, count + 1, None)
            self.visual_tree(tree_list, count + 1, None)

    def tree_max_level_checker(self, count, currentNode):
        if currentNode is not None:
            count += 1
            if self.max_level < count:
                self.max_level = count
            self.tree_max_level_checker(count, currentNode.leftChild)
            self.tree_max_level_checker(count, currentNode.rightChild)

    def __str__(self):
        self.tree_max_level_checker(0, self.root)
        self.visual_tree(self.tree_list, 0, self.root)
        x = len(self.tree_list[-2]) * 4
        for i in self.tree_list[:-1]:
            for j in i:
                y = x // (len(i) * 2)
                if not j:
                    j = r' '
                print(" " * (y - 1) + str(j) + " " * y, end='')
            print('')
            print('')
        self.tree_list = []
        self.max_level = 0
        return ''
