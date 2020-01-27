# -*- coding: utf-8 -*-
"""
Description: This module reads data related to the US states from a csv file 
and outputs the data as per user's preferences. User has the option to print 
a State report for all of the US states, sort the states by their names or 
population,print information related to a particular state or exit the program.

"""

#from csv import reader
from stateClass import State
import numpy
import sys
import csv

global quick_sorted
quick_sorted=False
state_list=[]

def import_data():
    """
    This function will import data from States .csv file into a list and print 
    the total record count of the file.
    Exceptions:
        Program will exit in case an invalid file name is passed in the input.
    """
    filename=raw_input("Enter the file name: ")
    try:
        with open(filename,'rb') as sfile:
            csv_reader=csv.reader(sfile)
            next(csv_reader)
            for row in csv_reader:
                state_list.append(State(row[0],row[1],row[2],row[3],\
                                                        row[4],row[5]))
            print "\nThere were {0} state records read.\n"\
                    .format(len(state_list))
            sfile.close
    except(IOError, RuntimeError, TypeError, NameError):
        print("Program is exiting, "+\
              "please retry by entering a valid file name.")
        sys.exit()
#    
#    filename=str(raw_input("Enter the file name: "))
#    print filename
#    with open(filename,'rb') as sfile:
#        csv_reader=csv.reader(sfile)
#        next(csv_reader)
#        for row in csv_reader:
#            state_list.append(State(row[0],row[1],row[2],row[3],\
#                                                        row[4],row[5]))
#        print "There were {0} state records read.\n"\
#                    .format(len(state_list))
#        sfile.close    

def state_report():
    """
    This function prints State Name, Captital, State abbreviation, Population,
    Region and the number of US house seats for all the fifty US states.
    """
    print('\n{:15s} {:15s} {:^12s} {:20s} {:20s} {:20s}'.format("State Name", \
          "Capital City", "State Abbr", "State Population", "Region", \
          "US House Seats"))
    print("-"*102)
    for item in state_list:
        print('{:15s} {:15s} {:^12s} {:<20,} {:20s} {:20s}'\
            .format(item.stateName,item.capital, item.abbreviation,\
            int(item.population), item.region, item.houseseats))
    print("\n")

def quicksort_state_name(s_list, low, high):
    """
    This function uses the quicksort approach to sort the data from States.csv 
    by the State name.
    Parameters:
        s_list (list): The State list that is to be sorted.
        low (int): This integer acts as the starting index for the quicksort.
        high (int): This integer acts as the last index for the quicksort.
    """
    if (low < high):
        #the below 'index' is the partitiong index
        index = partition(s_list, low, high)
        #List elements will be sorted before and after partition.
        quicksort_state_name(s_list, low, index-1)
        quicksort_state_name(s_list, index+1, high)

    global quick_sorted
    quick_sorted = True

def partition(s_list, low, high):
    """
    This function takes last element in the provided list as pivot. The pivot 
    element is then placed at the correct position in the sorted array, and 
    places the smaller states (by names) tot he left of the pivot and all 
    larger ones to the right.
    Parameters:
        s_list (list): The State list that is to be sorted.
        l (int): This integer acts as the starting index of the partition.
        h (int): This integer acts as the last index of the partition.
    """
    i = (low-1)
    pivot = s_list[high].stateName
    for j in range(low, high):
        if (s_list[j].stateName <= pivot):
            i += 1
            s_list[i], s_list[j] = s_list[j], s_list[i]

    s_list[i+1], s_list[high] = s_list[high], s_list[i+1]
    return (i+1)

def countingSort(s_list,exp1):
    """
    This function does a count sort of the State list.
    Parameters:
        s_list (list): The State list that is to be sorted.
        exp1 (int): counting sort is done according exp1's value.
    """
    high=len(s_list)
    output=[0]*(high)
    count=[0]*100

    for i in range(0, high):
        index = (int(s_list[i].population)/int(exp1))
        count[int((index)%10)] += 1

    for i in range(1,10):
        count[i] += count[i-1]

    i = high-1
    while i>=0:
        index = (int(s_list[i].population)/int(exp1))
        output[ count[int((index)%10)] - 1] = s_list[i]
        count[int((index)%10)] -= 1
        i -= 1

    i = 0
    for i in range(0,len(s_list)):
        s_list[i] = output[i]

def radix_sort_population(s_list):
    """
    This function uses radix sort approach to sort the provided list by
    population.
    Parameters:
        s_list (list): The State list that is to be sorted.
    """
    #Find the max value of the population coulmn.
    population_list = numpy.genfromtxt("States.csv",dtype='float',\
                    delimiter =',',skip_header=1,skip_footer=0,usecols=3,\
                    usemask=True)
    max_population=int(max(population_list))
    #Counting sort for every population value.
    exp=1
    while max_population/exp > 0:
        countingSort(s_list,exp)
        exp*=10

    global quick_sorted
    quick_sorted = False

def binary_search_rf(binary_search_state,s_list,low,high):
    """
    This function does a binary search on the State list usign the State name
    specified in the search.
    Parameters:
        binary_search_state (str): Name of the State to be searched.
        s_list (list): State list in which the state is to be searched.
        low (int): Starting index in the list for the search
        high (int): Last index in the list for the search
    Returns:
        mid (int): This is the index of the searched state.
        (-1): In case the specified state doesn't exist in the list.
    """
    if high>=low:
        mid=int((low+high)/2)
        if str(s_list[mid].stateName).upper()==binary_search_state:
            return mid
        elif str(s_list[mid].stateName).upper()>binary_search_state:
            return binary_search_rf(binary_search_state,s_list,low,mid-1)
        elif str(s_list[mid].stateName).upper()<binary_search_state:
            return binary_search_rf(binary_search_state,s_list,mid+1,high)
        else:
            return -1
    else:
        return -1

def sequential_search(sequential_search_state,s_list,high):
    """
    This function does a sequential search on the State list usign the State 
    name specified in the search.
    Parameters:
        sequential_search_state (str): Name of the State to be searched.
        s_list (list): State list in which the state is to be searched.
        high (int): Last index in the list to be searched for the state
    Returns:
        i (int): This is the index of the searched state.
        (-1): In case the specified state doesn't exist in the list.
    """
    for i in range(high):
        if str(s_list[i].stateName).upper()==sequential_search_state:
            return i
    return -1


def main():
    """

    """
    import_data()
    low=0
    high=len(state_list)-1

    qContinue="yes"
    print("Below are the options:\n"\
         "1) Print a state report\n"\
         "2) Sort by state name\n"\
         "3) Sort by population\n"\
         "4) Find and print a given state\n"\
         "5) Quit")
    option=raw_input("Enter your choice: ")

    while qContinue=="yes":
        if option=="1":
            state_report()
            print("Below are the options:\n"\
                 "1) Print a state report\n"\
                 "2) Sort by state name\n"\
                 "3) Sort by population\n"\
                 "4) Find and print a given state\n"\
                 "5) Quit")
            option=raw_input("Enter your choice: ")

        elif option=="2":
            quicksort_state_name(state_list, 0, (high))
            print("\nStates sorted by State name.\n")
            print("Below are the options:\n"\
                 "1) Print a state report\n"\
                 "2) Sort by state name\n"\
                 "3) Sort by population\n"\
                 "4) Find and print a given state\n"\
                 "5) Quit")
            option=raw_input("Enter your choice: ")

        elif option=="3":
            radix_sort_population(state_list)
            print("\nStates sorted by Population.\n")
            print("Below are the options:\n"\
                 "1) Print a state report\n"\
                 "2) Sort by state name\n"\
                 "3) Sort by population\n"\
                 "4) Find and print a given state\n"\
                 "5) Quit")
            option=raw_input("Enter your choice: ")

        elif option=="4":
            search_statei=raw_input("Enter the state name: ")
            search_state=str(search_statei).upper()
            global quick_sorted
            if quick_sorted==True:
                print("\nBinary search\n")
                binary_search_index=\
                binary_search_rf(search_state,state_list,low,high+1)

                if binary_search_index > -1:
                    print(state_list[binary_search_index])
                else:
                    print("Error: State {0} not found.\n"\
                          .format(search_statei))
            else:
                 print("\nSequential search\n")
                 sequential_search_index=sequential_search(search_state,\
                                                           state_list,high+1)
                 if sequential_search_index > -1:
                     print(state_list[sequential_search_index])
                 else:
                    #print(f"Error: State {search_statei} not found.\n")
                    print("Error: State {0} not found.\n"\
                          .format(search_statei))

            print("Below are the options:\n"\
                 "1) Print a state report\n"\
                 "2) Sort by state name\n"\
                 "3) Sort by population\n"\
                 "4) Find and print a given state\n"\
                 "5) Quit")
            option=raw_input("Enter your choice: ")

        elif option=="5":
            qContinue="no"
            print("\nHave a good day!")
            break
        else:
            option=raw_input("Please enter a valid value between 1 to 5: ")

if __name__ == "__main__":
    main()  # Calling the main() function




