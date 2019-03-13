# import dependencies
import pandas as pd
import numpy as np

#Read file file from which pandas manipulates data.
election_data_file = "election_data.csv"
election_data_pd = pd.read_csv(election_data_file)

# Get count of all votes.
total_votes = election_data_pd["Voter ID"].count()
#print(total_votes)

# Create array containing list of unique values in "Candidate" column.
candidates = election_data_pd["Candidate"].unique()

# This returns a series which is only being used to debug and verify votes per candidate.
vote_candidate = election_data_pd["Candidate"].value_counts()
#print(vote_candidate[0])

#  create multiple arrays that store needed data.
#These arrays are built in the same order as the Candidate list.
#Ex: vote_count_list[1] is the value corresponding to candidate[1], and so on.
vote_count_list = []
vote_percent_list = []
for i in range(len(candidates)):
    # Grabs all rows in "Candidate" column
    # which contain/match the name in the list of candidates at index i.
    aggregate_candidate = election_data_pd.loc[election_data_pd["Candidate"] == candidates[i]]
    # Count the single candidate aggregated list.
    # Append the count to a vote_count_list
    candidate_vote = aggregate_candidate["Candidate"].count()
    vote_count_list.append(candidate_vote)
    # Create a list of percentages.
    vote_percent = (vote_count_list[i] / total_votes)* 100
    vote_percent_list.append(vote_percent)

for i in range(len(vote_percent_list)):
    if vote_percent_list[i] == max(vote_percent_list):
        winner = candidates[i]
print(winner)
# initialize a header and footer variable so entire string can be used again easily
header_title_totalvotes = """
Election Results
-----------------------
Total Votes: """ + str(total_votes) + """
----------------------- """

footer_election_winner = """
-----------------------
Winner: """ + winner + """
-----------------------"""


# Print analysis to terminal
print(header_title_totalvotes)
for i in range(len(candidates)):
    print(candidates[i] + " "+ str(round(vote_percent_list[i], 2)) + "%" + " " + "(" + str(vote_count_list[i]) + ")")
print(footer_election_winner)



# Write the analysis to file
with open("PyPollOut_complete.txt", "w", newline="") as f:
    f.write(header_title_totalvotes + "\n")
    for i in range(len(candidates)):
        f.write(candidates[i] + " "+ str(round(vote_percent_list[i], 2)) + "%" + " " + "(" + str(vote_count_list[i]) + ")" + " "+ "\n")
    f.write(footer_election_winner + "\n")
