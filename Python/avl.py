""" Module implementing AVL tree """


class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:

    def __init__(self, root):
        self.root = root

    def print_preorder(self, root=0):
        if root == 0:
            root = self.root

        if root:
            print(root.value, end=' ')
            self.print_preorder(root.left)
            self.print_preorder(root.right)

    def insert(self, value, root=0):
        if root == 0:
            root = self.root

        if not root:
            return Node(value)

        elif value < root.value:
            root.left = self.insert(value, root.left)

        else:
            root.right = self.insert(value, root.right)

        # update height
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # get balance factor
        balance_factor = self.balance_factor(root)

        # right left
        if balance_factor < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        # right right
        if balance_factor < -1 and value > root.right.value:
            return self.left_rotate(root)

        # left right
        if balance_factor > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # left left
        if balance_factor > 1 and value < root.left.value:
            return self.right_rotate(root)

        return root

    def delete(self, value, root=0):

        if root == 0:
            root = self.root

        if not root:
            return root

        elif value < root.value:
            root.left = self.delete(value, root.left)

        elif value > root.value:
            root.right = self.delete(value, root.right)

        else:

            if not root.left and not root.right:
                root = None
                return root

            if not root.left:
                temp = root.right
                if root == self.root:
                    self.root = temp
                root = None
                return temp

            elif not root.right:
                temp = root.left
                if root == self.root:
                    self.root = temp
                root = None
                return temp

            else:
                temp = self.get_next_inorder(root.right)
                root.value = temp.value
                root.right = self.delete(temp.value, root.right)

        root.height = 1 + max(self.height(root.left),
                              self.height(root.right))

        balance_factor = self.balance_factor(root)

        # left left
        if balance_factor > 1 and self.balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        # left right
        if balance_factor > 1 and self.balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # right right
        if balance_factor < -1 and self.balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        # right left
        if balance_factor < -1 and self.balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_next_inorder(self, root):
        if not root or not root.left:
            return root

        return self.get_next_inorder(root.left)

    def right_rotate(self, parent):
        child = parent.left
        grand_child = child.right

        parent.left = grand_child
        child.right = parent

        parent.height = 1 + max(self.height(parent.left),
                                self.height(parent.right))
        child.height = 1 + max(self.height(child.left),
                               self.height(child.right))

        if parent == self.root:
            self.root = child

        return child

    def left_rotate(self, parent):
        child = parent.right
        grand_child = child.left

        parent.right = grand_child
        child.left = parent

        parent.height = 1 + max(self.height(parent.left),
                                self.height(parent.right))
        child.height = 1 + max(self.height(child.left),
                               self.height(child.right))

        if parent == self.root:
            self.root = child

        return child

    def height(self, root):
        if not root:
            return 0

        return root.height

    def balance_factor(self, root):
        if not root:
            return 0

        return self.height(root.left) - self.height(root.right)


if __name__ == '__main__':

    start = Node(34)
    avl = AVL(start)

    avl.print_preorder()
    print()

    avl.insert(12)
    avl.insert(39)
    avl.insert(93)
    avl.insert(65)
    avl.insert(48)
    avl.insert(1)
    avl.insert(84)
    avl.insert(3)

    print(avl.print_preorder())
    print()

    avl.delete(39)

    avl.print_preorder()
    print()
