# UI for Free Fall Penetrometers

## How to get drop view running
1. Navigate to sponsor-docs/'CS Capstone'/'dropView Distrib (v1100)-20230801T174944Z-001'/()/Volume/
- be mindful of spaces
2. Run setup.exe 
- this will install dropview
- keep in mind the install location you selected
3. Navigate to the install location you selected and run 'dropView_v1100.exe'
4. Select an input binary file from 'Aquafort 08-01-2023' directory 


## Software Requirements
python3 and pip

to install the necessary python packages:
```
python3 -m pip install tk
python3 -m pip install numpy
python3 -m pip install matplotlib==3.9.2
python3 -m pip install pandas
```

## Running the program
To run:

1. execute `main.py` from the `\src` directory:
```
python3 main.py
```

2. Select your blueDrop number from the dropdown menu

3. Click "Select Data File" and select your blueDrop data file with the `.bin` extension from the file explorer

The data will automatically be saved to the F_Matrix.csv file under the `\output` directory.
The accelerometer data, ppm, and raw data matrices will be output to stdout in the terminal.

## Known issues

## Using JSON to input calibration factors

There is a JSON file in the src folder that contains the outline for inputting calibration factors
The default values are the current values for blue drop 8, but all the values can be modified to any calibration constant
To use the constants from the JSON, select the 'json' option in the dropdown from the file select window


- If this package is located deep within the file system of your computer, then you may experience issues with selecting multiple files.