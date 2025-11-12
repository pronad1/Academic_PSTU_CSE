# BFS (Breadth-First Search) Explained in Bangla

## BFS কী?
BFS (Breadth-First Search) একটি গ্রাফ ট্রাভার্সাল অ্যালগরিদম, যা প্রথমে কাছের নোডগুলো ঘুরে দেখে এবং পরে দূরের নোডগুলোতে যায়। এটি সাধারণত কিউ (queue) ব্যবহার করে।

## কোডের ব্যাখ্যা

```python
from collections import deque
```
- collections লাইব্রেরি থেকে deque (ডাবল-এন্ডেড কিউ) ইমপোর্ট করা হয়েছে।

```python
def bfs_shortest_path(graph, start, goal):
```
- bfs_shortest_path নামে একটি ফাংশন, যেখানে graph, start, goal প্যারামিটার নেয়।

```python
    visited = set()
```
- ভিজিট করা নোডগুলো রাখার জন্য একটি সেট।

```python
    queue = deque([[start]])
```
- queue-তে প্রথমে শুধু start নোডের পথ রাখা হয়েছে।

```python
    while queue:
```
- queue-তে যতক্ষণ আইটেম আছে, লুপ চলবে।

```python
        path = queue.popleft()
```
- queue থেকে প্রথম পথটি বের করা হচ্ছে।

```python
        node = path[-1]
```
- path-এর শেষ নোডটি node-এ রাখা হচ্ছে।

```python
        if node == goal:
            return path
```
- যদি node গন্তব্য হয়, তাহলে সেই path রিটার্ন করা হবে।

```python
        if node not in visited:
            visited.add(node)
```
- যদি node আগে ভিজিট না হয়, তাহলে সেটিকে visited-এ যোগ করা হচ্ছে।

```python
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
```
- node-এর প্রতিটি neighbor-এর জন্য:
    - path-এর কপি new_path-এ রাখা হচ্ছে।
    - neighbor-কে new_path-এ যোগ করা হচ্ছে।
    - new_path-কে queue-তে যোগ করা হচ্ছে।

```python
    return None
```
- কোনো পথ না পাওয়া গেলে None রিটার্ন করা হচ্ছে।

## গ্রাফের উদাহরণ

```python
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
```
- একটি গ্রাফ ডিকশনারি আকারে তৈরি করা হয়েছে।

## রান করার নিয়ম

```python
print(bfs_shortest_path(graph, 'A', 'F'))
```
- A থেকে F পর্যন্ত সবচেয়ে ছোট পথটি প্রিন্ট করা হচ্ছে।

## BFS-এর বৈশিষ্ট্য
- BFS সর্বদা সবচেয়ে ছোট পথ খুঁজে পায় (যদি ওজন না থাকে)।
- কিউ ব্যবহার করে নোডগুলো ট্র্যাক করে।
- গ্রাফ বা ট্রি ট্রাভার্সাল, পথ খোঁজা, সংযোগ খোঁজা ইত্যাদিতে ব্যবহৃত হয়।

---

**লেখক:** GitHub Copilot
