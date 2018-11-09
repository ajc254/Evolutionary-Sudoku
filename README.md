# Evolutionary-Sudoku

Manual for EvolSudoku.py

This program performs an evolutionary algorithm to attempt to solve a sudoku grid file provided.
It is designed to be reusable so it is easily ran with different parameters for effective experimentation.

Run the python program from the command line, using the following syntax:

python [Grid Path] [Maximum Generations] [Population Size] [Truncation Rate] 
       [Replacement Rate] [Super Mutate Count] [SM Tolerance] [Time Limit]
       [Verbose]
       
Parameter Descriptions:
    Grid Path:                Path to the file with the sudoku grid to be solved.
    
    Maximum Generations:      The maximum number of generations to run the algorithm for.
    
    Population Size:          The number of individuals per generations.
    
    Truncation Rate:          The percentage of individuals to keep per selection (0-1).
    
    Replacement Rate:         The percentage of parents to replace between generations (0-1).
    
    Super Mutate Count:       The number of unchanging generations before a super mutation,
                              (A guard against becoming trapped in local minima)
                              or use 0 to disable Super Mutations.
                              
    Super Mutation Tolerance: The tolerance defining leniency either side of the previous
                              generation, in order to count as an unchanging generation.
                              E.G. with SM Tolerance = 1: say gen1 = 3 then gen2 = 2,3or4 would be 'unchanging'.
                              
    Time Limit:               Time limit in seconds to apply to the algorithm,
                              or 0 to apply no time limit.
                              
    Verbose:                  Prints out best known fitness solution value after each generation.
                              Also signifies when a super mutation occurs.
                              
                              
Specific commands used for experiments:

    First navigate to the program's location in the terminal/command line.
    
    Population Experiments:

    Grids 1 and 2:
        Population size 10:     python EvolSudoku.py [Grid Path] 1000000 10 0.6 0.2 50 1 0 0
        Population size 100:    python EvolSudoku.py [Grid Path] 1000000 100 0.6 0.2 50 1 0 0
        Population size 1000:   python EvolSudoku.py [Grid Path] 1000000 1000 0.6 0.2 50 1 0 0
        Population size 10000:  python EvolSudoku.py [Grid Path] 1000000 10000 0.6 0.2 50 1 0 0
        
    Grid 3 (time limit needed):
        Population size 10:     python EvolSudoku.py [Grid Path] 1000000 10 0.6 0.2 50 1 300 0
        Population size 100:    python EvolSudoku.py [Grid Path] 1000000 100 0.6 0.2 50 1 300 0
        Population size 1000:   python EvolSudoku.py [Grid Path] 1000000 1000 0.6 0.2 50 1 300 0
        Population size 10000:  python EvolSudoku.py [Grid Path] 1000000 10000 0.6 0.2 50 1 300 0
        
        
    Super Mutation Experiments: 
    
        No Super Mutations:     python EvolSudoku.py [Grid Path] 1000000 100 0.6 0.2 0 0 300 0
        Super Mutations:        python EvolSudoku.py [Grid Path] 1000000 100 0.6 0.2 50 1 300 0
        
    All the above commands will run the algorithm once, I ran these 5 times each and found an average for reliability.

NOTE:
    If you wish to see details of the algorithm running for any of the above runs, change the final '0' to a '1'.
    You may need to adjust 'python' to your version accordingly (written in version 3)
