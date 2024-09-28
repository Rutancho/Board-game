#    Main Author(s): Jaehyuk Heo , Wilgard Fils-aime
#    Main Reviewer(s):Ziyang Wang

from partC import Queue

def get_overflow_list(grid):
    row = len(grid)
    col = len(grid[0])
    over_list = []
    
    for i in range(row):
        for j in range(col):
            
            count = 0
            
            if i > 0:
                count += 1
                
            if i < row -1:
                count += 1
            
            if j > 0:
                count += 1
                
            if j < col -1:
                count += 1
                
            if abs(grid[i][j]) >= count:
                over_list.append((i, j))
        
    if not over_list:
        return None
    
    return over_list



def overflow(grid, a_queue):
    def difference(grid):
        first_positive = None
        first_negative = None

        for row in grid:
            for cell in row:
                if cell > 0:
                    if first_positive is None:
                        first_positive = True
                elif cell < 0:
                    if first_negative is None:
                        first_negative = True

                if first_positive and first_negative:
                    return True

        return False
    
    def spread(row, col, is_negative, processed):
        neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for r, c in neighbours:
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and (r, c) not in processed:
                if grid[r][c] < 0:
                    grid[r][c] -= 1
                else:
                    grid[r][c] += 1
                
                if (is_negative and grid[r][c] > 0) or (not is_negative and grid[r][c] < 0):
                    grid[r][c] *= -1

    def recursive_overflow(grid, a_queue, steps):
        overflow_list = get_overflow_list(grid)
        processed = []

        if not overflow_list or not difference(grid):
            return steps

        for r, c in overflow_list:
            is_negative = (grid[r][c] < 0)
            neighbours = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            neighbours_overflow = sum(0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and (nr, nc) in overflow_list for nr, nc in neighbours)

            grid[r][c] = neighbours_overflow
            processed.append((r, c))
            spread(r, c, is_negative, processed)

        grid_copy = [row[:] for row in grid]
        a_queue.enqueue(grid_copy)
        return recursive_overflow(grid, a_queue, steps + 1)

    return recursive_overflow(grid, a_queue, 0)
