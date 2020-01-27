# -*- coding: utf-8 -*-
"""
Description: This module consists of class 'State' to hold data for US 
states. It has getter and setter methods for every instance variable
and methods displaying information related to the state.

"""

class State:
    """
    The class contains data for the fifty US states and provide methods for
    displaying information related to a state.
    """
    def __init__(self,stateName,capital=None,abbreviation=None,population=0, \
                 region=None,houseseats=0):
        """ This is the __init__ method, which gets called everytime an
        instance of the class is created.
        """
        self.stateName=stateName
        self.capital=capital
        self.abbreviation=abbreviation
        self.population=population
        self.region=region
        self.houseseats=houseseats

    def get_stateName(self):
        """
        Getter method for State's name
        """
        return self.stateName
    
    def set_stateName(self, newstate):
        """
        Setter method for State's name
        """
        self.stateName = newstate

    def get_capital(self):
        """
        Getter method for State's capital city
        """
        return self.capital
    
    def set_capital(self, newcapital):
        """
        Setter method for State's capital city
        """
        self.capital = newcapital
            
    def get_abbreviation(self):
        """
        Getter method for abbreviation
        """
        return self.abbreviation
    
    def set_abbreviation(self, newabbreviation):
        """
        Setter method for abbreviation
        """
        self.abbreviation = newabbreviation

    def get_population(self):
        """
        Getter method for State's population
        """
        return self.population
    
    def set_population(self, newpopulation):
        """
        Setter method for State's population
        """
        self.population = newpopulation
      
    def get_region(self):
        """
        Getter method for State's region
        """
        return self.region
    
    def set_region(self, newregion):
        """
        Setter method for State's region
        """
        self.region = newregion

    def get_houseseats(self):
        """
        Getter method for US House seats
        """
        return self.houseseats
    
    def set_houseseats(self, newhouseseats):
        """
        Setter method for US House seats
        """
        self.houseseats = newhouseseats
        
    def __gt__(self,other_state):
        """
        This method compares two state objects based on their State names.
        """
        if (self.stateName > other_state.stateName):
            print("{0} State is greater lexicographically when " \
                  "compared to {1}".format(self.stateName, \
                               other_state.stateName))
        elif (self.stateName == other_state.stateName):
            print("You supplied same name states as input")
        else:
            print("{0} State is smaller lexicographically when " \
                  "compared to {1}".format(self.stateName, \
                               other_state.stateName))

    def __str__(self):
        """
        This method returns the class objects in the defined string format.
        """       
        
        return '{:<18}{:<}{}{:<18}{:<}{}{:<18}{:<}{}{:<18}{:<,d}{}{:<18}{:<}{}{:<18}{:<}{}'\
                .format('State Name: ', self.stateName, '\n',\
                'Capital City: ', self.capital,'\n',\
                'State Abbr: ', self.abbreviation,'\n',\
                'State Population: ', int(self.population), '\n', \
                'Region: ', self.region, '\n', \
                'US House Seats: ', self.houseseats, '\n'
                )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        