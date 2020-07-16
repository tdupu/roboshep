from openpyxl import *
import table_functions.pytabe

Class SheetObject:
    """
    A wrapper to help work with excel_spreadsheets for sheets of openpyxl.
    
    Assumptions:
    --the spreadsheed has the first column a list of strings
    (these will be the keys for our dictionaries)
    --we never want to add more keys to our sheet.
    
    > from openpyxl import *
    >
    
    """
    __init__(self,excel_worksheet):
        """
        To instantiate such a class we just need to pass it an openpyxl sheet.
        """
        #read off the first row of the spreadsheet keep track of which column has which entry
        
        self.sheet = excel_worksheet
        
        self.column_dict = {}
        j=0
        for value in self.sheet.inter_rows(min_row=1,max_row=1,values_only=True):
            j=j+1
            self.column_dict[j]=value
            
        self.number_of_keys = j
        
        self.keys = self.column_dict.keys()
        
        self.set_of_keys = set(self.keys) #since this may be used many times
        
        #index =
        
    #def __iter__(self):
    #    return self
        
    #def __next__(self):
    #    not implemented
    
    def is_valid_entry(self, new_entry):
        """
        New entries are assumed to be dictionaries.
        """
        set_of_entry_keys = set(new_entry.keys())
        return set_of_entry_keys.is_subset(self.set_of_keys)

        
    def append(self, new_entry):
        """
        Takes a dictionary input and if its keys match the keys for the spreadsheet it will make a new row.
        """
        if self.is_valid_entry(new_entry):
            new_row = [ new_entry[self.column_dict[i+1]] for i in range(self.number_of_keys)]
            self.sheet.append(new_row)
            
        else:
            return ValueError
            
            
    def get(self,partial_entry):
        """
        --INPUT: partial_entry is a dictionary which has a subset of self.keys for entries.
        --OUTPUT: this function will return all the elements of the spreadsheet as dictionaries whose entries matches those that we searched for.
        """
        if self.is_valid_entry(partial_entry):
            entry_keys = partial_entry.keys()
            
            matches = []
            
            for row in self.sheet.iter_rows(min_row=2,values_only=True):
                
                #first convert the row to a dictionary
                row_as_dictionary = self.row_to_dict(row)
                
                #if the row is a match, throw the dictionary into the list of matches
                if is_subdictionary(partial_entry,row_as_dictionary):
                    matches.append(row_as_dictionary):
                    
            return matches
            
        else:
            return ValueError #you were trying to look-up some bogus shit
            
    def remove(self, partial_entry):
        
            
    def row_to_dict(self, row):
        """
        Converts a given row to a dictionary.
        The row needs to be a list or tuple with values only!
        """
        row_as_dictionary = {}
        for i in range(self.number_of_keys):
            row_as_dictionary[self.keys[i]] = row[i]
            
        return row_as_dictionary
