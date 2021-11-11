"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor
codeskulptor.set_timeout(20)
import random

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    running_maximum = 0
    for number in hand:
        max_for_number = number * hand.count(number)
        if max_for_number > running_maximum:
            running_maximum = max_for_number
    return running_maximum
        
def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    #First we enumerate the possible outcomes for the free dice
    die_sides = []
    for side in range(1, num_die_sides + 1):
        die_sides.append(side)
    possible_outcomes = gen_all_sequences(die_sides, num_free_dice)
    #Then, we calculate the expected value for these outcomes
    #We must view them as possible hands by adding our held dice in
    #This is because score considers the entire hand, not just held dice
    running_total = 0.0
    for outcome in possible_outcomes:
        rolled_dice_list = list(outcome)
        rolled_dice_list.extend(held_dice)
        running_total += score(tuple(rolled_dice_list))
    expected_score = running_total / len(possible_outcomes)
    return expected_score
    
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    #all_holds will keep track of every unique tuple generated
    all_holds = set([()]) 
    #iterative_holds is akin to answer_set in gen_all_sequences()
    iterative_holds = set([()])
    #We will generate tuples ranging from length 1 to length of hand
    for dummy_index in range(len(hand)): 
        temp_set = set()
        for partial_hold in iterative_holds: 
            #Ensure we do not hold duplicate dice by removing held dice (partial_hold) from the hand
            remaining_hand = list(hand)
            for held_die in partial_hold:
                remaining_hand.remove(held_die)
            #We generate possible future holds (new_hold) by iterating over the remaining dice
            #I.e. if we had (1,2) and remaining hand (2,3), we should get (1,2,2) and (1,2,3)
            for die in remaining_hand:
                new_hold = list(partial_hold)
                new_hold.append(die)
                new_hold.sort() #Sorting is important as (1,2,3) and (1,3,2) are the same
                temp_set.add(tuple(new_hold)) #Sets do not take in duplicates, so sorting rejects them
        #We then save all generated tuples to all_holds, and refresh iterative_holds for the next round
        all_holds.update(temp_set)
        iterative_holds = temp_set
    return all_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    max_expected_value = 0
    optimal_hold = []
    #For a given hand, generate all possible holds
    possible_holds = gen_all_holds(hand)
    #For a given hold, generate the expected value - and record the highest
    for hold in possible_holds:
        num_free_dice = len(hand) - len(hold) #Can't assume it's always 5
        hold_expected = expected_value(hold, num_die_sides, num_free_dice)
        if hold_expected > max_expected_value:
            optimal_hold = []
            max_expected_value = hold_expected
            optimal_hold.append(hold)
        if hold_expected == max_expected_value:
            optimal_hold.append(hold)
    return(max_expected_value, random.choice(optimal_hold))

def recommend(hand):
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand_score, hold = strategy(hand, num_die_sides)
    print ("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)
    
print ("To use this planner, enter 'recommend(hand)'")
print ("hand is a tuple of (usually five) numbers, with values corresponding to what you've rolled")
print ("E.g. recommend((1,2,3,4,5))")
