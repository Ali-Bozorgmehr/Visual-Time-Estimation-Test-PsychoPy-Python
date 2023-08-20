# Psychopy Experiment - Time Perception Test

This is a Python project developed using the Psychopy library to conduct a time perception test. The experiment consists of two tests: 

1. **Test 1: Time Interval Perception**
   - Participants observe a sequence of shapes with varying time intervals.
   - They are required to press the space bar twice with a specific interval between presses that matches the time interval between the first and last red rectangle.

2. **Test 2: Time Interval and Shape Count Perception**
   - Similar to Test 1, but participants need to note both the number of shapes presented and the time intervals between them.
   - Participants press the space bar after each shape appearance, and all keypress times are recorded.


### Test Data
The experiment records participant responses, including reaction times and experiment parameters. The data is stored in two DataFrames:

df_interval: Contains data for Test 1 (Time Interval Perception).

df_number_interval: Contains data for Test 2 (Time Interval and Shape Count Perception).

The experiment also combines the results from both tests into a single DataFrame called results.

### Saving Results
After the experiment, you can save the results to a text file using the provided save dialog. Click the "Save" button in the graphical user interface (GUI) to choose a location to save the data.

### License
This project is designed and developed by Ali Bozorgmehr.
