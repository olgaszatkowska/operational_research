from collections import deque

from dataclasses import dataclass


@dataclass
class CriticalPathDto():
    path: list[int]
    length: float


class CriticalPath():
    @classmethod
    def _get_indegree(graph: dict[int,list[int]]) -> dict[int, int]:
        indegree = {node: 0 for node in graph}

        for node in graph:
            for neighbor in graph[node]:
                indegree[neighbor] += 1
                
        return indegree

    @classmethod
    def sort_topologically(cls, graph: dict[int,list[int]]) -> list[int]:
        '''
        Sorts graph in topological order.
        
        The resuling sequence are nodes in order when each vertex
        never comes before its predecessors.
        '''
        indegree = cls._get_indegree(graph)

        zero_indegree_queue = deque([node for node in graph if indegree[node] == 0])

        topo_order = []

        while zero_indegree_queue:
            current = zero_indegree_queue.popleft()
            topo_order.append(current)
            for neighbor in graph[current]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    zero_indegree_queue.append(neighbor)

        return topo_order


    @classmethod
    def find_critical_path_fixed(cls, graph: dict[int,list[int]]) -> tuple[list, float]:
        topo_order = cls.sort_topologically(graph)
        distance = {node: float("-inf") for node in graph}
        predecessors = {node: None for node in graph}

        for node in topo_order:
            if not any(
                node in neighbors for neighbors in graph.values()
            ):
                distance[node] = 0

        for node in topo_order:
            if distance[node] != float("-inf"):
                for neighbor in graph[node]:
                    if distance[neighbor] < distance[node] + 1:
                        distance[neighbor] = distance[node] + 1
                        predecessors[neighbor] = node

        end_node = max(distance, key=distance.get)
        critical_path_length = distance[end_node]

        critical_path = []
        while end_node:
            critical_path.append(end_node)
            end_node = predecessors[end_node]

        critical_path.reverse()

        return CriticalPathDto(path=critical_path, length=critical_path_length) 
    