from math import inf
from random import shuffle, uniform
COLORS = 6
#assigns a random color to each pin, so that the guesses are a bit less predictable
colorList = ["Blue", "Green", "Yellow", "Orange", "Purple", "Pink"]
shuffle(colorList)

#Returns if a combination is still possible given a guess and a constraint
def is_possible(combination, guess, constraint):
    return (reds:=equal_pins(combination, guess))==constraint[0] and semi_equal_pins(combination, guess)-reds==constraint[1] 


def combination_to_string(combination):
    return(f"({', '.join(list(map(lambda x: colorList[x], combination)))})")

#Returns the number of white pins in the response, given a guess and a solution
def equal_pins(comb1, comb2):
    return len([x for x in list(zip(comb1, comb2)) if x[0]==x[1]])

#Returns the number of white + red pins in the respons, given a guess and a solution
def semi_equal_pins(comb1, comb2):
    A = [0]*COLORS
    B = [0]*COLORS
    for pin in comb1:
        A[pin]+=1
    for pin in comb2:
        B[pin]+=1
    return sum(map(lambda a: min(a[0],a[1]), zip(A,B)))

#Returns the number of combinations ruled out by a guess and a constraint    
def excludes(combination, constraint, possible):
    count = 0
    for comb in possible:
        if not is_possible(comb, combination, constraint):
            count+=1
    return count

#Guesses a given combination
def guess(guess, possible):
    old_possibilities = len(possible)
    constraintInput = input(f"The guess is {combination_to_string(guess)}. What is the response? 'red' 'white' ").split()
    constraint = (int(constraintInput[0]), int(constraintInput[1]))
    update(guess, constraint, possible)
    new_possibilities = len(possible)
    print(f"Eliminated {old_possibilities-new_possibilities} combination{'' if new_possibilities==1 else ''}. There {'is' if new_possibilities==1 else 'are'} now {new_possibilities} remaining.")


#Removes all combinations that are ruled out by the constraint
def update(guess, constraint, possible):
    remove_set = set()
    for comb in possible:
        if not is_possible(comb, guess, constraint):
            remove_set.add(comb)
    possible-=remove_set

#Updates the symmetry table given a guess and a bool 
def update_symmetry(symmetry, guess, no_info):
    occurences = [0]*COLORS
    for n in guess:
        occurences[n] = 1 if no_info else occurences[n]+1
        if n in symmetry["used_once"]:
            symmetry["used_twice"].add(n)
            for m in range(COLORS):
                if n!=m:
                    symmetry["table"][n][m], symmetry["table"][m][n] = 0, 0
        symmetry["used_once"].add(n)
    sets = dict()
    for n, m in enumerate(occurences):
        if not (m in sets):
            sets[m] = set()
        sets[m].add(n)
    for n in range(COLORS):
        for S in sets:
            if not (n in S):
                for m in S:
                    symmetry["table"][n][m], symmetry["table"][m][n] = 0, 0
    included = set()
    sets = []
    for n, row in enumerate(symmetry["table"]):
        if n in included:
            continue
        group = set()
        for m, b in enumerate(row):
            if b==1:
                group.add(m)
                included.add(m)
        sets.append(group)
    for i, S in enumerate(sets):
        for n in S:
            symmetry["map"][n] = COLORS+i
                
     
def main():
    #List of all possible combiinations 
    combinations = [(x,y,z,w) for x in range(COLORS) for y in range(COLORS) for z in range(COLORS) for w in range(COLORS)]
    #List of all combinations not yet ruled out
    possible = set(combinations)
    #List of all possible responses
    constraints = [(x,y) for x in range(5) for y in range(5) if x+y<5]
    #object that keeps track of data related to utilizing pin symmetry to speed up move generation
    symmetry = {
        "table":[[1]*COLORS for _ in range(COLORS)],
        "map":{-1:n for n in range(COLORS)},
        "used_once":set(),
        "used_twice":set()        
    }

    #The algorithm will always choose this as its first guess, so there is no point in calculating it 
    guess((0,0,1,1), possible)
    #End if the correct combination was found
    if(len(possible)==1):
        print(f"The correct combination is: {combination_to_string(list(possible)[0])}")
        return
    #Print and error if input doesnt make sense
    if(len(possible)==0):
            print("The supplied responses lead to a contradiction!")
            return
    while True:
        global_best = 0
        best_comb = (-1,-1,-1,-1)
        #Find the combination that has the best worst case
        for comb in combinations:
            local_worst = inf
            for const in constraints:
                if (exc:=excludes(comb, const, possible)) < local_worst:
                    local_worst = exc
            if local_worst > global_best:
                global_best = local_worst
                best_comb = comb
        #Guess the combination
        guess(best_comb, possible)
        if(len(possible)==1):
            print(f"The correct combination is: {combination_to_string(list(possible)[0])}")
            return
        if(len(possible)==0):
            print("The supplied responses lead to a contradiction!")
            return

main()