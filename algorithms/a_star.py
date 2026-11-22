
import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            goal_index = tile - 1

            row, col = divmod(index, 3)
            goal_row, goal_col = divmod(goal_index, 3)

            distance += abs(row - goal_row) + abs(col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        queue = []
        counter = 0

        heapq.heappush(queue, (self.heuristic(initial), counter, initial))
        best_cost = {initial: initial.cost}

        expanded = 0
        generated = 1
        max_frontier = 1

        while queue:
            _, _, current = heapq.heappop(queue)

            if current.cost > best_cost[current]:
                continue

            if current.is_goal:
                return SearchResult(current, expanded, generated, max_frontier, current.cost)

            expanded += 1

            for neighbor in current.neighbors():
                if neighbor not in best_cost or neighbor.cost < best_cost[neighbor]:
                    best_cost[neighbor] = neighbor.cost
                    counter += 1

                    priority = neighbor.cost + self.heuristic(neighbor)
                    heapq.heappush(queue, (priority, counter, neighbor))
                    generated += 1

            max_frontier = max(max_frontier, len(queue))

        return SearchResult(None, expanded, generated, max_frontier, 0)
