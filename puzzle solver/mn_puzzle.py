from puzzle import Puzzle

# helper functions:


def de_tuple(double_tuple):
    """
    creates a nested list version of the nested tuples
    @param double_tuple: tuple[tuple[str]] -> current tuple grid
    @rtype: List[List[str]]
    """
    listed_tuple = []
    for down in range(len(double_tuple)):
        mini_list = []
        for along in double_tuple[down]:
            mini_list.append(along)
        listed_tuple.append(mini_list)
    return listed_tuple


def re_tuple(nested_list):
    """
    creates a tuple of tuples out of a nested list
    @param nested_list: List[List[str]]
    @rtype: tuple[tuple[str]]
    """
    outer_tuple = ()
    mini_list = []
    for inner_list in nested_list:
        mini_list.append(tuple(inner_list))
        outer_tuple = tuple(mini_list)
    return outer_tuple


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle
        @rtype: bool
        """
        return type(other) == type(self) and self.n == other.n and \
            self.m == other.m and \
            self.from_grid == other.from_grid and self.to_grid == other.to_grid

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.
        >>> s = MNPuzzle((("1", "2", "3"), ("4", "5", "*"), ("6", "7", "8")), \
            (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "*")))
        >>> print(s)
        |1|2|3|
        |4|5|*|
        |6|7|8|
        >>> s = MNPuzzle((("*", "2", "3"), ("1", "4", "5")), (("1", "2", "3"),\
        ("4", "5", "*")))
        >>> print(s)
        |*|2|3|
        |1|4|5|
        """
        rstring = '|'
        for down in range(self.n):
            if down > 0:
                rstring += "\n" + "|"
            for along in range(self.m):
                rstring += (str(self.from_grid[down][along]) + "|")
        return rstring

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @typr self: MNPuzzle
        @rtype: list[MNPuzzle]
        """
        extension_list = []

        # from the empty tile:
        # check a direction
        # make it a list and look it an index
        # try nested lists, call a helper to de-tuple and retuple before you
        # add the mn puzzle to the extensions list
        maingrid = de_tuple(self.from_grid)

        # all I need is the index of the list its in (i) and its index in
        # that list(k)
        for j in range(len(maingrid)):         # this gives the depth
            if '*' in maingrid[j]:
                k = maingrid[j].index('*')
                i = j

        # checking for empty square.
        # now checking for other squares on the sides
        # moving the right:
        if k < len(maingrid[i])-1:
            grid = de_tuple(self.from_grid)
            grid[i][k] = grid[i][k+1]
            grid[i][k+1] = '*'
            extension_list.append(MNPuzzle(re_tuple(grid), self.to_grid))
        # moving to the left:
        if k > 0:
            grid = de_tuple(self.from_grid)
            grid[i][k] = grid[i][k-1]
            grid[i][k-1] = '*'
            extension_list.append(MNPuzzle(re_tuple(grid), self.to_grid))
        # moving up:
        if i > 0:
            grid = de_tuple(self.from_grid)
            grid[i][k] = grid[i-1][k]
            grid[i-1][k] = "*"
            extension_list.append(MNPuzzle(re_tuple(grid), self.to_grid))
        # moving down:
        if i < len(maingrid)-1:
            grid = de_tuple(self.from_grid)
            grid[i][k] = grid[i+1][k]
            grid[i+1][k] = "*"
            extension_list.append(MNPuzzle(re_tuple(grid), self.to_grid))

        return extension_list

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool
        """
        return self.from_grid == self.to_grid

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3", '4'), ("5", "6", "7", "*"),)
    start_grid = (("4", "1", "6", "7"), ("3", "*", "2", "5"),)
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
