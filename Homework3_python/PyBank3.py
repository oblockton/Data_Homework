# Import dependencies
import os
import csv
import sys
 # set path to file
pybankCSV = os.path.join("budget_data.csv")
# Read file
with open(pybankCSV, 'r') as csvfile:
    pyBank = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvfile)
# Define function that does the analysis
    def analyze(file):
        # initialize base value and empty lists used in the analysis
        sumMonths = 0
        sumPL  = 0
        # trailing & leading value list. The value is equal to the profit/loss value
        trailing = []
        leading = [] # leading value list will not include the first month's profit/loss value.

        # initialize list of changes(leading value - trailing value)
        changes = []
        # Initialize list of months where a change value is calcuted
        # Ex: Feb/leading $ value - Jan/trailing $ value = Change for month Feb
        changeMonth = []

        # Iterate through rows in file
        # Data is aggregated based on the same iterator number.
        # Ex: The value that trails the leading value(leading[i])
        # is located at trailing[i] .
        for i in file:
            # Calcute total months, each row is one month
            sumMonths = sumMonths + 1
            # calcutate sum of profit/loss, each row has one P/L value
            sumPL = sumPL + int(i[1])
            # Set trailing values, which is equal to list of all values
            trailing.append(int(i[1]))
            # Set the inital P/L value so leading list & the list of months with a change(changeMonth)
            # does not include the first month.
            initVal= trailing[0]
            if int(i[1]) != initVal:
                leading.append(int(i[1]))
                changeMonth.append(i[0])

        # Calcute all the  P/L changes. Since the initial month does not Count
        # as a month of change, there is only a calculable change if there is a leading value.
        # The length of list of change values = length of leading value lsit.
        # Build list of changes.
        for i in range(len(leading)):
            changes.append(leading[i] - trailing[i])

        #Set intial values
        maxChange= changes[0]
        maxMonth= changeMonth[0]
        leastChange = changes[0]
        leastMonth = changeMonth[0]
        # Iterate through list of changes.
        # First loop will set the above^^^ variable to the first change in P/L value.
        # Max/least values are then calcuted in comparison to the first value.
        for i in range(len(changes)):
            if changes[i] > maxChange:
                maxChange = changes[i]
                maxMonth = changeMonth[i]
            if changes[i] < leastChange:
                leastChange = changes[i]
                leastMonth = changeMonth[i]

        # Calcute the average of all the changes in the changes list.
        changesum = sum(changes)
        avg_change = round((changesum / (len(changes))),2)

        # Create the varialbe that contains a formatted string of our analysis
        # and captured data.
        Analysis = """
Financial Analysis
-----------------------------------
Total Months: """ + str(sumMonths) +"""
Total: $""" + str(sumPL) +"""
Average Change: $""" + str(avg_change) +"""
Greatest Increase in Profits: """ + maxMonth + " ($" + str(maxChange) + """)
Greatest Decrease in Profits: """ + leastMonth + " ($" + str(leastChange) + ")"


        return Analysis
    # set a variable that triggers the function to execute,
    # allowing us the print the returned value( the analysis string)
    # The function here is hard coded to run on the specific PyBank.csv file
    # However using this method the code can be modified so that the functions arguement
    # is the result of a user input, or can be called on another csv read variable.
    analysis_run = analyze(pyBank)
    # Print to terminal
    print(analysis_run)

    # Write the output file.
    with open("PyBankOut.txt", "w") as f:
        f.write(analysis_run)
#to add to file change "w" to "a"= append

        #sys.stdout = open('PyBankOut.txt', 'w')
        #print(analysis_run)
        #sys.stdout.close(PyBankOut.txt)

        #pybankOut = "PyBankOut.text"
        #pbOut = open(pybankOut, "w")
        #print >>pbOut, (analysis_run)
        #pbOut.close()




        #print(analysis_run)
