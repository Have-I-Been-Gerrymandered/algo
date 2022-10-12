# Voting data CSV Extractor

import csv

csv_filename = ''

file = open(csv_filename, "r")
total_lines = 0
for line in file:
    total_lines += 1

def newRemoveLines(lines):
    with open(csv_filename, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
        writeFile.close()

def readFile(count):
    lines = list()
    with open(csv_filename, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            
            if (count == 0 or row[2] in ("DEMOCRAT", "REPUBLICAN")):
                lines.append((row[0], row[1], row[2], row[5], row[6], row[10], row[11], row[14], row[16]))

            if (count % 1000 == 0):
                print("Processed row: " + str(count))

            if (count == total_lines-1):
                newRemoveLines(lines)

            count += 1

readFile(0)