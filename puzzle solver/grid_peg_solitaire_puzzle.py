from puzzle import Puzzle
from copy import deepcopy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle
        @rtype: bool
        """
        return type(other) == type(self) and self._marker == other._marker and \
            self._marker_set == other._marker_set

    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle
        self.

        >>> grid = [["*", "*", "*", "*", "*"],["*", "*", "*", "*", "*"],\
        ["*", "*", "*", "*", "*"],["*", "*", ".", "*", "*"],\
        ["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gpsp)
        |*|*|*|*|*|
        |*|*|*|*|*|
        |*|*|*|*|*|
        |*|*|.|*|*|
        |*|*|*|*|*|
        """
        rstring = '|'
        i = 0
        for down in self._marker:
            i += 1
            if i > 1:
                rstring += "\n" + "|"
            for along in down:
                rstring += along + "|"
        return rstring

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @typr self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]
        """

        extensions_list = []

        markers, marker_set = self._marker, self._marker_set

        for i in range(len(markers)):
            for j in range(len(markers[i])):
                if markers[i][j] == "*":
                    # Checking right side
                    if j < len(markers[i]) - 2:
                        # Checking right for peg to jump and if space is empty
                        if markers[i][j+1] == "*" and markers[i][j+2] == ".":
                            board_copy = deepcopy(markers)
                            board_copy[i][j] = "."
                            board_copy[i][j+1] = "."
                            board_copy[i][j+2] = "*"
                            extensions_list.append(GridPegSolitairePuzzle
                                                   (board_copy,
                                                    {"*", ".", "#"}))
                    # Checking left side
                    if j > 1:
                        # Checking left for peg to jump or if space is empty
                        if markers[i][j-1] == "*" and markers[i][j-2] == ".":
                            board_copy = deepcopy(markers)
                            board_copy[i][j] = "."
                            board_copy[i][j-1] = "."
                            board_copy[i][j-2] = "*"
                            extensions_list.append(GridPegSolitairePuzzle
                                                   (board_copy,
                                                    {"*", ".", "#"}))
                    # Checking up
                    if i > 1:
                        # Checking up for peg to jump or if space is empty
                        if markers[i-1][j] == "*" and markers[i-2][j] == ".":
                            board_copy = deepcopy(markers)
                            board_copy[i][j] = "."
                            board_copy[i-1][j] = "."
                            board_copy[i-2][j] = "*"
                            extensions_list.append(GridPegSolitairePuzzle
                                                   (board_copy,
                                                    {"*", ".", "#"}))
                    # Checking down
                    if i < len(markers) - 2:
                        # Checking down for peg to jump and if space is empty
                        if markers[i+1][j] == "*" and markers[i+2][j] == ".":
                            board_copy = deepcopy(markers)
                            board_copy[i][j] = "."
                            board_copy[i+1][j] = "."
                            board_copy[i+2][j] = "*"
                            extensions_list.append(GridPegSolitairePuzzle
                                                   (board_copy,
                                                    {"*", ".", "#"}))

        return extensions_list

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.
        @type self: GridPegSolitairePuzzle
        @rtype: bool
        """
        star_count = 0
        for i in range(len(self._marker)):
            star_count += self._marker[i].count('*')
        return star_count == 1

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
