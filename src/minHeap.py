import sys

from src.DiGraph import DiGraph
from src.Node import Node

"""
classic minHeap class to use in the dijkstra algorithm
"""


class MinHeap:
    def __init__(self, capacity: int, key: int, graph: DiGraph, size: int):
        self.index_of_nodes1 = [0] * size
        self.node_holder1 = [0] * capacity
        # init the src as the min node in the heap with weight 0
        node_temp: Node = (graph.nodes.get(key))
        node_temp.weight = 0
        self.node_holder1[0] = node_temp
        self.heap_size = 0

    # insert the node to the heap
    def insert(self, node: Node):
        self.heap_size += 1
        idx = self.heap_size
        node.weight = sys.maxsize
        self.node_holder1[idx] = node
        self.index_of_nodes1[node.key] = idx
        # put the node at the current index at his place in the heap
        self.heapfyUp(idx)

    # simple heapifyUp
    def heapfyUp(self, pos: int):
        parentIdx = int(pos / 2)
        currentIdx = pos
        # parent_node: Node = self.node_holder.get(parentIdx)
        # current_node: Node = self.node_holder.get(currentIdx)
        while currentIdx > 0 and self.node_holder1[parentIdx].weight > self.node_holder1[currentIdx].weight:
            # //swap the positions
            self.index_of_nodes1[self.node_holder1[currentIdx].key] = parentIdx
            self.index_of_nodes1[self.node_holder1[parentIdx].key] = currentIdx
            self.swap(currentIdx, parentIdx)
            currentIdx = parentIdx
            parentIdx = int(parentIdx / 2)

    # get the node with the minimum weight
    def extractMin(self) -> Node:
        min: Node = self.node_holder1[0]
        lastNode: Node = self.node_holder1[self.heap_size]
        # // update the indexes[] and move the last node to the top
        self.index_of_nodes1[lastNode.key] = 0
        self.node_holder1[0] = lastNode
        self.node_holder1[self.heap_size] = None
        self.sinkDown(0)
        self.heap_size -= 1
        return min

    #  push the node at the current index down
    def sinkDown(self, k: int):
        smallest = k
        leftChildIdx = 2 * k
        rightChildIdx = 2 * k + 1
        #
        if (leftChildIdx < self.heap_size and self.node_holder1[smallest].weight >
                self.node_holder1[leftChildIdx].weight):
            smallest = leftChildIdx
        if (rightChildIdx < self.heap_size and self.node_holder1[smallest].weight >
                self.node_holder1[rightChildIdx].weight):
            smallest = rightChildIdx
        if smallest != k:
            smallestNode: Node = self.node_holder1[smallest]
            kNode: Node = self.node_holder1[k]
            # swap the positions
            self.index_of_nodes1[smallestNode.key] = k
            self.index_of_nodes1[kNode.key] = smallest
            self.swap(k, smallest)
            self.sinkDown(smallest)

    # swap the two nodes
    def swap(self, a: int, b: int):
        temp: Node = self.node_holder1[a]
        self.node_holder1[a] = self.node_holder1[b]
        self.node_holder1[b] = temp

    # check if the heap is empty
    def isEmpty(self) -> bool:
        return self.heap_size == 0

    # return the heapSize
    def heapSize(self) -> int:
        return self.heap_size
