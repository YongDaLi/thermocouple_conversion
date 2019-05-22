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

    with open ('conversion.csv') as csv_file:
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
    closets = 1
    for i in range (1, len(arr), 1):
        if val >= arr[i]:
            closest = i

    # min index is 1, max index is last index
    return closest


def main():
    # get data for type T thermocouple
    temp, voltage = read_file()

    # define min and max conversion values
    min_voltage = voltage[0]
    max_voltage = voltage[len(voltage) - 1]

    min_temp = temp[0]
    max_temp = temp[len(temp) - 1]

    while(1):

        # request reference temperature and measured voltage
        ref_temp = float(input("Enter reference temperature: "))
        measured_voltage = float(input("Enter measured voltage (mV): "))

        # check if values are within range of conversion
        if (ref_temp < min_temp or ref_temp > max_temp):
            print("Error: reference temperature out of range {" + str(min_temp) + ", " + str(max_temp) + "} °C")
        
        elif (measured_voltage < min_voltage or measured_voltage > max_voltage):
            print("Error: measured voltage out of range {" + str(min_voltage) + ", " + str(max_voltage) + "} mV")
        
        # if no errors, perform conversion
        else:

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


            # print("t_index:", t_index)
            # print("adj_voltage", adj_voltage)
            # print("v_index:", v_index)

            print("Temperature is:", adj_temp)
            
        print()

main()