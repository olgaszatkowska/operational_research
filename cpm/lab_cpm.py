from collections import deque

from dataclasses import dataclass

from data import Data


@dataclass
class CriticalPathDto:
    path: list[int]
    length: float
    early_start: list[int, float]
    early_finish: list[int, float]
    late_start: list[int, float]
    late_finish: list[int, float]


class CriticalPath:
    @classmethod
    def _get_indegree(cls, graph: dict[int, list[int]]) -> dict[int, int]:
        indegree = {node: 0 for node in graph}

        for node in graph:
            for neighbor in graph[node]:
                indegree[neighbor] += 1

        return indegree

    @classmethod
    def sort_topologically(cls, graph: dict[int, list[int]]) -> list[int]:
        """
        Sorts graph in topological order.

        The resuling sequence are nodes in order when each vertex
        never comes before its predecessors.
        """
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
    def critical_path(cls, data: Data) -> CriticalPathDto:
        graph = data.full_graph
        durations = data.times

        topo_order = cls.sort_topologically(graph)

        distance = {node: float("-inf") for node in graph}
        predecessors = {node: None for node in graph}
        early_start = {node: 0 for node in graph}
        early_finish = {node: 0 for node in graph}

        for node in topo_order:
            if not any(node in neighbors for neighbors in graph.values()):
                distance[node] = 0

        for node in topo_order:
            if distance[node] != float("-inf"):
                for neighbor in graph[node]:
                    early_start[neighbor] = max(
                        early_start[neighbor], early_finish[node]
                    )
                    early_finish[neighbor] = early_start[neighbor] + durations[neighbor]

                    if distance[neighbor] < distance[node] + durations[neighbor]:
                        distance[neighbor] = distance[node] + durations[neighbor]
                        predecessors[neighbor] = node

        end_node = max(distance, key=distance.get)
        critical_path_length = distance[end_node]

        critical_path = []
        while end_node:
            critical_path.append(end_node)
            end_node = predecessors[end_node]
        critical_path.reverse()

        late_finish = {node: float("inf") for node in graph}
        late_start = {node: float("inf") for node in graph}

        for node in reversed(topo_order):
            if not graph[node]:
                late_finish[node] = early_finish[node]
            late_start[node] = late_finish[node] - durations[node]

            for neighbor in graph[node]:
                late_finish[node] = min(late_finish[node], late_start[neighbor])
                late_start[node] = late_finish[node] - durations[node]

        return CriticalPathDto(
            path=critical_path,
            length=critical_path_length,
            early_start=early_start,
            early_finish=early_finish,
            late_start=late_start,
            late_finish=late_finish,
        )
