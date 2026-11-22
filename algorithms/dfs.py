
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        stack = [initial]
        visited = {}

        expanded = 0
        generated = 1
        max_frontier = 1

        while stack:
            current = stack.pop()

            if current in visited and visited[current] <= current.cost:
                continue

            visited[current] = current.cost

            if current.is_goal:
                return SearchResult(current, expanded, generated, max_frontier, current.cost)

            if current.cost >= self.depth_limit:
                continue

            expanded += 1

            for neighbor in current.neighbors():
                if neighbor not in visited or neighbor.cost < visited[neighbor]:
                    stack.append(neighbor)
                    generated += 1

            max_frontier = max(max_frontier, len(stack))

        return SearchResult(None, expanded, generated, max_frontier, 0)
