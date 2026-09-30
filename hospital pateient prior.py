# Experiment 3 : Hospital Patient-Priority and Record Organization System
# Part A/B : BST and AVL tree keyed by Patient ID  |  Part C : Max-Heap for emergency triage

class Record:                                    # one patient record = one tree node
    def __init__(self, pid, name):
        self.pid, self.name = pid, name
        self.left = self.right = None
        self.h = 1                               # height of the subtree rooted here

def height(n):
    return n.h if n else 0

def fix(n):                                      # recompute height of node n
    n.h = 1 + max(height(n.left), height(n.right))

def bf(n):                                       # balance factor = left height - right height
    return height(n.left) - height(n.right) if n else 0

# ---------------- Binary Search Tree ----------------
def bst_insert(root, pid, name):
    if root is None:
        return Record(pid, name)
    if pid < root.pid:
        root.left = bst_insert(root.left, pid, name)
    elif pid > root.pid:
        root.right = bst_insert(root.right, pid, name)
    fix(root)
    return root

def search(root, pid):                           # works for both BST and AVL
    path = []
    while root:
        path.append(root.pid)
        if pid == root.pid:
            return root, path
        root = root.left if pid < root.pid else root.right
    return None, path

def inorder(n):   return inorder(n.left) + [n.pid] + inorder(n.right) if n else []
def preorder(n):  return [n.pid] + preorder(n.left) + preorder(n.right) if n else []
def postorder(n): return postorder(n.left) + postorder(n.right) + [n.pid] if n else []
def nodes(n):     return nodes(n.left) + [n] + nodes(n.right) if n else []

# ---------------- AVL Tree ----------------
def rotate_right(y):                             # fixes LL imbalance
    x = y.left
    y.left, x.right = x.right, y
    fix(y); fix(x)
    return x

def rotate_left(x):                              # fixes RR imbalance
    y = x.right
    x.right, y.left = y.left, x
    fix(x); fix(y)
    return y

def avl_insert(root, pid, name, log):
    if root is None:
        return Record(pid, name)
    if pid < root.pid:
        root.left = avl_insert(root.left, pid, name, log)
    elif pid > root.pid:
        root.right = avl_insert(root.right, pid, name, log)
    fix(root)
    b = bf(root)
    head = f"insert {pid}: node {root.pid} BF={b:+d} -> "
    if b > 1 and bf(root.left) >= 0:             # LL case
        log.append(head + "LL, right rotation")
        return rotate_right(root)
    if b > 1:                                    # LR case
        log.append(head + f"LR, left({root.left.pid}) then right({root.pid})")
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if b < -1 and bf(root.right) <= 0:           # RR case
        log.append(head + "RR, left rotation")
        return rotate_left(root)
    if b < -1:                                   # RL case
        log.append(head + f"RL, right({root.right.pid}) then left({root.pid})")
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root

# ---------------- Max-Heap (triage) ----------------
class TriageHeap:                                # highest severity is treated first
    def __init__(self):
        self.a = []                              # list of (severity, name)

    def push(self, sev, name):
        self.a.append((sev, name))
        i = len(self.a) - 1
        while i > 0 and self.a[(i - 1) // 2][0] < self.a[i][0]:    # bubble up
            p = (i - 1) // 2
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def pop(self):
        top, last = self.a[0], self.a.pop()
        if self.a:
            self.a[0] = last
            i, n = 0, len(self.a)
            while True:                                            # sift down
                big = i
                for c in (2 * i + 1, 2 * i + 2):
                    if c < n and self.a[c][0] > self.a[big][0]:
                        big = c
                if big == i:
                    break
                self.a[i], self.a[big] = self.a[big], self.a[i]
                i = big
        return top

    def show(self):
        return [s for s, _ in self.a]

# ---------------- Main program ----------------
if __name__ == "__main__":
    records = [(120, "Anitha"), (140, "Balaji"), (160, "Charan"), (130, "Divya"),
               (125, "Ezhil"), (110, "Farook"), (115, "Geetha")]

    print("=== 1. BST (key = Patient ID) ===")
    root = None
    for pid, nm in records:
        root = bst_insert(root, pid, nm)
    print("Inorder   :", inorder(root))
    print("Preorder  :", preorder(root))
    print("Postorder :", postorder(root))
    print("Height    :", height(root), "| Root BF:", bf(root))
    for key in (125, 999):
        node, path = search(root, key)
        print(f"Search {key}:", f"found {node.name}" if node else "not found",
              f"| path {path} | {len(path)} comparisons")

    print("\n=== 2. AVL tree (same records) ===")
    log, avl = [], None
    for pid, nm in records:
        avl = avl_insert(avl, pid, nm, log)
    for line in log:
        print(line)
    print("Preorder  :", preorder(avl))
    print("Height    :", height(avl))
    print("BF inorder:", [(n.pid, bf(n)) for n in nodes(avl)])
    node, path = search(avl, 125)
    print(f"Search 125: found {node.name} | path {path} | {len(path)} comparison")
    b = a = None
    for k in range(101, 108):                    # IDs issued in increasing order
        b, a = bst_insert(b, k, "x"), avl_insert(a, k, "x", [])
    print("IDs 101..107 in order -> BST height", height(b), "| AVL height", height(a))

    print("\n=== 3. Max-Heap (severity 1-10) ===")
    patients = [("Kiraht", 6), ("Maideen", 4), ("Panjavarnam", 9),
                ("Pandi", 7), ("Veeramani", 8), ("Basha", 3)]
    heap = TriageHeap()
    for nm, sev in patients:
        heap.push(sev, nm)
        print(f"Arrive {nm:<6} sev {sev} -> heap {heap.show()}")
    while heap.a:
        sev, nm = heap.pop()
        print(f"Treat  {nm:<6} sev {sev} -> heap {heap.show()}")