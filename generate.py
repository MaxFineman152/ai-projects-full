import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # If word not correct length, remove option
        crossword_dict = copy.deepcopy(self.domains)
        for v, words in crossword_dict.items():
            for word in words:
                if len(word) != v.length:
                    self.domains[v].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False

        # Check if any overlaps (or if consistent by default)
        if self.crossword.overlaps[x, y] is None:
            return revision

        revisions = set()
        (i, j) = self.crossword.overlaps[x, y]  # Co-ords of overlapping nodes

        # Check if letter matches for word x and word y
        for x_word in self.domains[x]:
            removal = True
            for y_word in self.domains[y]:
                if list(x_word)[i] == list(y_word)[j]:
                    removal = False
                    break
            # If no possible y word, remove x word
            if removal:
                revisions.add(x_word)
                revision = True

        # Remove x words
        for word in revisions:
            self.domains[x].remove(word)

        return revision  # True if revision has been made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            # Add all arcs
            queue = []
            for v in self.crossword.variables:
                for neighbor in self.crossword.neighbors(v):
                    arc = (v, neighbor)
                    queue.append(arc)

        else:
            # Parameter given arcs
            queue = arcs

        while len(queue) > 0:
            x, y = queue[0]  # Front of queue
            queue.pop(0)  # Remove from queue
            if self.revise(x, y):  # If need to make revisions

                # No options left
                if len(self.domains[x]) == 0:
                    return False
                # Add possible new arcs
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment or assignment[v] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        unique = set()
        for v in assignment:
            word = assignment[v]

            # Check word not used before
            if word in unique:
                return False
            unique.add(word)

            # Check word fits
            if len(word) != v.length:
                return False
            
            # Check nodes are consistent across overlapping words
            for neighbor in self.crossword.neighbors(v):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[v, neighbor]
                    if assignment[v][i] != assignment[neighbor][j]:
                        return False
        return True  

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        new_domain = []
        for word in self.domains[var]:
            count = 0

            # For each neighbor, see how many words are ruled out
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    for comparison in self.domains[neighbor]:
                        if word[i] != comparison[j]:  # If word ruled out
                            count += 1
            new_domain.append((word, count))
        
        # Sort new domain by words that rule out fewest options
        new_domain = sorted(new_domain, key=lambda x: x[1])

        return [word for word, count in new_domain]  # Count no longer needed

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_remaining_value = []
        for v in self.crossword.variables:
            if v not in assignment:
                min_remaining_value.append((v, len(self.domains[v])))

        # Sort by number of remaining values, smallest first
        min_remaining_value = sorted(min_remaining_value, key=lambda x: x[1])

        # Find ties
        least_remaining = min_remaining_value[0][1]
        tie = []
        for (v, count) in min_remaining_value:
            if count == least_remaining:
                tie.append(v)

        # If tie, find most constrained word via degree heuristic
        var = None
        length = 0
        for v in tie:
            if len(self.crossword.neighbors(v)) > length:
                length = len(self.crossword.neighbors(v))
                var = v

        return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If crossword correctly filled, return solution
        if self.assignment_complete(assignment) and self.consistent(assignment):
            return assignment

        # Try assigning new variable
        v = self.select_unassigned_variable(assignment)
        for word in self.domains[v]:
            new_assignment = assignment.copy()
            new_assignment.update({v: word})
            # If not consistent, go to next word
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)  # Iteratively call
                if result != None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
