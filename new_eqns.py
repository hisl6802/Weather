#/usr/bin/python3 
'''Create the functions in a class called NewEquations that allows
a new user to input equations into and the program will put the new 
equations into the dictionary allowing the new equations to be sent 
to Wunderground via a post request.'''


class NewEquations:
    
    
    #take an input of the engineering dictionary and the list if pulling 
    #from list and output the engineering dictionary with the added term.
    #
    def weather(dictionary, lst = []):
        eng_data = dictionary
        units = lst 
        key = 'weather'
        eqn = 'Sunny'
        eng_data[key] = eqn
        
        return eng_data
        
    #take an input from the engineering dictionary and list if pulling
    #from the list and output the engineering dictionary.
    #
    def clouds(dictionary, lst = []):
        eng_data = dictionary
        units = lst 
        key = 'clouds'
        eqn = 'overcast'
        eng_data[key] = eqn
        
        return eng_data
        
    #take an input from the engineering data dictionary and list if pulling
    #from the list and output the engineering dictionary with added 
    #key and value.
    #
    def UV(dictionary, lst = []):
        eng_data = dictionary
        units = lst 
        key = 'UV'
        eqn = 'index' #could pull from units here if the UV was output in
        #the lst.
        eng_data[key] = eqn
        
        return eng_data
    
    def windgustmph_10m(dictionary, lst = []):
        eng_data = dictionary
        units = lst 
        key = 'windgustmph_10m'
        eqn = units[3] - 43 # simply a place holding function at this 
        #point showing the user how to 
        eng_data[key] = eqn
        
        return eng_data
    
    def windgustdir_10m(dictionary, lst = []):
        eng_data = dictionary
        units = lst 
        key = 'windgustdir_10m'
        eqn = (units[5] + 19)/1000 #input your own funtion here.
        eng_data[key] = eqn
        
        return eng_data
    #
    #Input the number of soil temperature sensors which you will be 
    #adding to the engineering data dictionary, in the numsoiltemp argument.
    #
    def soiltempf(dictionary, lst = [], numsoiltemp = 1):
        eng_data = dictionary
        units = lst 
        if numsoiltemp == 1:
            key = 'soiltempf'
            eqn = units[10] 
        
        
        
