class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        if value < self.value:
            if self.left is None:
                self.left = Node(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = Node(value)
            else:
                self.right.insert(value)

    def inorder_traversal(self, result):
        if self.left:
            self.left.inorder_traversal(result)
        result.append(self.value)
        if self.right:
            self.right.inorder_traversal(result)


def tree_sort(arr):
    if len(arr) == 0:
        return arr
    root = Node(arr[0])
    for item in arr[1:]:
        root.insert(item)
    result = []
    root.inorder_traversal(result)
    return result
