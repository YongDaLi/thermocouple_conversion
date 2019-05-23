# thermocouple_conversion
Converts voltage measurements from type T thermocouples into temperature data.

Working as a research assistant at the Nanomaterials and Nanosystems Innovation group at the National University of Singapore.

## Setup
1. Find the appropriate thermocouple conversion data sheet for the desired type of themocouple (common ones include Type E, J, K, M, N, T)
2. Copy paste the negative values into raw1.csv and the positive values into raw2.csv, found in the `table` folder
3. Modify `process.py` (in the `table` folder) with the appropriate temperature range and last value
4. Run `process.py` to convert the raw csv files into a 2 column csv of {'temp', 'voltage'}

## Usage
1. Format the input csv file as a 2 column csv of {'ref_temp', 'measured_voltage'} (reference temperature)
2. Run `convert.py`. The output file will save into the `output` folder.
