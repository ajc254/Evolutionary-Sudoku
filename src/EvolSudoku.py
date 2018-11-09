from random import random, shuffle, randint, sample, choice
from copy import deepcopy
from time import time
import sys

grid = []   # Holds rows of base grid 
changeable = []   # Holds indices per row in 'grid' that are not fixed

"""
Processes a file and formulates a base grid, and keeps track of changeable indices.

Parameters
    file_path: Path to the file to be processed
"""
def process_file(file_path):
    
    with open(file_path, "r") as grid_file:
        grid_data = grid_file.readlines()
        
        for line in grid_data:
            current_row = []
            current_changeable = []
            index = 0
            
            # Ignore divider row.
            if line[0] == '-':
                continue
        
            for ch in line:
                # If number is not fixed, add a '0' placeholder & record index.
                if ch == '.':
                    current_row.append(0)
                    current_changeable.append(index)
                    index += 1
                    
                elif ch != '\n' and ch != '!':
                    # If number is fixed, add to the base grid.
                    current_row.append(int(ch))
                    index += 1

            grid.append(current_row)
            changeable.append(current_changeable)
            
            
### Evolutionary Algorithm ###

"""
Perform the evolution using helper functions.
"""
def evolve():

    last_best = 100
    local_counter = 0
    best_known = [[], 100, 0]

    population = create_pop()
    fitness_population = evaluate_pop(population)
    
    for gen in range(MAX_GENERATIONS):
        mating_pool = select_pop(population, fitness_population)
        offspring_population = crossover_pop(mating_pool)
        
        # If detected trapped in local minima, attempt super mutation escape.
        if SUPER_MUTATE_COUNT and local_counter > SUPER_MUTATE_COUNT:
            if VERBOSE: 
                print("SUPER MUTATION")
            mutate_pop(offspring_population, 1)
        else:
            mutate_pop(offspring_population, MUTATION_RATE)
        population = offspring_population
          
        fitness_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        
        # Keep track of best known result.
        if best_fit < best_known[1]:
            best_known[0], best_known[1], best_known[2] = best_ind, best_fit, gen
        
        if VERBOSE:
            print("Generation #", gen, "Best fit: ", best_fit)
        # Stop if solution found.
        if best_fit == 0:
            break
        # If generation not deviated more than SM_TOLERANCE above or below the last.
        if best_fit in range(last_best-SM_TOLERANCE, last_best+SM_TOLERANCE+1):
            local_counter += 1
        else:
            last_best = best_fit
            local_counter = 0
        if TIME_LIMIT and time() - START > TIME_LIMIT:
            break
    
    time_end = time() - START
    
    print("\nResult with: ", FILE_PATH) 
    print("Using Population Size: ", POPULATION_SIZE)
    print("With Generation Limit: ", MAX_GENERATIONS)
    print("\nBest found fitness: ", best_known[1])
    print("Generation: ", best_known[2]) 
    print("In", time_end, "seconds")
    print("\nSolution Grid:\n")    
    print_grid(best_known[0])
    
               

### Population Level Operators ###
            
"""
Create an initial population of defined size.

Returns:
    List of individuals in the created population.
"""
def create_pop():

    return [ create_individual() for _ in range(POPULATION_SIZE) ]

"""
Order the population in terms of the best fitness first.

Parameters:
    population: The population to evaluate.

Returns:
    Sorted list of tuples, each tuple contains the individual and it's fitness value.
"""
def evaluate_pop(population):

    return [ evaluate_individual(individual) for individual in population ]

"""
Take a percentage of the best individuals, percentage defined by constants.

Parameters:
    population: The population to select.

Returns:
    New population selected.
"""
def select_pop(population, fitness_population):

    # Sort the population.
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    # Take only a percentage of the best individuals.
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]

"""
Perform random crossover of individuals and defined replacement of a population.

Returns:
    Offspring population.
"""
def crossover_pop(population):

    # Take some of the best parents, and add to the offspring unchanged.
    offspring = population[:REPLACEMENT_NUMBER]
    
    # Randomly cross the individuals to make the remaining offspring population.
    for _ in range(POPULATION_SIZE-REPLACEMENT_NUMBER):
        offspring.append(crossover_individuals(choice(population), choice(population)))
     
    return offspring

"""
Mutate the population in place, according to a specified rate.

Parameters:
    population: The population to evaluate.
    mutate_rate: The rate of mutation (0-1).
"""
def mutate_pop(population, mutate_rate):

    for indv in population:
        mutate_individual(indv, mutate_rate)
        
"""
Find the best individual in a population.

Parameters:
    population: The population to search for the individual in.
    fitness_population: The respective list of fitnesses to represent the population.

Returns:
    The best individual.
"""       
def best_pop(population, fitness_population):

    return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]         
            
            
### Individual Operators ###

"""
Create an individual using the base grid, and randomly re-assigning non fixed-numbers.

Returns:
    New individual
""" 
def create_individual():

    individual = deepcopy(grid)
    row_index = 0
    
    for row in individual:
        
        # Find the remaining numbers to fill in this row.
        remaining = {1, 2, 3, 4, 5, 6, 7, 8, 9} - set(row)
        remaining = list(remaining)
        # Shuffle them randomly.
        shuffle(remaining)
        
        # Add them in this random order to the non-fixed row locations.
        for index in changeable[row_index] :
            
            row[index] = remaining.pop()
        
        assert len(remaining) == 0
        row_index += 1
        
    return individual
    
"""
Obtain a fitness value for an individual.

Parameters:
   indv: Individual to evaluate.

Returns:
    Fitness value of the individual.
"""
def evaluate_individual(indv):

    conflicts = 0
    
    # Count subgrid conflicts.
    for i in range(0, 8, 3): 
        conflicts += (9 - len(set(indv[i][:3]  + indv[i+1][:3]  + indv[i+2][:3])))
        conflicts += (9 - len(set(indv[i][3:6] + indv[i+1][3:6] + indv[i+2][3:6])))
        conflicts += (9 - len(set(indv[i][6:9] + indv[i+1][6:9] + indv[i+2][6:9])))
       
    # Count row conflicts.
    for row in indv:
        conflicts += (9 - len(set(row)))
        
    # Count column conflicts.
    for col_index in range(9):
        col = []
        for row in indv:
            col.append(row[col_index])
        
        conflicts += (9 - len(set(col)))
        
    return conflicts
    
    
"""
Crossover two individuals.

Parameters:
    indv1: The first parent to crossover.
    indv2: The second parent to crossover.

Returns:
    The crossed child.
"""
def crossover_individuals(indv1, indv2):
    
    crossover_point = randint(1, 8)
    return deepcopy(indv1[:crossover_point]) + deepcopy(indv2[crossover_point:])
    
"""
Mutates an individual in place by swapping the places of two numbers in rows, 
randomly determined by a set rate.

Parameters:
    indv: The individual to mutate.
    mutate_rate: The chance of mutation applied to each row of the individual.
"""
def mutate_individual(indv, mutate_rate):
    
    for n in range(9):
    
        if random() < mutate_rate and len(changeable[n]) > 1:
            swap = sample(changeable[n], 2) # Get the indices of the two elements to swap.
            # Swap their places.
            indv[n][swap[0]], indv[n][swap[1]] = indv[n][swap[1]], indv[n][swap[0]]
    
   
"""
Helper function to print the elements in a list, without a newline.

Parameters:
    list: The list to print.
""" 
def print_list(list):
    for item in list:
        print(item, end='')
        
"""
Prints an individual grid in a human-readable sudoku grid form, to the screen.

Parameters:
    indv: The individual grid to print.
"""  
def print_grid(indv):
    
    for row_index in range(9):
    
        if row_index % 3 == 0 and row_index:
            print('-'*3+'|'+'-'*3+'|'+'-'*3)
              
        print_list(indv[row_index][:3])
        print('|', end='')
        print_list(indv[row_index][3:6])
        print('|', end='')
        print_list(indv[row_index][6:9])
        print('')
    print('\n')

# Algorithm parameter constants provided by the command line input.
FILE_PATH = sys.argv[1]
MAX_GENERATIONS = int(sys.argv[2])
POPULATION_SIZE = int(sys.argv[3])
TRUNCATION_RATE = float(sys.argv[4])
REPLACEMENT_RATE = float(sys.argv[5])
SUPER_MUTATE_COUNT = int(sys.argv[6])
SM_TOLERANCE = int(sys.argv[7])
TIME_LIMIT = int(sys.argv[8])
VERBOSE = int(sys.argv[9])
      
process_file(FILE_PATH)
MUTATION_RATE = 1/len(grid)
REPLACEMENT_NUMBER = int(POPULATION_SIZE * REPLACEMENT_RATE)

# Start the timer and the evolution algorithm!
START = time()
evolve()