class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class BinaryTree:
    def __init__(self, key, parent=None):
        self.key = key
        self.leftChild = None
        self.rightChild = None
        self.parent = parent

    def insertLeft(self, newNode):
        if self.leftChild is None:
            self.leftChild = BinaryTree(newNode, parent=self)
        else:
            t = BinaryTree(newNode, parent=self.key)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode):
        if self.rightChild is None:
            self.rightChild = BinaryTree(newNode, parent=self)
        else:
            t = BinaryTree(newNode, parent=self)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key


class TreeVisualization:
    def __init__(self, rootObj):
        self.root = rootObj
        self.tree_list = []
        self.tree_max_level = 1

    def visual_tree(self, tree_list, count, currentNode):
        if count > self.tree_max_level:
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
            if self.tree_max_level < count:
                self.tree_max_level = count
            self.tree_max_level_checker(count, currentNode.leftChild)
            self.tree_max_level_checker(count, currentNode.rightChild)

    def __str__(self):
        self.tree_max_level_checker(0, self.root)
        self.visual_tree(self.tree_list, 0, self.root)
        x = len(self.tree_list[-2]) * 5
        if self.tree_max_level > 5:
            x = len(self.tree_list[-2]) * 3
        for i in self.tree_list[:-1]:
            for j in i:
                if len(str(j)) == 1:
                    j = ' ' + str(j) + ' '
                elif len(str(j)) == 2:
                    j = str(j) + ' '
                y = x // (len(i) * 2)
                if j == '[] ' or j == '':
                    j = r'   '
                print(" " * (y - 1) + str(j) + " " * y, end='')
            print('')
            print('')
        self.tree_list = []
        return ''


def create_list(fplist: str):
    alist = []
    while len(fplist) != 0:
        if fplist[:3] in ['sin', 'cos', 'exp']:
            alist.append(fplist[:3])
            fplist = fplist[3:]
        elif 'ln' in fplist[:2]:
            alist.append(fplist[:2])
            fplist = fplist[2:]
        else:
            alist.append(fplist[0])
            fplist = fplist[1:]
    return alist


def buildParseTree(fpexp: str, unknown='x'):
    fplist = create_list(fpexp)
    # print(fplist)
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in ['+', '-', '*', '^', '/', ')', 'cos', 'sin', 'ln', 'exp', unknown]:
            currentTree.setRootVal(int(i))
            parent = pStack.pop()
            currentTree = parent
        elif i == unknown:
            currentTree.setRootVal(i)
            parent = pStack.pop()
            currentTree = parent
        elif i == '-':
            if currentTree.getLeftChild() is None:
                currentTree.setRootVal(i)
                currentTree.insertLeft('')
                currentTree = currentTree.getLeftChild()
            else:
                currentTree.setRootVal(i)
                currentTree.insertRight('')
                pStack.push(currentTree)
                currentTree = currentTree.getRightChild()
        elif i in ['+', '*', '/', '^']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i in ['cos', 'sin', 'ln', 'exp']:
            currentTree.setRootVal(i)
            currentTree.insertLeft('')
            currentTree = currentTree.getLeftChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError
    return eTree


def unpacking_Tree_First(ulist, parseTree, parent=None):
    if parseTree is not None:
        if parseTree.getRightChild() is None and parseTree.getLeftChild():
            ulist.append(parseTree.getRootVal())
            unpacking_Tree_First(ulist, parseTree.getLeftChild(), parseTree)
        else:
            if parseTree.getRootVal() in ['+', '*', '/', '^', '-']:
                ulist.append('(')
            unpacking_Tree_First(ulist, parseTree.getLeftChild(), parseTree)
            ulist.append(parseTree.getRootVal())
            if parent is not None:
                if parent.getRightChild() == parseTree and parseTree.getRightChild() is None:
                    ulist.append(')')
                elif parent.getRightChild() is None and parseTree.getLeftChild() is None:
                    ulist.append(')')
            unpacking_Tree_First(ulist, parseTree.getRightChild(), parseTree)
    while '' in ulist:
        ulist.remove('')
    return ulist


def unpacking_Tree(parseTree):
    current = parseTree
    dlist = unpacking_Tree_First([], parseTree, parent=None)
    while current.rightChild is not None:
        if current.rightChild.rightChild is not None:
            dlist.append(')')
        current = current.rightChild
    return dlist


def finding_number(alist, unknown):
    for i in range(len(alist)):
        if alist[i] == unknown:
            if len(alist) == 1:
                return [str(unknown)]
            if i > 4:
                if alist[i - 3] == '/' and alist[i-1] == '*':
                    return [alist[i-4], '/', alist[i-2]]
            elif i > 1:
                if alist[i - 1] == '*':
                    return [alist[i - 2]]
            if i < len(alist) - 2:
                if alist[i + 1] == '*':
                    return [alist[i + 2]]
            if i < len(alist) - 2:
                if alist[i + 1] == '/':
                    return ['1', '/', alist[i + 2]]
            if (alist[i-1] and alist[i+1]) not in ['*', '/']:
                return None


def derivative_from_list(ulist, unknown):
    print('Given function to differentiate:')
    print(''.join(map(str, ulist)))
    prepare_list = []
    der_list = []
    x = len(ulist)
    i = 0
    while i < x:
        if ulist[i] in ['cos', 'sin', 'ln', 'exp'] or (ulist[i] == '^' and ulist[i-1] != unknown):
            if ulist[i + 1] == '(':
                j = i + 1
                help_list = ['(']
                while help_list:
                    if j == i + 1:
                        j += 1
                    if ulist[j] == '(':
                        help_list.append('(')
                    elif ulist[j] == ')':
                        help_list.pop()
                    j += 1
                prepare_list.append(ulist[i])
                prepare_list.append(ulist[i + 1:j])
                i = j
            else:
                prepare_list.append(ulist[i])
                prepare_list.append([ulist[i+1]])
                i += 2
        else:
            prepare_list.append(ulist[i])
            i += 1
    # print(prepare_list)
    i = 0
    while i < len(prepare_list):
        if prepare_list[i] in ['cos', 'sin', 'ln', 'exp', '^', '*'] and isinstance(prepare_list[i+1], list):
            if unknown in prepare_list[i + 1]:
                if prepare_list[i] == 'cos':
                    der_list.append('-')
                    der_list.append('(')
                    if finding_number(prepare_list[i + 1], unknown) is not None:
                        for j in finding_number(prepare_list[i + 1], unknown):
                            der_list.append(j)
                        der_list.append('*')
                    der_list.append('sin')
                    for j in prepare_list[i + 1]:
                        der_list.append(j)
                    der_list.append(')')
                elif prepare_list[i] == 'sin':
                    der_list.append('(')
                    if finding_number(prepare_list[i + 1], unknown) is not None:
                        for j in finding_number(prepare_list[i + 1], unknown):
                            der_list.append(j)
                        der_list.append('*')
                    der_list.append('cos')
                    for j in prepare_list[i + 1]:
                        der_list.append(j)
                    der_list.append(')')
                elif prepare_list[i] == 'ln':
                    if len(prepare_list[i + 1]) != 1:
                        # print(prepare_list[i+1])
                        der_list.append('(')
                        der_list.append('1')
                        der_list.append('/')
                        der_list.append(''.join(map(str, prepare_list[i+1])))
                        der_list.append(')')
                        if finding_number(prepare_list[i + 1], unknown) is not None:
                            der_list.append(')')
                    else:
                        der_list.append('(')
                        der_list.append('1')
                        der_list.append('/')
                        der_list.append(str(prepare_list[i]))
                        der_list.append(')')
                elif prepare_list[i] == 'exp':
                    der_list.append('(')
                    der_list.append(''.join(map(str, derivative_from_list(prepare_list[i+1], unknown))))
                    der_list.append('*')
                    der_list.append('(')
                    der_list.append('exp')
                    der_list.append(''.join(map(str, prepare_list[i+1])))
                    der_list.append(')')
                    der_list.append(')')
                elif prepare_list[i] == '^':
                    if isinstance(prepare_list[i+1], list):
                        if len(prepare_list[i+1]):
                            der_list.append('(')
                            der_list.append(prepare_list[i-1])
                            der_list.append('^')
                            for j in prepare_list[i + 1]:
                                der_list.append(j)
                            der_list.append(')')
                            der_list.append('*')
                            der_list.append('(')
                            der_list.append('ln')
                            der_list.append(prepare_list[i-1])
                            der_list.append(')')
            i += 2
        elif prepare_list[i] == str(unknown):
            if i < len(prepare_list):
                if prepare_list[i + 1] == '^':
                    der_list.append(prepare_list[i + 2])
                    der_list.append('*')
                    if int(prepare_list[i+2]-1) != 1:
                        der_list.append('(')
                        der_list.append(str(unknown))
                        der_list.append('^')
                        der_list.append(int(prepare_list[i + 2]) - 1)
                        der_list.append(')')
                    else:
                        der_list.append(str(unknown))
                elif prepare_list[i + 1] == "*":
                    der_list.append(prepare_list[i + 2])
                elif prepare_list[i - 1] == "*":
                    der_list.append(prepare_list[i - 2])
                else:
                    der_list.append('1')
            else:
                der_list.append('1')
            i += 1
        elif prepare_list[i] == '(':
            stack = ['(']
            j = i + 1
            while stack:
                # print(prepare_list[j], stack)
                if prepare_list[j] == '(':
                    stack.append('(')
                elif prepare_list[j] == ')':
                    stack.pop()
                j += 1
            slices = prepare_list[i:j]
            # print(slices)
            if unknown not in slices:
                der_list.append('(')
                der_list.append(eval(''. join(str(k) for k in slices)))
                der_list.append(')')
                i = j + 1
            else:
                der_list.append('(')
            i += 1
        elif prepare_list[i] in ['(', ')', '+', '-']:
            der_list.append(prepare_list[i])
            i += 1
        else:
            i += 1
    # print(der_list)
    return der_list


def clearing_derivative(dlist):
    i = 0
    while i < len(dlist):
        if dlist[i] == '-' and dlist[i + 1] == '-' and dlist[i-1] != '(':
            dlist[i:i+2] = '+'
        elif dlist[i] == '-' and dlist[i + 1] == '-':
            dlist[i:i+2] = ''
        if dlist[i] == '^' and dlist[i + 1] == 1:
            dlist[i:i+2] = ''
        if dlist[i] == '(':
            j = i + 1
            while dlist[j] != ')':
                j = j + 1
            k = j - 1
            while dlist[k] != '(':
                k -= 1
            x = dlist[k + 1: j]
            if not x:
                dlist[k: j + 1] = ''
            elif len(x) < 3:
                if '+' in x:
                    x.remove('+')
                    dlist[k: j + 1] = x
                else:
                    dlist[k: j + 1] = x
        i += 1
    i = 0
    while i < len(dlist) - 1:
        if dlist[i] in ['+', '*', '/', '^'] and (dlist[i - 1] != ')' or dlist[i + 1] != '('):
            if dlist[i - 1] in ['(', ')'] and dlist[i+1] in ['(', ')']:
                dlist[i] = ''
                dlist.remove('')
        i += 1
    print('Counted derivative:')
    print(''.join(map(str, dlist[1:-1])))
    return dlist


def derivative_Tree(parseTree, unknown='x'):
    x = unpacking_Tree(parseTree)
    x = derivative_from_list(x, unknown)
    x = clearing_derivative(x)
    for i in range(len(x)):
        x[i] = str(x[i])
    x = ''.join(x)
    x = buildParseTree(x, unknown)
    x = TreeVisualization(x)
    print(x)
    return ''


print(derivative_Tree(buildParseTree('((n^2)+n)', 'n'), 'n'))
