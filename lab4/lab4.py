from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    #X is the variable currently being assigned
    X = state.get_current_variable()
    value = None

    if X is None: return True                     #Thus this is the root of the search tree, since forward checking could only be done when there are variables to be assigned
    
    x = X.get_assigned_value()
    constraints_list = state.get_constraints_by_name(X.get_name())

    for const in constraints_list:

        if (const.get_variable_i_name() != X.get_name() ):
            Y = state.get_variable_by_name( const.get_variable_i_name() )
        else:
            Y = state.get_variable_by_name( const.get_variable_j_name() )

        for y in Y.get_domain():
            #if not fulfilling constraint, remove y
            if not const.check(state, x, y):
                Y.reduce_domain(y)
            if ( Y.domain_size() == 0 ):
                return False

    return True


# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    #Some general mistake in the CSP search
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    #agenda = list()

    all_vars = state.get_all_variables()

    singletons = []
    flagged = []

    for s in all_vars:
        if s.domain_size() == 1:
            singletons.append(s.get_name())

    while (len(singletons) != 0):
        X = state.get_variable_by_name( singletons[0] )
        x = X.get_domain()[0]

        for const in state.get_constraints_by_name(singletons[0]):
            i = state.get_variable_by_name(const.get_variable_i_name())
            j = state.get_variable_by_name(const.get_variable_j_name())

            if i == X:
                Y = j
            else:
                Y = i

            for y in Y.get_domain():
                if not const.check(state, x, y):
                    Y.reduce_domain(y)
                if Y.domain_size() == 0:
                    return False

        for var in state.get_all_variables():
            varName = var.get_name()
            if (var.domain_size() == 1) and (varName not in flagged) and (varName not in singletons):
                singletons.append(varName)

        flagged.append(singletons[0])
        singletons.pop(0)
    return True

    # #As long as there is an element in the queue
    # for s in singletons:
    #     value = s.get_domain()[0]
        
    #     constraints_list = state.get_constraints_by_name( s.get_name() )

    #     for const in constraints_list:
    #         if ( const.get_variable_i_name != s.get_name() ):
    #             Y = state.get_variable_by_name( const.get_variable_i_name() )
    #         else:
    #             Y = state.get_variable_by_name( const.get_variable_j_name() )

    #         for y in Y.get_domain():
    #             #if not fulfilling constraint, remove y
    #             if not const.check(state, value, y):
    #                 Y.reduce_domain(y)
    #             if ( Y.domain_size() == 0 ):
    #                 return False    


## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    dist = 0.00

    for item1, item2 in zip(list1, list2):
        dist += (item1 - item2)**2
    dist = math.sqrt(dist)
    
    return dist
    
#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 3)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def get_disorder(branch, clas, branch_total_length):
    sample_count = 0
    for x in branch:
        if x == clas:
            sample_count += 1
    fraction = sample_count / branch_total_length
    return ( fraction * math.log(fraction , 2) ) if fraction > 0 else 0

def information_disorder(yes, no):    
    total_yes = float(len(yes))
    total_no = float(len(no))
    total = total_yes + total_no
    fraction_yes = total_yes / total
    fraction_no = total_no / total

    """Calculating the disorder within the 'yes' branch"""
    disorder_in_yes = 0.00000
    for clas in ['Democrat', 'Independent', 'Republican']:
        disorder_in_yes -= get_disorder(yes, clas, total_yes)

    disorder_in_yes = fraction_yes * (disorder_in_yes)

    """Calculating the disorder within the 'no' branch"""
    disorder_in_no = 0.00000
    for clas in ['Democrat', 'Independent', 'Republican']:
        disorder_in_no -= get_disorder(no, clas, total_no)
   
    disorder_in_no = fraction_no * (disorder_in_no)

    return disorder_in_no + disorder_in_yes



#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people, house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 45
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
