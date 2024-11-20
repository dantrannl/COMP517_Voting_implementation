# COMP517_Voting_implementation

This project implements various voting rules that take the preferences of a group of voters and determine a winner based on different decision-making methods. The core task is to simulate voting systems, where the input is a preference profile of voters, and the output is the winner according to the selected voting rule.

Voting Rules Implemented:
- Dictatorship Rule: The winner is simply the most preferred alternative of a specific "dictator" (selected agent).
- Scoring Rule: Each voter assigns a score to each alternative based on their ranking, and the alternative with the highest total score wins.
- Plurality Rule: The alternative that appears most often in the first position of voters' rankings wins. Tie-breaker logic is used when necessary.
- Veto Rule: Every voter gives 0 points to their least preferred alternative and 1 point to others. The alternative with the most total points wins.
- Borda Count: Voters rank alternatives and assign points based on their ranking (most preferred gets the highest score). The alternative with the highest total score is the winner.
- Single Transferable Vote (STV): This is an iterative process where alternatives with the least support are eliminated until only one alternative remains (or a tie-breaker is used).

Key Features:
- Preference Profile: A preference profile represents the rankings of all voters over the set of alternatives.
- Tie-breaking Agent: For voting rules that may result in a tie, a specific agent’s ranking is used to determine the final winner.
- Error Handling: Includes validation checks for invalid agents, mismatched score vectors, and other edge cases.
  
Skills & Concepts:
- Object-Oriented Programming: The project uses classes and methods to encapsulate the preferences and behavior of voters and candidates.
- Algorithm Design: Implements various algorithms for counting votes, handling ties, and simulating the rounds of STV.
- Data Structures: Efficient use of lists and dictionaries to store and manipulate the preferences and scores.
- Error Handling: Ensures robustness by handling potential invalid inputs and edge cases (e.g., invalid agents or mismatched score vectors).
