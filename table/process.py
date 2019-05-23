'''
Yong Da Li
Wednesday, May 22, 2019
Professor Ho Ghim Wei

quick python program to convert table form to csv form
'''

import csv

def main():
    output = []
    temp = []

    # open file, which is copy-paste from table with 2 end columns removed
    # raw1 is all the negative values
    with open('raw1.csv', 'r') as in_csv1:
        reader = csv.reader(in_csv1, delimiter = ',')
        for row in reader:
            # flip the order of each row (for negatives) and append
            # only take 0-9 values, since the ends repeat
            temp = row[::-1]
            temp = temp [0:10]
            output = output + temp


    # raw2 is all the positive values
    with open('raw2.csv', 'r') as in_csv2:
        reader = csv.reader(in_csv2, delimiter = ',')
        for row in reader:
            # don't need to flip order
            # only take 0-9 values, since the ends repeat
            temp = row [0:10]
            output = output + temp


    # manually add the last value, since we skipped it
    output = output + [20.869]


    # convert all to floats
    for i in range (0, len(output)):
        output[i] = float(output[i])


    # start at -270 degrees C
    temp = -270
    i = 0
    with open('conversion.csv','w') as out_csv:
        writer = csv.writer(out_csv, delimiter = ',')

        # write header
        writer.writerow(['temp', 'voltage'])

        for row in output:
            row = [temp] + [row]
            writer.writerow(row)

            temp = temp + 1

main()