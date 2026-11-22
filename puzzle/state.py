
from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        children = []
        position = self.blank_index
        row, col = divmod(position, 3)

        moves = [
            (-1, 0, "up"),
            (1, 0, "down"),
            (0, -1, "left"),
            (0, 1, "right")
        ]

        for dr, dc, action in moves:
            new_row = row + dr
            new_col = col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_position = new_row * 3 + new_col
                new_tiles = list(self.tiles)

                new_tiles[position], new_tiles[new_position] = new_tiles[new_position], new_tiles[position]

                child = State(tuple(new_tiles), self, action, self.cost + 1)
                children.append(child)

        return children

    def path(self) -> List["State"]:
        path = []
        current = self

        while current is not None:
            path.append(current)
            current = current.parent

        path.reverse()
        return path

    def actions(self) -> List[str]:
        return [state.action for state in self.path() if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
