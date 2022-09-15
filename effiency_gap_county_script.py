import csv
import math

csv_filename = ''

dem_votes = 0
rep_votes = 0
total_votes = 0

count = 0
alt = 0
with open(csv_filename, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    net_votes = 0
    net_dem_votes = 0
    net_wasted_dem_votes = 0
    net_rep_votes = 0
    net_wasted_rep_votes = 0
    dem_seats_won = 0
    rep_seats_won = 0

    for row in spamreader:
        # Skip header
        if (count == 0):
            count = 1
            continue
        if (count == 1):
            county = row[4]
            count = 2

        if (row[4] != county):

            # efficiency gap
            total_wasted_votes = abs(net_wasted_dem_votes - net_wasted_rep_votes)
            eff_gap = total_wasted_votes / net_votes

            # The sign used with EG depends on whether the wasted votes favor the majority party(+) or not(-).
            ideal_eff_gap = 0
            
            # Wasted votes favor majority party: Party has more wasted votes than their opponent but won fewer seats
            if ((net_wasted_dem_votes >= net_wasted_rep_votes and dem_seats_won <= rep_seats_won) or 
                (net_wasted_rep_votes >= net_wasted_dem_votes and rep_seats_won <= dem_seats_won)):
                ideal_eff_gap = abs(((1 + eff_gap) / (1 + 0.1)) - 1)
            # Wasted votes favor minority party
            else:
                ideal_eff_gap = abs(((1 - eff_gap) / (1 + 0.1)) - 1)

            print("[ Election Results for " + county + " ]")
            print("Dem votes: " + str(net_dem_votes) + " ... Wasted: " + str(net_wasted_dem_votes) + " ... Seats won: " + str(dem_seats_won))
            print("Rep votes: " + str(net_rep_votes) + " ... Wasted: " + str(net_wasted_rep_votes) + " ... Seats won: " + str(rep_seats_won))
            print("Effiency Gap: " + str(round(eff_gap, 4)))
            print("Ideal Efficiency Gap: " + str(round(ideal_eff_gap, 4)))
            print("\n-------------------\n")

            net_votes = 0
            net_dem_votes = 0
            net_wasted_dem_votes = 0
            net_rep_votes = 0
            net_wasted_rep_votes = 0
            dem_seats_won = 0
            rep_seats_won = 0
            county = row[4]

        # Last row
        if (row[4] == "End"):
            break

        if (alt == 0):
            dem_votes = 0
            rep_votes = 0
            total_votes = 0
            print("District: " + str(row[0]) + " [State: " + str(row[8]) + "]")
            alt = 1
        else:
            alt = 0
        
        if (row[2] == "DEMOCRAT"):
            print("Dem Votes: " + str(row[3]))
            dem_votes += int(row[3])
        elif (row[2] == "REPUBLICAN"):
            print("Rep Votes: " + str(row[3]))
            rep_votes += int(row[3])

            # do math
            total_votes += rep_votes
            total_votes += dem_votes

            # net
            net_votes += total_votes
            net_dem_votes += dem_votes
            net_rep_votes += rep_votes

            # majority winner
            votes_for_majority = total_votes / 2
            if (votes_for_majority % 2 == 0):
                votes_for_majority = int(votes_for_majority+1)
            else:
                votes_for_majority = int(math.ceil(votes_for_majority))

            if (dem_votes > rep_votes):
                winner = "D"
                dem_seats_won += 1
            else:
                winner = "R"
                rep_seats_won += 1

            print("Total district votes: " + str(total_votes))
            print("Votes needed for majority: " + str(votes_for_majority))

            # wasted votes
            dem_wasted_votes = 0
            rep_wasted_votes = 0
            total_wasted_votes = 0

            if (winner == "D"):
                dem_wasted_votes = abs(dem_votes - votes_for_majority)
                rep_wasted_votes = rep_votes
            elif (winner == "R"):
                dem_wasted_votes = dem_votes
                rep_wasted_votes = abs(rep_votes - votes_for_majority)

            print("Dem wasted votes: " + str(dem_wasted_votes))
            print("Rep wasted votes: " + str(rep_wasted_votes))

            net_wasted_dem_votes += dem_wasted_votes
            net_wasted_rep_votes += rep_wasted_votes