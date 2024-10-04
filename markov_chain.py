import os
import json
from copy import deepcopy
import matplotlib.pyplot as plt
from PIL import Image
import random


""" ---------------------------------------------------------------------------------------------- """

def visualize(dimensions, level, grid_to_image, save_path=None):
    level_image = Image.new("RGB", (dimensions[1] * len(level[0]), dimensions[0] * len(level)))

    for row in range(len(level)):
        for col in range(len(level[0])):
            level_image.paste(grid_to_image[level[row][col]], 
                              (col * dimensions[0], row * dimensions[1], 
                               (col + 1) * dimensions[0], (row + 1) * dimensions[1]))
    plt.figure()
    plt.imshow(level_image)
    if save_path:
        plt.axis('off')
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
        plt.show()


# proposes a swap between two random tiles in the grid
def propose(grid):
    rows = len(grid)
    cols = len(grid[0])

    # list of all possible positions in the grid
    options = [i for i in range(rows * cols)]

    # randomly select two distinct positions to swap
    entries = random.sample(options, 2)

    # ensure the tiles at the two positions are different to avoid a redundant swap
    while grid[entries[0] // cols][entries[0] % cols] == grid[entries[1] // cols][entries[1] % cols]:
        entries = random.sample(options, 2)

    # eeturn the coordinates of the two tiles to be swapped
    return [(entries[0] // cols, entries[0] % cols), (entries[1] // cols, entries[1] % cols)]


# calculates the likelihood of a tile at a given position based on its neighbors
def calculate_likelihood(grid, position, adjacency_frequencies, occurrences):
    tile_val = grid[position[0]][position[1]]
    probability = 1
    
    # check the four neighboring tiles (up, down, left, right)
    for offset in [(0,1), (1,0), (0,-1), (-1,0)]:
        row = position[0] + offset[0]
        col = position[1] + offset[1]
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            probability *= occurrences[tile_val]/sum(occurrences.values())
            continue
        offset_val = grid[row][col]
        adjacencies = adjacency_frequencies[offset_val]
        total = sum(adjacencies.values())
        adjacency_count = adjacencies.get(tile_val, 0)
        probability *= adjacency_count / total if total > 0 else 1

    return probability


# decides whether to accept a proposed swap based on likelihood comparison
def accept(grid, tile_one_pos, tile_two_pos, adjacency_frequencies, occurrences):

    # calculate the likelihood of the current grid before the swap
    before_grid = deepcopy(grid)
    before_likelihood = 1
    for pos in [tile_one_pos, tile_two_pos]:
        for offset in [(0,0), (0,1), (1,0), (0,-1), (-1,0)]:
            row = pos[0] + offset[0]
            col = pos[1] + offset[1]
            if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
                continue
            before_likelihood *= calculate_likelihood(before_grid, (row, col), adjacency_frequencies, occurrences)
    
    # perform the swap to create the new grid state
    after_grid = deepcopy(grid)
    after_grid[tile_one_pos[0]][tile_one_pos[1]], after_grid[tile_two_pos[0]][tile_two_pos[1]] = (
        after_grid[tile_two_pos[0]][tile_two_pos[1]],
        after_grid[tile_one_pos[0]][tile_one_pos[1]]
    )
    
    # calculate the likelihood of the new grid state after the swap
    after_likelihood = 1
    for pos in [tile_one_pos, tile_two_pos]:
        for offset in [(0,0), (0,1), (1,0), (0,-1), (-1,0)]:
            row = pos[0] + offset[0]
            col = pos[1] + offset[1]
            if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
                continue
            after_likelihood *= calculate_likelihood(after_grid, (row, col), adjacency_frequencies, occurrences)
    
    if before_likelihood == after_likelihood == 0:
        after_likelihood, before_likelihood = 0.5, 0.5
    
     # use the Metropolis-Hastings acceptance criterion to decide whether to accept the swap
    should_accept = random.choices([False, True], weights=[before_likelihood, after_likelihood])[0]

    # return the new grid if the swap is accepted, otherwise return the original grid.
    return after_grid if should_accept else before_grid


# calculates the adjacency frequencies and occurrences of each tile in the level
def calculate_tile_adjacency_frequencies(level):
    adjacency_frequencies_list = {}
    occurrences = {}
    
    for row in range(len(level)):
        for col in range(len(level[0])):
            tile = level[row][col]
            occurrences[tile] = occurrences.get(tile, 0) + 1
            
            if tile not in adjacency_frequencies_list:
                adjacency_frequencies_list[tile] = {}

            for tile_offset in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                adjacent_row = row + tile_offset[1]
                adjacent_col = col + tile_offset[0]
                
                if 0 <= adjacent_row < len(level) and 0 <= adjacent_col < len(level[0]):
                    adjacent_tile = level[adjacent_row][adjacent_col]
                    adjacency_frequencies_list[tile][adjacent_tile] = (
                        adjacency_frequencies_list[tile].get(adjacent_tile, 0) + 1
                    )

    return adjacency_frequencies_list, occurrences


# validation for good/bad conetnt
def check_contact_and_support(grid):
    # tiles to check for contact and support
    target_tiles = {'1', '2', '3', '4', '5', '6'}
    contact = False
    support = True  # start assuming there's support unless proven otherwise

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            tile = grid[row][col]
            if tile in target_tiles:
                # check if this tile is in contact with another target tile
                for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    adj_row = row + offset[0]
                    adj_col = col + offset[1]
                    if (0 <= adj_row < len(grid)) and (0 <= adj_col < len(grid[0])):
                        if grid[adj_row][adj_col] in target_tiles:
                            contact = True

                # check if the tile is supported (not above tile '0')
                if row < len(grid) - 1:  # not in the last row (ground)
                    if grid[row + 1][col] == '0':  # directly below is air
                        support = False
                # check if it lies above air (tile '0')
                if row > 0 and grid[row - 1][col] == '0':  # directly above is air
                    support = False
                
                # if it's in the bottommost row (ground), it has support by default
                if row == len(grid) - 1:
                    support = True

                # check if it's floating on left or right edges
                if col > 0 and grid[row][col - 1] == '0':  # left side
                    support = False
                if col < len(grid[0]) - 1 and grid[row][col + 1] == '0':  # right side
                    support = False

    if contact and support:
        return "Good: All tiles are in contact and have support."
    else:
        return "Bad: Some tiles are floating or not in contact."

# analysis of mixing time across swaps
def mixing_time_analysis(grid, adjacency_frequencies, occurrences):
    likelihoods = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            probability = calculate_likelihood(grid, (row, col), adjacency_frequencies, occurrences)
            likelihoods.append(probability)
    return sum(likelihoods) / len(likelihoods) if likelihoods else 0


""" ---------------------------------------------------------------------------------------------- """


grid_to_image = {}
tiles = ["0", "1", "2", "3", "4", "5", "6"]
for tile in tiles:
    grid_to_image[tile] = Image.open(f'tiles/{tile}.png')

with open('input_level.json', 'r') as f:
    input_level = json.load(f)

dimensions = grid_to_image["0"].size

# adjacency frequencies and occurrences
adjacency_frequencies_list, occurrences = calculate_tile_adjacency_frequencies(input_level)

flat_list = [item for sublist in input_level for item in sublist]
random.shuffle(flat_list)
rows, cols = len(input_level), len(input_level[0])
grid = [flat_list[i * cols:(i + 1) * cols] for i in range(rows)]


""" ---------------------------------------------------------------------------------------------- """

# generating output images
output_folder = 'output_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

generated_grids = []
for round in range(30):
    for i in range(50000):
        tiles_to_swap = propose(grid)
        grid = accept(grid, tiles_to_swap[0], tiles_to_swap[1], adjacency_frequencies_list, occurrences)
    
    generated_grids.append(deepcopy(grid))
    image_path = os.path.join(output_folder, f'level__round_{round + 1}.png')
    print(check_contact_and_support(grid))
    visualize(dimensions, grid, grid_to_image, save_path=image_path)

# Save all generated grids to a JSON file
output_json_path = 'output_levels_grid.json'
with open(output_json_path, 'w') as json_file:
    json.dump(generated_grids, json_file, indent=4)

print(f"All grids saved to {output_json_path}")