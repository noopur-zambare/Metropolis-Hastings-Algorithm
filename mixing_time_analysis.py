import json
import random
import matplotlib.pyplot as plt
from markov_chain import propose, accept, mixing_time_analysis, calculate_tile_adjacency_frequencies


""" ---------------------------------------------------------------------------------------------- """
# loading input file
with open('input_level.json', 'r') as f:
    input_level = json.load(f)
flat_list = [item for sublist in input_level for item in sublist]
random.shuffle(flat_list)
rows, cols = len(input_level), len(input_level[0])
grid = [flat_list[i * cols:(i + 1) * cols] for i in range(rows)]

tile_adjacency_frequencies, occurrences = calculate_tile_adjacency_frequencies(input_level)

with open('output_levels_grid.json', 'r') as json_file:
    generated_grids = json.load(json_file)

for round in range(1):
    swap_counts = []  # list to store the number of swaps for this round
    mixing_probabilities = []  # list to store mixing probabilities for this round

    for i in range(50000):
        tiles_to_swap = propose(grid)
        grid = accept(grid, tiles_to_swap[0], tiles_to_swap[1], tile_adjacency_frequencies, occurrences)

        # keep track of swap counts and mixing probabilities
        swap_counts.append(i)  # add the current iteration as the number of swaps
        mixing_probability = mixing_time_analysis(grid, tile_adjacency_frequencies, occurrences)  # Assuming this function is defined
        mixing_probabilities.append(mixing_probability)

# plots
    plt.figure()
    plt.plot(swap_counts, mixing_probabilities, marker='.', color='#4A90E2', markersize=4, linestyle='-', linewidth=1)
    plt.xlabel('Number of Swaps')
    plt.ylabel('Likelihood')
    plt.grid(color='grey', linestyle='--', linewidth=0.5)
    plt.show()
