# 2048
This is the 2nd assignment of the Artificial Intelligence course at Columbia University. This code presents an example of adversarial search using minimax with alpha-beta pruning and heuristic functions, completed on March 16, 2020.

**Problem Description:**
An instance of the 2048-puzzle game is played on a 4×4 grid, with numbered tiles that slide in all four directions when a player moves them. Every turn, a new tile will randomly appear in an empty spot on the board, with a value of either 2 or 4. Per the input direction given by the player, all tiles on the grid slide as far as possible in that direction, until they either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide while moving, they will merge into a single tile, valued at the sum of the two original tiles that collided. The resulting tile cannot merge with another tile again in the same move.

With typical board games like chess, the two players in the game (i.e. the "Computer AI" and the "Player") take similar actions in their turn, and have similar objectives to achieve in the game. In the 2048-puzzle game, the setup is inherently asymmetric; that is, the computer and player take drastically different actions in their turns. Specifically, the computer is responsible for placing random tiles of 2 or 4 on the board, while the player is responsible for moving the pieces. However, adversarial search can be applied to this game just the same.

In the 2048-puzzle game, the computer AI is technically not "adversarial". In particular, all it does is spawn random tiles of 2 and 4 each turn, with a designated probability of either a 2 or a 4; it certainly does not specifically spawn tiles at the most inopportune locations to foil the player's progress. However, we create a "Player AI" to play as if the computer is completely adversarial.

**Strategies:**

- Employ the **minimax** algorithm. 
- Implement **alpha-beta pruning**. This speeds up the search process by eliminating irrelevant branches.
- Use **heuristic functions**. It is highly impracticable to search the entire depth of the theoretical game tree. To be able to cut off the search at any point, heuristic functions allow the assignment of approximate values to nodes in the tree. The time limit allowed for each move is 0.2 seconds.
- Assign **heuristic weights** for more than one heuristic functions.

**Resources:** 
[stackoverflow post](https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048) about smoothness and monotonicity.
