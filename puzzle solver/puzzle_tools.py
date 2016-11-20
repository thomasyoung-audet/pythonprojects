"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """

    visited = set()
    stack = deque()

    puzzle_node = PuzzleNode(puzzle)
    stack.append(puzzle_node)

    while stack:
        current_node = stack.pop()

        if str(current_node) not in visited:
            if current_node.puzzle.is_solved():
                while current_node.parent:
                    current_node.parent.children.append(current_node)
                    current_node = current_node.parent

                return current_node

            elif not current_node.puzzle.fail_fast():
                stack.extend([PuzzleNode(i, parent=current_node) for i in
                              current_node.puzzle.extensions()])

            visited.add(str(current_node))
        else:
            pass

# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    visited = set()
    stack = deque()

    puzzle_node = PuzzleNode(puzzle)
    stack.append(puzzle_node)

    while stack:
        current_node = stack.popleft()

        if str(current_node) not in visited:
            if current_node.puzzle.is_solved():
                while current_node.parent:
                    current_node.parent.children.append(current_node)
                    current_node = current_node.parent

                return current_node

            elif not current_node.puzzle.fail_fast():
                stack.extend([PuzzleNode(i, parent=current_node) for i in
                              current_node.puzzle.extensions()])

            visited.add(str(current_node))
        else:
            pass


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle, "\n".join([str(x) for x in self.children]))
