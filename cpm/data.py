class Data:
    def __init__(self, filename: str) -> None:
        self._read_data(filename)

    def _read_data(self, filename: str) -> None:
        with open(filename) as file:
            for n, line in enumerate(file):
                if n == 0:
                    task_count, order_count = line.split(" ")
                    self.task_count = int(task_count)
                    self.order_count = int(order_count)
                if n == 1:
                    raw_times = line.split(" ")
                    raw_times[-1] = raw_times[-1].replace("\n", "")

                    int_times = list(map(int, raw_times))
                    zipped = zip(range(1, len(int_times) + 1), int_times)
                    self.times = {k: v for (k, v) in zipped}

                if n == 2:
                    raw_graph = line.split("  ")
                    raw_graph[-1] = raw_graph[-1].replace("\n", "")

                    self.graph: dict[int, list[int]] = {}
                    all_vertexes = []

                    for dependency in raw_graph:
                        first, second = list(map(int, dependency.split(" ")))
                        all_vertexes.append(first)
                        all_vertexes.append(second)

                        if self.graph.get(first):
                            new_graph = self.graph[first]
                            new_graph.append(second)
                            self.graph[first] = new_graph
                        else:
                            self.graph[first] = [second]

                    self.vertexes = set(all_vertexes)
                    self.full_graph = {}
                    
                    for vertex in self.vertexes:
                        if dependables:=self.graph.get(vertex):
                            self.full_graph[vertex] = dependables
                        else:
                            self.full_graph[vertex] = []

    def __str__(self) -> str:
        return f"""
Tasks: {self.task_count}
Orders: {self.order_count}
Times: {self.times}
Graph:{self.graph}
Full graph: {self.full_graph}
Vertexes: {self.vertexes}
"""