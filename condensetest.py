import csv
from distutils.dir_util import copy_tree

inputfile = "cut.csv"
output_filename = "condensed_results.csv"

writefile = open(output_filename, "w")
writer = csv.writer(writefile, lineterminator="\n")
header = ["precinct", "office", "party_detailed", "votes", "county_name", "candidate", "district", "year", "state"]
writer.writerow(header)

current_row = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "", ""]

with open(inputfile, newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")

    dem_votes = 0
    rep_votes = 0
    district = ""

    rows_seen = 0

    for row in spamreader: 

        # Skip header
        if (rows_seen == 0):
            rows_seen += 1
            continue

        if (rows_seen == 1):
            district = row[0]

        # new district
        if (row[0] != district and rows_seen > 0):

            # dem votes
            writer.writerow((row[0], row[1], "DEMOCRAT", dem_votes, row[4], row[5], row[6], row[7], row[8]))

            # rep votes
            writer.writerow((row[0], row[1], "REPUBLICAN", rep_votes, row[4], row[5], row[6], row[7], row[8]))

            district = row[0]
            dem_votes = 0
            rep_votes = 0

            if (row[1] == "end"):
                break

        if (row[2] == "DEMOCRAT"):
            dem_votes += int(row[3])
            
        if (row[2] == "REPUBLICAN"):
            rep_votes += int(row[3])
            
        rows_seen += 1

csvfile.close()
writefile.close()