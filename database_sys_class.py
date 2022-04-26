#Author: Tristan Bailey
#Date Created: 2/20/2022
#Last Modified: 4/26/2022
#Assignment: PA 4
#Class: CS457
#File: File for the database methods

#libraries
import sys
import os
import table_methods as TB
import helper_methods as helper

class database_sys:
    #shared class variable
    database_in_use = None

    def __init__(self):
        pass

    #creates the database director in the master database directory
    def create_database(self, database_name):
        #make a directory that represents this database
        if not os.path.exists("databases/"+ database_name.lower()):
            os.mkdir("databases/" + database_name.lower())
            print("Database " + database_name + " created.")
        else:
            print("!Failed to create database " + database_name + " because it already exists.")
    
    #adds the specified table to the currentlyl used database by calling
    #   the make table method
    def add_table(self, table_name, param_list, type_list):
        #check if table already exists in the database
        if os.path.exists("databases/" + database_sys.database_in_use + "/" + table_name.lower() + ".txt"):
            print("!Failed to create table " + table_name + " because it already exists.")
        else:
            #create the specified table's file for storage
            TB.make_table(database_sys.database_in_use, table_name, param_list, type_list)
            print("Table " + table_name + " created.")
    
    #deletes the specified table from the currnetly used database directoy by
    #    calling the remove table method.
    def delete_table(self, table_name):
        #check if table exists in the database
        if not(TB.table_exists(database_sys.database_in_use, table_name)):
            print("!Failed to delete " + table_name + " because it does not exist.")
        else:
            #delete the specified table's file
            TB.remove_table(database_sys.database_in_use, table_name)
            print("Table " + table_name + " deleted.")
    
    #checks if the database already exists
    def database_exists(self, database_name):
        if os.path.exists("databases/"+ database_name):
            return True
        else:
            return False

    #returns a table that contains the desired fields and consits of only records that satisfy the given expressions 
    def database_select(self, tokens):
        WGHO = ["where", "group by", "having", "order by", "on"]

        index = helper.keyword_index(tokens, "from")
        attribute_names = tokens[:index]
        
        tokens = tokens[index + 1:]

        x = 0
        exit = False
        while(not(exit) and (x < len(tokens))):
            if tokens[x].lower() in WGHO:
                exit = True
            else:
                x += 1

        table_names = tokens[:x]
        tokens = tokens[x:]
        #check if join
        table_names_size = len(table_names)
        #multi-table operation
        if(table_names_size > 2):
            return TB.binary_join(database_sys.database_in_use ,table_names, tokens[1:])
        #o.w. single table operation
        #in this version we support only one table, but it can be expanded to accept multi table
        some_table = TB.load_table(database_sys.database_in_use, table_names[0])
        
        #check the table loaded properly
        if(some_table == []):
            raise Exception("!Failed to query table " + table_names[0] + " because it does not exist.")

        #special case where we are doing no extra augmentations but only retriving table columns
        if(0 == len(tokens)):
            #complete for this if
            if(attribute_names[0] != "*"):
                some_table = TB.remove_all_other_columns(some_table, attribute_names)
            #o.w. int this particular case we're basically just printing the table from disk to the
            #   consol
        else:
            #*** at this point for PA2 we need only consider where, but if the other options
            #   beed be added return here, filter out where, make the same call, and then do proper
            #   handling of the rest of the options present, also consider the case in which the other
            #options exits but where does not
            if(tokens[0].lower() == "where"):
                tokens = tokens[1:]
                
                #take the set difference between all possible indicies and the indicies that pass the where conditions
                records_to_del = list(set(range(2, len(some_table))).difference(set(TB.index_list_generator(some_table, tokens))))
                
                #remove the records that do not fit the where clause
                TB.delete_record(some_table, records_to_del)
           
            some_table = TB.remove_all_other_columns(some_table, attribute_names)
        return some_table   

    #returns a bool representing if a particular database was able to be removed
    def delete_database(self, database_name):
        dir = "databases/"+ database_name.lower()
        if self.database_exists(database_name):
            for root, dirs, files in os.walk(dir):
                for name in files:
                    os.remove(os.path.join(root, name))
            os.rmdir(dir)
            print("Database " + database_name + " deleted.")
        else:
            print("!Failed to delete " + database_name + " because it does not exist.")

    #changes the database currently in use
    def use_database(self, database_name):
        if(self.database_exists(database_name.lower())):
            database_sys.database_in_use = database_name.lower()
            print("Using database " + database_name + ".")
        else:
            print("Database " + database_name + " does not exist.")

    #returns the database currently in use
    def cur_database(self):
        #updates the cur database in use for all class objects
        return database_sys.database_in_use

    #alters the specified table in the currently used direcotry by adding the specified
    #   parameter and its respective datatype
    def alter_table_add(self, table_name, attribute, data_type, add):
        if(add):
            TB.add_table_attribute(database_sys.database_in_use, table_name, attribute, data_type)
            print("Table " + table_name + " modified.")
        else:
            #*** add subtraction functionality later
            pass
    
    #adds the respective tuple to the 
    def insert_data(self, table_name, param_list):
        if(not(TB.add_tuple(database_sys.database_in_use, table_name, param_list))):
            print("Failed to insert record")
        else:
            print("1 new record inserted")
    
    #wipes all records matching the given list of relational args (one dimensional and in order) from table in disk
    def delete_from_database(self, table_name, relational_args):
        some_table = TB.load_table(database_sys.database_in_use, table_name)
        original_len = len(some_table)

        if(some_table == []):
            return

        indexes_that_contain = TB.index_list_generator(some_table, relational_args)
        TB.delete_record(some_table, indexes_that_contain)
        
        removed = original_len - len(some_table)
        if(removed == 1):
            print("1 record deleted.")
        else:
            print(str(removed) +  " records deleted.")

        TB.save_table(database_sys.database_in_use, table_name, some_table)

    def update_table(self, table_name, tokens):
        #find keyword 'where'
        index = helper.keyword_index(tokens, "where")
        values_to_set = tokens[:index]
        #get relational args right of 'where'
        relational_args = tokens[index+1:]

        #load the table into memory
        some_table = TB.load_table(database_sys.database_in_use, table_name)
        #check table loaded
        if(some_table == []):
            return

        #make a list of tuple indexes that have the desired attributes
        indexes_that_contain = TB.index_list_generator(some_table, relational_args)

        #update the records in the table in memory
        TB.update_records(some_table, indexes_that_contain, values_to_set)
        
        #save updates to disk
        TB.save_table(database_sys.database_in_use, table_name, some_table)
        
        #some print/returns
        if(len(indexes_that_contain) == 1):
            print("1 record modified.")
        else:
            print(str(len(indexes_that_contain)) + " records modified.")
        
