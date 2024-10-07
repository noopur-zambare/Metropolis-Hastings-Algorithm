# Angry Birds Level Generation using Metropolis-Hastings Algorithm (MCMC)

The Metropolis-Hastings (Markov Chain Monte Carlo) method was employed to generate tile-based levels for Angry Birds. 
The process began with the use of a propose function, which randomly selected two tiles for potential swapping. 
Following this, the probability of the tile configurations was calculated, evaluating the tiles based on their adjacency to other tiles. 
To decide whether to accept the proposed swaps, the Metropolis-Hastings algorithm was applied through an accept function, where the likelihoods before and after the swap were compared. 
Finally, the occurrence of adjacent tiles was analyzed, aiding in the evaluation of the likelihood of that specific configuration.


## Analysis of Mixing Time
The analysis of mixing time refers to the duration required for the Markov Chain to converge to its stationary distribution. The mixing probability was calculated by evaluating the likelihood of each state in the grid, taking into account adjacency frequencies and occurrences. These likelihoods were then averaged to assess how efficiently the Markov Chain mixes across the state space, varying with the number of swaps.
