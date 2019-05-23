'''
Yong Da Li
Wednesday, May 22, 2019
Professor Ho Ghim Wei

converts type T thermocouple voltage to temperature
'''

import csv

# opens file called conversion.csv with {'temp', 'voltage'}
# loads data values into arrays
def read_file():
    temp = []
    voltage = []

    with open ('table/conversion.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        for row in csv_reader:
            temp.append(float(row['temp']))
            voltage.append(float(row['voltage']))

            line_count = line_count + 1

    # print("Finished reading file, processed " + str(line_count) + " lines");
    # print("temp:", temp)
    # print("voltage:", voltage)s

    return temp, voltage


# Arduino map function
# accepts value, range of value, and range of output
# returns linearly mapped value
def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


# accepts value and array (increasing)
# returns index of value in array that is just bigger than input value
def closest_value (val, arr):
    closest = 1
    for i in range (1, len(arr), 1):
        if val >= arr[i]:
            closest = i

    # min index is 1, max index is last index
    return closest


# accepts reference temperature and measured voltage
# returns converted temperature
def convert (ref_temp, measured_voltage):
    # check if values are within range of conversion
    if (ref_temp < min_temp or ref_temp > max_temp):
        adj_temp = "temperatue out of range: {" + str(min_temp) + ", " + str(max_temp) + "} °C"
    
    elif (measured_voltage < min_voltage or measured_voltage > max_voltage):
        adj_temp =  "measured voltage out of range: {" + str(min_voltage) + ", " + str(max_voltage) + "} mV"

    # index of closest integer temperature value
    t_index = closest_value(ref_temp, temp)
    
    # find appropriate voltage as linear map between the 2 closest integer temperatures
    ref_voltage = map(ref_temp, temp[t_index-1], temp[t_index], voltage[t_index - 1], voltage[t_index])
    
    # calculate adjusted voltage
    adj_voltage = ref_voltage + measured_voltage

    # index of closest voltage value
    v_index = closest_value(adj_voltage, voltage)            

    # find appropriate temperature as a linear map between the 2 closets voltage measurements
    adj_temp = map(adj_voltage, voltage[v_index - 1], voltage[v_index], temp[v_index-1], temp[v_index])

    return adj_temp


# driver for command line conversion
def convert_cli ():
    # default reference temperature
    ref_temp = 0

    print("\nCommand line mode selected")
    print("Enter -999 in reference temperature to quit\n")
    while (1):
        # request reference temperature and measured voltage
        ref_temp = float(input("Enter reference temperature (°C): "))

        # quit
        if ref_temp == -999:
            print("quitting command line mode\n")
            return

        measured_voltage = float(input("Enter measured voltage (mV): "))

        # check if values are within range of conversion
        if (ref_temp < min_temp or ref_temp > max_temp):
            print("Error: reference temperature out of range {" + str(min_temp) + ", " + str(max_temp) + "} °C")
        
        elif (measured_voltage < min_voltage or measured_voltage > max_voltage):
            print("Error: measured voltage out of range {" + str(min_voltage) + ", " + str(max_voltage) + "} mV")
        
        # if no errors, perform conversion
        else:
            print("Temperature (°C):", convert(ref_temp, measured_voltage))
            
        # new line for formatting
        print()


# driver for converting volt-->temp for a csv file
def convert_csv():
    print("\ncsv mode selected")

    # include .csv in file name
    input_file = input("Enter name of input csv file: ")
    output_file = input("Enter name of output csv file: ")

    ref_temp = []
    measured_voltage = []
    line_count = 0

    with open (input_file) as in_csv:
        reader = csv.DictReader(in_csv)

        for row in reader:
            ref_temp.append(float(row['ref_temp']))
            measured_voltage.append(float(row['measured_voltage']))

            line_count = line_count + 1

    print("\nProcessed " + str(line_count) + " lines in file: " + input_file)

    with open ("output/" + output_file, 'w') as csv_file:
        fieldnames = ['ref_temp', 'measured_voltage', 'temp']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()

        for i in range (0, line_count):
            temp = convert(ref_temp[i], measured_voltage[i])
            writer.writerow({'ref_temp': ref_temp[i], 'measured_voltage': measured_voltage[i], 'temp': temp})

    print("Conversion finished, output file: " + output_file)

    return


def main():
    print("\n----------Type T Thermocouple---------")
    print("last modified May 22, 2019 by Yong Da Li")
    print("----------------------------------------\n")

    while(1):
        print("0. quit")
        print("1. command line")
        print("2. csv\n")
        choice = int(input("Enter choice: "))

        if choice == 0:
            return
        elif choice == 1:
            convert_cli()
        elif choice == 2:
            convert_csv()

        print("-" * 20)

# setup global variables
# get data for type T thermocouple
temp, voltage = read_file()

# define min and max conversion values
min_voltage = voltage[0]
max_voltage = voltage[len(voltage) - 1]

min_temp = temp[0]
max_temp = temp[len(temp) - 1]

main()
