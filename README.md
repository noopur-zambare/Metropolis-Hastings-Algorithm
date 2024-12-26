## Angry Birds Level Generation using Metropolis-Hastings Algorithm (MCMC)

The Metropolis-Hastings (Markov Chain Monte Carlo) method generated tile-based levels for Angry Birds. 
The process began with the use of a propose function, which randomly selected two tiles for potential swapping. 
Following this, the probability of the tile configurations was calculated, and the tiles were evaluated based on their adjacency to other tiles. 
To decide whether to accept the proposed swaps, the Metropolis-Hastings algorithm was applied through an accept function, where the likelihoods before and after the swap were compared. 
Finally, the occurrence of adjacent tiles was analyzed, aiding in evaluating the likelihood of that specific configuration.


### Analysis of Mixing Time
Mixing time refers to the duration required for the Markov Chain to converge to its stationary distribution. The mixing probability was calculated by evaluating the likelihood of each state in the grid, taking into account adjacency frequencies and occurrences. These likelihoods were then averaged to assess how efficiently the Markov Chain mixes across the state space, varying with the number of swaps.


### Generated Content
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/b477f5df-fd7d-43f1-ab8f-7e1a012f4a3d" alt="good4" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/721d3478-1dc3-4bdb-80d8-751648860647" alt="good3" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/eaca283a-3805-437f-bba2-347d4cd71e85" alt="good2" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/f4e4cf78-7e2d-4c91-b570-840f25e8283f" alt="good1" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/41e8f22b-f4ef-4192-ae3d-c36bf2a6691d" alt="good5" width="200"></td>
  </tr>
</table>




