#Voting system
class Preference:
  """this is for testing only. DO NOT SUBMIT
  """
  def __init__(self,preferences):
    """Initialise the preference object

    Args:
        preference (dict): A dictionary where keys are voters No. [1,..m] and values are list
        of ranked order of candidates [1,..,n]
        Example: {1: [1, 2, 3, 4], 2: [3, 2, 1, 4]}
    """
    self.preferences = preferences
    self.candidates = (len(v) for v in preferences.values())
    self.voters = len(preferences)  # No of voters

  def candidates(self):
    """Returns a list of candidates/alternatives in a list of the form [1..n].
    """
    return list(range(1, self.candidates +1))
  
  def voters(self):
    """Returns a list of voters/agents, in a list of distinct voters of the form [1,...,m].
    """
    return list(self.preferences.keys())
  
  def get_preference(self,candidate,voter):
    """Returns the preference rank of the given candidate for the given voter. The highest rank candidate will return 0, and the lowest ranked candidate will return n-1.

    Args:
        candidate (int): candidate No. 
        voter (int): Voter No.
    
    Returns:
        int: The rank of the candidates for the given voter
    """
    rank = self.preferences[voter]
    return rank.index(candidate)


def dictatorship(preferences, agent):
    """Return the first-ranked alternative of the dictator

       Args:
       preferences (Preference): Preference object of the given alternative for the given voter
       agent (int): index of the agent
    """
    if agent not in preferences.voters():
        # Check if the agent exists, if not raise error
        raise ValueError

    for candidate in preferences.candidates():  # Loop through list of candidates
        if preferences.get_preference(candidate, agent) == 0:
            # Return the candidate with index 0
            return candidate

# Make a function to handle the tie-breaking agent's preference in the order of their ranking
def tie_breaking_rule(preferences, tie_break):
    """Returns list of tie-breaking agent's preference in the order of their ranking

    Args:
        preferences (Preference): Preference object containing the preferences
        tie_break (int): Denotes the tie breaking agent
    """
    # If there is a tie, use the tie breaking agent
    if tie_break not in preferences.voters():
        raise ValueError("Agent does not exist")

    # Get the list of all candidates
    candidate = preferences.candidates()

    # Sort the candidates according to the tie breaking agent's preference
    sorted_candidate = sorted(candidate, key=lambda candidate: preferences.get_preference(candidate, tie_break))
    return sorted_candidate

def scoring_rule(preferences, score_vector, tie_break):
    """Each agent assigns the highest scored based on their preference.
       Returns the candidate with the highest total score.
       If there is a tie, apply tie-breaking option.

    Args:
        preferences (Preference): A Preference object containing the preferences
        score_vector (List[float]): A score of vector of length n, equal to number of candidates
        tie_break (int): Denotes the tie breaking agent
    """
    # Check if score_vector equal to number of candidates
    if len(score_vector) != len(preferences.candidates()):
        raise ValueError("Length of score vector must equal the number of candidates")

    # Initialise a dictionary to store the total scores for each candidate
    total_score = {candidate: 0 for candidate in preferences.candidates()}

    # Loop through each voter to calculate the scores for each candidate
    for voter in preferences.voters():
        for candidate in preferences.candidates():
            # Get the ranking of the preferred candidates
            rank = preferences.get_preference(candidate, voter)
            # Map the rank to the index of score_vector to get score
            score = score_vector[rank]
            total_score[candidate] += score

    # Find the highest value in total_score
    max_val = max(total_score.values())

    # Initialise a list storing candidates with the same highest score
    tied_scores = [candidate for candidate, score in total_score.items() if score == max_val]

    # If there is only one candidate with the highest score, select as winner
    if len(tied_scores) == 1:
        return tied_scores[0]

    # Get tie breaking agent's preference
    tie_break_preference = tie_breaking_rule(preferences, tie_break)

    # Return the first candidate from the agent's preference list that is in tied_scores
    for candidate in tie_break_preference:
        if candidate in tied_scores:
            return candidate

def plurality(preferences, tie_break):
    """Returns the winner who appears the most times in the first position
    of the agent's preference orderings. If there is a tie, apply tie-breaking option.

    Args:
        preferences (Preference): Preference object of the given alternative for the given voter
        tie_break (int): Denotes the tie breaking agent
    """
    # Initialise a dictionary storing the candidate and the number they appear in the first position
    candidate_count = {candidate: 0 for candidate in preferences.candidates()}

    for voter in preferences.voters():
        # For each voter, check all candidates to find the first-ranked one
        for candidate in preferences.candidates():
            if preferences.get_preference(candidate, voter) == 0:
                # When a first-ranked candidate is spotted, increment their count
                candidate_count[candidate] += 1
                break  # Stop after the first-ranked candidate

    # Find all the candidates with the same max counts
    max_count = max(candidate_count.values())
    tied_count = [candidate for candidate, count in candidate_count.items() if count == max_count]

    # If there is only one candidate with the highest count, select as winner
    if len(tied_count) == 1:
        return tied_count[0]

    # If there is more than one candidate with the highest count, use the tie breaking agent
    tie_break_preference = tie_breaking_rule(preferences, tie_break)

    # Return the first candidate from the agent's preference list that is in tied_scores
    for candidate in tie_break_preference:
        if candidate in tied_count:
            return candidate

# Create a function that calculates points for each candidate based on scoring rule
def get_scores(preferences, scoring_function):
    """Calculates points for each candidate based on different rules (veto, borda)

    Args:
        preferences (Preference): Preference object of the given alternative for the given voter
        scoring_function (str): A string indicating which rule to use, such as:
            - 'veto': The veto rule, where all candidates except the last-ranked candidate receive 1 point.
            - 'borda': The borda rule, where each candidate receives points based on their ranking (higher ranks receive more points).
    """
    # Initialise a dictionary to store the candidates and their points
    candidate_points = {candidate: 0 for candidate in preferences.candidates()}

    for voter in preferences.voters():
        # Get the list of candidates and their ranking for each voter
        for candidate in preferences.candidates():
            rank = preferences.get_preference(candidate, voter)
            if scoring_function == 'veto':  # Apply veto logic
                points = 0 if rank == len(preferences.candidates()) - 1 else 1
            elif scoring_function == 'borda':  # Apply borda logic
                points = 0 if rank == len(preferences.candidates()) - 1 else (len(preferences.candidates()) - 1 - rank)
            else:
                raise ValueError("Invalid scoring rule")
            candidate_points[candidate] += points
    return candidate_points

def veto(preferences, tie_break):
    """For each voter's preference, last place candidate receives 0 points, every other candidate receives 1 point. Winner has the most points. If there is a tie, apply tie-breaking option.

    Args:
        preferences (Preference): Preference object of the given alternative for the given voter
        tie_break (int): Denotes the tie breaking agent
    """
    # Get the points using the veto_scoring function
    candidate_points = get_scores(preferences, 'veto')

    # Find the highest point in candidate_point, store it in a list called tied_point.
    max_points = max(candidate_points.values())
    tied_points = [candidate for candidate, points in candidate_points.items() if points == max_points]

    # If there is only one element in tied point, select candidate as winner
    if len(tied_points) == 1:
        return tied_points[0]

    # Get tie breaking agent's preference
    tie_break_preference = tie_breaking_rule(preferences, tie_break)

    # Return the first candidate from the agent's preference list that is in tied_scores
    for candidate in tie_break_preference:
        if candidate in tied_points:
            return candidate

def borda(preferences, tie_break):
    """For each voter's preference, candidate ranked at position j receives a score of n-j.
    Winner has the most scores. If there is a tie, apply tie-breaking option.

    Args:
        preferences (Preference): Preference object of the given alternative for the given voter
        tie_break (int): Denotes the tie breaking agent
    """
    # Get the points using the veto_scoring function
    candidate_points = get_scores(preferences, 'borda')

# Find the highest point in candidate_points, store it in a list called tied_point.
    max_points = max(candidate_points.values())
    tied_points = [candidate for candidate, points in candidate_points.items() if points == max_points]

    # If there is only one element in tied point, select candidate as winner
    if len(tied_points) == 1:
        return tied_points[0]

    # Get tie breaking agent's preference
    tie_break_preference = tie_breaking_rule(preferences, tie_break)

    # Return the first candidate from the agent's preference list that is in tied_scores
    for candidate in tie_break_preference:
        if candidate in tied_points:
            return candidate

def STV(preferences, tie_break):
    """Returns the winner of the Single Transferable Vote.
       In each round, candidate that appear the least in the first position are eliminated. Repeats until only one candidate remains.
       If there is a tie, apply tie-breaking option.

    Args:
        preferences (Preference): Preference object of the given alternative for the given voter
        tie_break (int): Denotes the tie breaking agent
    """

    # Initialise a dictionary to store the voters and their preference list in order of ranking
    preference_list = {
        voter: [candidate for candidate in preferences.candidates()] for voter in preferences.voters()
        }

    while len(preference_list) > 1:
        # Initialise a dictionary to store the candidates and number of times they appear in each voters' preference list
        first_position_candidates = {candidate: 0 for candidate in preferences.candidates()}

        for voter in preferences.voters():
            if preference_list[voter]:
                count = preference_list[voter][0]
                first_position_candidates[count] += 1  # Increment the count for each first-ranked candidate

        # Add candidates with the lowest count in the last_placed_candidates list
        min_val = min(first_position_candidates.values())
        eliminated_candidates = [
            candidate for candidate, count in first_position_candidates.items() if count == min_val
        ]

        # Initialise a list of all remaining candidates
        remaining_candidates = [
            candidate for candidate in preferences.candidates() if candidate not in eliminated_candidates
        ]

        for voter in preference_list:
            # remove last placed candidates
            preference_list[voter] = [
                candidate for candidate in preference_list[voter] if candidate in remaining_candidates
            ]

        # Check if there is one reamining candidate left
        if len(remaining_candidates) == 1:
            return remaining_candidates[0]  # Select as winner
        elif len(remaining_candidates) > 1:  # If there is more than one remaining candidates
            tie_break_preference = tie_breaking_rule(preferences, tie_break)  # Use tie breaking agent's preference
            # Return the first candidate from the agent's preference list that is in remaining_candidates
            for candidate in tie_break_preference:
                if candidate in remaining_candidates:
                    return candidate

