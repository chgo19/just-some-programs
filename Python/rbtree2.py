""" Better Red Black Tree Implementation """

DOUBLEBLACK = 'DB'
BLACK = 'B'
RED = 'R'


class Node:
    def __init__(self, value):
        self.value = value
        self.color = RED
        self.parent = None
        self.left = None
        self.right = None


class RBT:
    def __init__(self):
        self.root = None

    def preorder(self, root=0):
        if root == 0:
            root = self.root
        if root:
            print("{0} {1}".format(root.value, root.color), end=' ')
            self.preorder(root.left)
            self.preorder(root.right)

    def inorder(self, root=0):
        if root == 0:
            root = self.root
        if root:
            self.inorder(root.left)
            print("{0} {1}".format(root.value, root.color), end=' ')
            self.inorder(root.right)

    def postorder(self, root=0):
        if root == 0:
            root = self.root
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print("{0} {1}".format(root.value, root.color), end=' ')

    def normal_bst_insert(self, x, root):
        if not self.root:
            self.root = x
            return

        while root:
            if x.value < root.value:
                if root.left:
                    root = root.left
                else:
                    root.left = x
                    x.parent = root
                    return
            elif x.value > root.value:
                if root.right:
                    root = root.right
                else:
                    root.right = x
                    x.parent = root
                    return

    def left_rotate(self, root):
        child = root.right
        grand_child = child.left

        if root.parent:
            if root == root.parent.left:
                root.parent.left = child
            else:
                root.parent.right = child
        child.parent = root.parent
        root.parent = child
        root.right = grand_child
        if grand_child:
            grand_child.parent = root
        child.left = root

        if root == self.root:
            self.root = child

    def right_rotate(self, root):
        child = root.left
        grand_child = child.right

        if root.parent:
            if root == root.parent.left:
                root.parent.left = child
            else:
                root.parent.right = child
        child.parent = root.parent
        root.parent = child
        root.left = grand_child
        if grand_child:
            grand_child.parent = root
        child.right = root

        if root == self.root:
            self.root = child

    def insert(self, value):
        x = Node(value)
        self.normal_bst_insert(x, self.root)

        while x != self.root and x.parent.color != BLACK:
            p = x.parent
            if p == p.parent.left:
                u = p.parent.right
                if u and u.color == RED:
                    p.color = u.color = BLACK
                    p.parent.color = RED
                    x = p.parent
                else:
                    if x == p.left:
                        p.color = BLACK
                        p.parent.color = RED
                        self.right_rotate(p.parent)
                    else:
                        self.left_rotate(p)
                        x.color = BLACK
                        x.parent.color = RED
                        self.right_rotate(x.parent)
            else:
                u = p.parent.left
                if u and u.color == RED:
                    p.color = u.color = BLACK
                    p.parent.color = RED
                    x = p.parent
                else:
                    if x == p.right:
                        p.color = BLACK
                        p.parent.color = RED
                        self.left_rotate(p.parent)
                    else:
                        self.right_rotate(p)
                        x.color = BLACK
                        x.parent.color = RED
                        self.left_rotate(x.parent)

        self.root.color = BLACK

    def get_bst_node(self, value, root):
        if value < root.value:
            return self.get_bst_node(value, root.left)
        elif value > root.value:
            return self.get_bst_node(value, root.right)
        else:
            if not root.left or not root.right:
                return root
            else:
                temp = root.right
                while temp.left:
                    temp = temp.left
                root.value = temp.value
                return temp

    def free_node(self, v):
        v.left = v.right = v.parent = None

    def case1(self, v):
        # if v is red
        node = v.left if v.left else v.right

        if v == v.parent.left:
            v.parent.left = node
        else:
            v.parent.right = node

        if node:
            node.parent = v.parent

        self.free_node(v)

    def case2(self, v):
        # if u is RED
        node = v.left if v.left else v.right

        if v == v.parent.left:
            v.parent.left = node
        else:
            v.parent.right = node

        node.parent = v.parent
        node.color = BLACK

        self.free_node(v)

    def case3(self, v):
        # if u and v both are black
        node = Node(None)
        if v.left:
            node = v.left
        elif v.right:
            node = v.right

        if v == v.parent.left:
            v.parent.left = node
        else:
            v.parent.right = node

        node.parent = v.parent
        node.color = DOUBLEBLACK

        self.free_node(v)
        return node

    def get_sibling(self, u):
        if u == u.parent.left:
            return u.parent.right
        else:
            return u.parent.left

    def case4(self, u):
        # s is black and atleast one child of s is red
        if u == u.parent.left:
            s = u.parent.right

            # right right
            if s.right and s.right.color == RED:
                u.color = BLACK
                s.right.color = s.parent.color
                self.left_rotate(u.parent)

            # right left
            else:
                u.color = BLACK
                if s.parent.color == BLACK:
                    s.left.color = BLACK
                else:
                    s.parent.color = BLACK
                self.right_rotate(s)
                self.left_rotate(u.parent)

            if not u.value:
                u.parent.left = None
                self.free_node(u)
        else:
            s = u.parent.left

            # left left
            if s.left and s.left.color == RED:
                u.color = BLACK
                s.left.color = s.parent.color
                self.right_rotate(u.parent)

            # left right
            else:
                u.color = BLACK
                if s.parent.color == BLACK:
                    s.right.color = BLACK
                else:
                    s.parent.color = BLACK
                self.left_rotate(s)
                self.right_rotate(u.parent)

            if not u.value:
                u.parent.right = None
                self.free_node(u)

    def case5(self, u):
        # both children of s are black
        s = self.get_sibling(u)
        p = u.parent
        s.color = RED
        u.color = BLACK
        if p.color == RED:
            p.color = BLACK
        else:
            p.color = DOUBLEBLACK

        if not u.value:
            if u == u.parent.left:
                u.parent.left = None
            else:
                u.parent.right = None

            self.free_node(u)

        return p

    def case6(self, u):
        # s is red
        s = self.get_sibling(u)
        s.color = BLACK
        u.parent.color = RED

        if u == u.parent.left:
            self.left_rotate(u.parent)
        else:
            self.right_rotate(u.parent)

        return u

    def remove(self, value):
        v = self.get_bst_node(value, self.root)

        if v == self.root:
            if not v.left and not v.right:
                self.root = None
                self.free_node(v)
                return

        # if v is red
        if v.color == RED:
            self.case1(v)

        # if u is red
        elif v.right and v.right.color == RED:
            self.case2(v)
        elif v.left and v.left.color == RED:
            self.case2(v)

        # if v and u both are black
        else:
            u = self.case3(v)

            while u != self.root and u.color == DOUBLEBLACK:
                s = self.get_sibling(u)

                # if sibling(s) is black
                if s.color == BLACK:

                    # if s has atleast one red child
                    if s.left and s.left.color == RED:
                        self.case4(u)
                        return
                    elif s.right and s.right.color == RED:
                        self.case4(u)
                        return

                    # if both children of s are black
                    else:
                        u = self.case5(u)

                # if s is red
                else:
                    u = self.case6(u)

            # if u is root simply make it black
            self.root.color = BLACK


if __name__ == "__main__":
    rbt = RBT()

    nq = int(input())

    for _ in range(nq):
        op, val = input().split()
        if op == 'i':
            rbt.insert(int(val))
        else:
            rbt.remove(int(val))

    rbt.preorder()
    print()
    rbt.inorder()
    print()
    rbt.postorder()
    print()
