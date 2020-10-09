'''
Created on Feb 15, 2020

@author: Elif_Kaya_HW12 Kaya

Create an order summary matrix to calculate the number of orders for each day in the given interval amount from the user
'''

#Import necessary libraries 
import orderlog
import datetime 

#Define constants
STARTMIN = 60*6
ORDERS = orderlog.orderlst
CLOSING_MIN = 22 * 60
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#Define the function for interval labels 
def labelString(interval, startmin, duration):
    '''
    produces a string label with begin-end times of an interval
    :param interval: will calculate the interval where the order summary falls on, 
    :param startmin: is the opening hour in minutes
    :param duration: is the interval minutes entered by the user
    :return: returns interval as string 
    '''
    
    #Calculate the start time of the interval
    interval_start = startmin + (duration * interval)
    interval_end = interval_start + duration -1
    
    #Get the start time in hours and minutes
    start_hour = interval_start // 60 
    start_min = interval_start % 60 
    int_beginning = str(start_hour) + ":" + str(start_min).zfill(2)
    
    #Get the end time in hours and minutes 
    end_hour = interval_end // 60 
    end_min = interval_end % 60 
    int_end = str(end_hour) + ":" + str(end_min).zfill(2)
    
    return int_beginning + "-" + int_end


def composeWeeklyOrdersMatrix(duration = 60):
    '''
    produces a matrix for weekly orders
    :param duration: interval duration defaulting to 60 when nothing specified
    :return: returns summary matrix as 2 dimensional list 
    
    '''
    #calculating the opening and closing hours of the shop in minutes 
    global STARTMIN
    global ORDERS
    global CLOSING_MIN
    
    total_mins_open = CLOSING_MIN - STARTMIN #total mins the business open in one day
    
    #Calculate the total number of intervals based in duration
    total_intervals = total_mins_open // duration

    #Starting the 2d array - initializing the 2d array to 0
    summary_matrix = [[0]*total_intervals for i in range (7)]
    
    #go through the order list excluding the first row to find the minutes and split them with : to calculate the total mins
    for order in ORDERS[1:]:
        minutes = order[1].split(":")

        tot_minutes_per_order = int(minutes[0]) * 60 + int(minutes[1]) 
        occurence = (tot_minutes_per_order - STARTMIN) // duration

        dates = order[0].split("-")
        day = datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2])).weekday()

        #increase summary matrix of the dimensions of number of days and number of interval
        summary_matrix[day][occurence] +=1 

    return summary_matrix


def printOrderSummaryMatrix(summary_matrix, duration):
    '''
    prints order summary matrix
    :param summary_matrix: the matrix we created in our previous function
    :param duration: the interval in minutes 
    
    '''
    global CLOSING_MIN
    global STARTMIN
    global WEEK_DAYS
    
    #Assign the variable in our header that will be the same in every output
    header_output = "DAY\TIME | " 
 
    total_mins_open = CLOSING_MIN - STARTMIN
    
    #Calculate the total number of intervals in a day
    total_intervals = total_mins_open // duration
    
    #doing a for loop to find each interval and print it all in the same line 
    for i in range(total_intervals):
        header_output += labelString(i, STARTMIN, duration) + "|"
    print()
    print("WEEKLY ORDER SUMMARY") 
    print()
    print(header_output)
    print("-"*57) #crates the dashes after the label 
    
    #create a for loop to print the corresponding weekdays in our matrix 
    
    for r in range(len(summary_matrix)):
        day_label = WEEK_DAYS[r]
        print(day_label.ljust(9), end = "") #fill with spaces to the right 
        
        
        row = summary_matrix[r]
        for column in row:
            print(str(column).rjust(11), end = " ") #fill with spaces to the left with 11 spaces 
        print()
    print("-"*57)


def main():
    '''

    asks user for input, creates matrix, prints matrix and then asks user again to enter a day to calculate the 
    max order interval on that day
    
    '''
    
    global STARTMIN
    global WEEK_DAYS
    
    #Ask the user to specify the length (in minutes) of the time interval used to aggregate the orders
    user_interval = eval(input("Please specify the length of the time interval in minutes: "))
    
    # produce summary matrix
    summary_matrix = composeWeeklyOrdersMatrix(user_interval)
    
    # print matrix
    printOrderSummaryMatrix(summary_matrix, user_interval)
    

    #Create a while loop to get day information from user to display the peak interval of that day until they only press enter 
    peak_interval = None
    while peak_interval is not "":
        peak_interval = input("Enter day to see peak interval, or press enter to stop: ").lower().title()
        #Check to see if what user entered is in our week_day list 
        if peak_interval in WEEK_DAYS:
            index_row = WEEK_DAYS.index(peak_interval)
            
            row = summary_matrix[index_row] 
            row_max = max(row)
            
            interval_row = row.index(row_max)
            final_output = labelString(interval_row, STARTMIN, user_interval)
            print(final_output + ",", row_max, "orders")
            

    print("Bye!") #final print when they hit enter 
    

main()    

