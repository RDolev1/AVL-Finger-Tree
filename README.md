# Advanced AVL Tree

A robust, dynamic implementation of an AVL Tree in Python, featuring advanced tree manipulations and optimized search mechanics.

## 🚀 Features

* **Standard BST Operations:** Efficient `insert`, `delete`, and `search` functionality with automatic AVL rebalancing.
* **Finger Search & Insert:** Optimized `finger_search` and `finger_insert` operations that begin traversal from the maximum node, significantly improving performance when accessing elements close to the maximum value.
* **Tree Join:** The `join(tree2, key, val)` operation dynamically merges two separate AVL trees around a separating key while maintaining the AVL balance property.
* **Tree Split:** The `split(node)` operation divides an existing AVL tree into two separate valid AVL trees (keys smaller than the node, and keys larger).
* **Array Conversion:** Includes an in-order traversal method (`avl_to_array`) to export the tree structure to a sorted Python list.

## ⏱️ Time Complexities

| Operation | Time Complexity | Description |
| :--- | :--- | :--- |
| `search(key)` | O(log n) | Standard top-down search. |
| `finger_search(key)` | O(log d) | Search starting from the max node (d = elements between max and target). |
| `insert(key, val)` | O(log n) | Insertion with automatic height updates and rebalancing. |
| `finger_insert(key, val)` | O(log n) | Insertion starting from the max node. |
| `delete(node)` | O(log n) | Node removal with successor/predecessor replacement. |
| `join(tree2, key, val)` | O(abs(h1 - h2) + 1) | Merges two trees (h1, h2 are the heights of the respective trees). |
| `split(node)` | O(log n) | Splits the tree into two separate trees around the given node. |

## 🛠️ Implementation Details

* **Language:** Python 3
* **Virtual Leaves:** Utilizes virtual nodes (`None` keys) for all leaves. This structural choice simplifies the implementation of tree rotations and rebalancing logic by ensuring every real node always has two children.
* **Balance Factor Tracking:** The tree actively calculates balance factors and tracks the number of `promote` cases (height changes) during AVL rebalancing for theoretical performance analysis.

## 👥 Authors

* Roy Dolev
* Ofir Sher
