#Author: Tristan Bailey
#Date Created: 2/20/2022
#Last Modified: 5/10/2022
#Assignment: PA 4
#Class: CS457
#File: File for the table methods

#libraries
import sys
import os
import helper_methods as helper

#Note: attribute does not account for if it is desired that attributes with diferent datatypes can
# have the same attribute name, as searching and etc need the datatype

#these are possible attribute datatypes
#   valid_datatypes = {"int", "varchar", "float", "char"}

#separator used in table file reads/writes to separate columns
separator = " ; "
#this function creates a table with the desired parameters and respective datatypes
#   and approperatly saves it to disk so it can be quereied later
def make_table(database_name, table_name, param_list, type_list):
    #open a new file
    try:
        table_file = open("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt", "x")
        temp = ""
        for x in param_list:
            temp += str(x)
            temp += separator
        table_file.write(temp + "\n")
        temp = ""
        for x in type_list:
            temp += str(x)
            temp += separator
        table_file.write(temp + "\n")
        table_file.close()
    except:
        print("Failed to create table " + table_name + " because it already exists.")

#loads an existing specified table from it's data stored on disk
def load_table(database_name, table_name):
    try:
        table_file = open("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt", "r")
        list_of_lists = []
        lines = table_file.readlines()

        #table metadata
        list_of_lists.append((lines[0].split(separator))[:-1])
        list_of_lists.append((lines[1].split(separator))[:-1])

        #verify the table contains data other than the metadata
        if(len(lines) > 2):
            #table data
            for x in range(2, len(lines)):
                token_list = lines[x].split(separator)
                #pop off the newline token
                token_list.pop()
                for x in range(0, len(token_list)):
                    #if it is NULL value then disregard the check when loading
                    if(token_list[x] == "NULL"):
                        pass
                    #convert to char
                    elif(list_of_lists[1][x] == "char"):
                        try:
                            token_list[x] = token_list[x]
                        except:
                            print("Char conversion Error")
                            return False
                    #convert to int
                    elif(list_of_lists[1][x] == "int"):
                        try:
                            token_list[x] = int(token_list[x])
                        except:
                            print("could not convert to int: " + token_list[x])
                            return False
                    #convert to float
                    elif(list_of_lists[1][x] == "float"):
                        try:
                            token_list[x] = float(token_list[x])
                        except:
                            print("could not convert to float: " + token_list[x])
                            return False
                    #o.w. its a varchar and nothing should be doen to modify x
                #add the properly converted tuple to the list of lists
                list_of_lists.append(token_list)
        table_file.close()
        return list_of_lists
    except:
        #print("Failed to load data from " + table_name)
        return []
#function responsible for saving the two dimensional list to the table file with
#   appropriate formating
def save_table(database_name, table_name, list_of_lists):
    try:
        table_file = open("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt", "w")
        for l in list_of_lists:
            temp = ""
            for element in l:
                temp += str(element)
                temp += separator
            table_file.write(temp+ "\n")
        table_file.close()
    except:
        print("Table modifications' failed to save.")

#prints all attributes/datatypes and thier values that are in the specified table
#   if it exists
def print_table_attributes(database_table):
    temp = ""
    for x in range(0, len(database_table[0])):
        temp = temp + database_table[0][x] + " "
        temp += database_table[1][x]
        temp += "|"
    #removes the last "|" which is unecessary through splicing
    temp = temp[:-1]

    print("\n\n" + temp)

    if(len(database_table) > 2):
        for x1 in range(2, len(database_table)):
            temp = ""
            for x2 in range(0, len(database_table[0])):
                data_value = database_table[x1][x2]
                #check if the data value is a string
                if(isinstance(data_value, str)):
                    if(data_value == "NULL"):
                        data_value = ""
                    else:
                        #if it is then remove the "'" surrounding the actual string value
                        data_value = data_value.replace("'", "")
                else:
                    data_value = str(data_value)
                temp = temp + data_value + "|"
            #removes the last "|" which is unecessary through splicing
            temp = temp[:-1]
            print(temp)
    print("")

#complete
#rightmost appending of added attribute, and adds the desired atribute/datatype
#   to the specified table in the specified database
def add_table_attribute(database_name, table_name, attribute, data_type):
    #loads the table from disk
    database_table = load_table(database_name, table_name)
    #checks if the attribute is already in the list of attributes
    if attribute in database_table[0]:
        print("Attribute already present in table " + table_name)
        return False
    else:
        #add attribute to the list of attributes
        database_table[0].append(attribute)
        #add the attribut's data type to list of data types
        database_table[1].append(data_type)

        #add temporary NULL values
        for x in range(2, len(database_table)):
            database_table[x].append("NULL")

        save_table(database_name, table_name, database_table)
        return

#complete, with the added removing of \t and \n to the pre parsing filtering
#adds the desired tuple to the database table
def add_tuple(database_name, table_name, param_list):
    param_types = get_param_type(database_name, table_name)
    #check if table was able to be loaded
    if(param_types == []):
        return False
    #check that the number of parameters is equal to the param_list given
    if(len(param_list) != len(param_types)):
        print("Given parameters does not mach number of parameters in table " + table_name)
        return False
    #goes through each of the parameters
    for x in range(0, len(param_types)):
        #if a value in the tuple is the NULL value then do nothing
        if(param_list[x] == "NULL"):
            pass
        #convert to char
        elif(param_types[x] == "char"):
            try:
                param_list[x] = param_list[x][0]
            except:
                print("Char conversion Error")
                return False
        #convert to int
        elif(param_types[x] == "int"):
            try:
                param_list[x] = int(param_list[x])
            except:
                print("could not convert to int: " + param_list[x])
                return False
        #convert to float
        elif(param_types[x] == "float"):
            try:
                param_list[x] = float(param_list[x])
            except:
                print("could not convert to float: " + param_list[x])
                return False
        else:
            try:
                #remove ')' and then split string based on presence of '('
                temp_list = ((param_types[x])[:-1]).split("(")
                #check if cur string is larger than the max size allower for varchar
                #if it is make the appropriate reduction
                #if not then do nothing to it
                if(int(temp_list[1]) < len(param_list[x])):
                    param_list[x] = param_list[x][:int(temp_list[1])]
            except:
                #if this fails then it is not a var char and since all other valid typer have bee
                #   trried it is not a valid type
                print("Not a valid datatype")
                return False
    #add converted record to the table
    #database_table.append(param_list)
    
    #save table to disk
    append_to_table(database_name, table_name, param_list)    
    return True    

#gets only the tables parameters
def get_param_type(database_name, table_name):
    try:
        table_file = open("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt", "r")
        param_line = table_file.readline()
        param_line = table_file.readline()
        table_file.close()
        return param_line.split(separator)[:-1]
    except:
        print("Unable to get metadata from " + table_name)
        return []

#complete
#appends the desired tuple to the table's respective file
def append_to_table(database_name, table_name, param_list):
    try:
        table_file = open("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt", "a")
        temp = ""
        for element in param_list:
            temp += str(element)
            temp += separator
        table_file.write(temp+ "\n")
        table_file.close()
    except:
        print("Table addition failed to save.")

#deletes the specified table file from the database by removing it from 
#   the appropriate directory
def remove_table(database_name, table_name):
    if os.path.exists("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt"):
        #remove the specific table's file from the database's directory
        os.remove("databases/" + database_name.lower() + "/" + table_name.lower() + ".txt")
        #remove table form database's table list
        return True
    else:
        return False

#checks if the specified table in the specified directory exists on disk
def table_exists(database_name, table_name):
    if os.path.exists("databases/"+ database_name.lower() + "/" + table_name.lower() + ".txt"):
        return True
    else:
        return False

#deletes all records with indecies correspoding to numbers in the record_numbers list
def delete_record(some_table, record_numbers):
    #if empty then there is nothing to delete, therefore return
    if(record_numbers == []):
        return
    
    record_numbers.sort(reverse=True)
    #deletes in descending order allowing us to remove elements, without effecting the other elements
    # that will be removed later on
    for x in record_numbers:
        del some_table[x]

#generates a list of indexes in the table list that corresponds to records that pass the given
#   relational arguments which can be thought of as a varname, symbol, and value(this could be updated to also include variables)
def index_list_generator(some_table, relational_args):
        indexes_that_contain = []

        #initial run of all elements in the table
        index = some_table[0].index(relational_args[0])

        convert_int_and_float(some_table[1][index], relational_args)

        for x in reversed(range(2, len(some_table))):
            if(relational_args[1] == "="):
                if(some_table[x][index] == relational_args[2]):
                    indexes_that_contain.append(x)
            elif(relational_args[1] == "<"):
                if(some_table[x][index] < relational_args[2]):
                    indexes_that_contain.append(x)
            elif(relational_args[1] == ">"):
                if(some_table[x][index] > relational_args[2]):
                    indexes_that_contain.append(x)
            elif(relational_args[1] == "<="):
                if(some_table[x][index] <= relational_args[2]):
                    indexes_that_contain.append(x)
            elif(relational_args[1] == ">="):
                if(some_table[x][index] >= relational_args[2]):
                    indexes_that_contain.append(x)
            elif(relational_args[1] == "!="):
                if(some_table[x][index] != relational_args[2]):
                    indexes_that_contain.append(x)
        #remove the relation just computed
        relational_args = relational_args[3:]
        while(relational_args != []):
            if(relational_args[0].lower() == "and"):

                index = some_table[0].index(relational_args[0])

                convert_int_and_float(some_table[1][index], relational_args)

                relational_args = relational_args[1:]
                for x in reversed(range(0, len(indexes_that_contain))):
                    if(relational_args[1] == "="):
                        if(not(some_table[indexes_that_contain[x]][index] == relational_args[2])):
                            del indexes_that_contain[x]
                    elif(relational_args[1] == "<"):
                        if(not(some_table[indexes_that_contain[x]][index] < relational_args[2])):
                            del indexes_that_contain[x]
                    elif(relational_args[1] == ">"):
                        if(not(some_table[indexes_that_contain[x]][index] > relational_args[2])):
                            del indexes_that_contain[x]
                    elif(relational_args[1] == "<="):
                        if(not(some_table[indexes_that_contain[x]][index] <= relational_args[2])):
                            del indexes_that_contain[x]
                    elif(relational_args[1] == ">="):
                        if(not(some_table[indexes_that_contain[x]][index] >= relational_args[2])):
                            del indexes_that_contain[x]
                    elif(relational_args[1] == "!="):
                        if(not(some_table[indexes_that_contain[x]][index] != relational_args[2])):
                            del indexes_that_contain[x]
            #remove the relation just computed
            relational_args = relational_args[3:]
        return indexes_that_contain

def convert_int_and_float(data_type, relational_args):
    if(data_type == "int"):
        relational_args[2] = int(relational_args[2])
    elif(data_type == "float"):
        relational_args[2] = float(relational_args[2])

def update_records(some_table, indexes_to_be_updated, values_to_set):
    #go through each
    for x in indexes_to_be_updated:
        #itterate through each parameter name
        for y in range(0, len(some_table[0])):
            #find param name in list of vallues we're updating
            if some_table[0][y] in values_to_set:
                try:
                    some_table[x][y] = helper.convert_token(some_table[1][y], 
                        values_to_set[values_to_set.index(some_table[0][y]) + 2])
                except:
                    print("Invalid datatype")
            #o.w. do nothing for this parameter name

#this function removes all attributes in the provided table that are not in
#   the list of attributes to keep(must be a list)
def remove_all_other_columns(some_table, attributes_to_keep):
    #transpose the list for simple column operations
    temp_table = list(zip(*some_table))
    remove_list = []
    
    #reduce the attributes to keep to all be lowercase
    for i in range(len(attributes_to_keep)):
        attributes_to_keep[i] = attributes_to_keep[i].lower()
    
    #loops through each column
    for x in range(0, len(temp_table)):
        #check the attribute name and if it is in the attributes to keep
        if not(temp_table[x][0].lower() in attributes_to_keep):
            remove_list.append(x)

    delete_record(temp_table, remove_list)
    #transpose the table again
    temp_table = list(zip(*temp_table))

    #return the modified table
    return temp_table

#default function for joins that determines if the join is an inner, outer, or default, it then 
def binary_join(database_name, table_names, tokens):
    table_1_name = table_names[0]
    table_1_var = table_names[1]

    if(len(table_names) == 4):
        #strategy here is to perfrom the independent table evaluations
        # by generating intermediary token interverls to check for each table
        # then to join these already selected tables on the appropriate tokens
        table_2_name = table_names[2]
        table_2_var = table_names[3]

        table_1, table_2, join_on_args = build_prejoin_tables(database_name, table_1_name, table_1_var, table_2_name, table_2_var, tokens)
        return inner_join(table_1, table_1_var, table_2, table_2_var, join_on_args)
       
    #inner join
    elif(table_names[2].lower() == "inner" and table_names[3].lower() == "join"):
        #same strategy as default
        table_2_name = table_names[4]
        table_2_var = table_names[5]

        table_1, table_2, join_on_args = build_prejoin_tables(database_name, table_1_name, table_1_var, table_2_name, table_2_var, tokens)
        return inner_join(table_1, table_1_var, table_2, table_2_var, join_on_args)

    #left outer join
    elif(table_names[2].lower() == "left" and table_names[3].lower() == "outer" and table_names[4].lower() == "join"):
        table_2_name = table_names[5]
        table_2_var = table_names[6]

        table_1, table_2, join_on_args = build_prejoin_tables(database_name, table_1_name, table_1_var, table_2_name, table_2_var, tokens)
        return outer_join(table_1, table_1_var, table_2, table_2_var, join_on_args)
    #issue joining tables
    else:
        print("Error in binary")
        raise Exception("Invalid join operation: join type/syntax not supportted")

#builds and where selects the tables that will be used in a binary join
def build_prejoin_tables(database_name, table_1_name, table_1_var, table_2_name, table_2_var, tokens):
    table_1_args, table_2_args, join_on_args = helper.three_arg_lists(tokens, table_1_var, table_2_var)

    table_1 = load_and_whereselect(database_name, table_1_name, table_1_args)
    table_2 = load_and_whereselect(database_name, table_2_name, table_2_args)

    return table_1, table_2, join_on_args

#loads tables and perfroms where query on table to reduce its size, returns this where quered table
def load_and_whereselect(database_name, table_name, tokens):
    some_table = load_table(database_name, table_name)
    if(tokens != []):
        #take the set difference between all possible indicies and the indicies that pass the where conditions
        records_to_del = list(set(range(2, len(some_table))).difference(set(index_list_generator(some_table, tokens))))
        #remove the records that do not fit the where clause
        delete_record(some_table, records_to_del)
    return some_table

#inner join implementation that purly joins the specified tables on the spcified column arguments
def inner_join(table_1, table_1_var, table_2, table_2_var, join_on_args):
    joined_table = []
    #create joined table metadata
    joined_table.append(table_1[0] + table_2[0])
    joined_table.append(table_1[1] + table_2[1])
    
    for row_t1 in table_1[2:]:
        for row_t2 in table_2[2:]:
            temp_join_row = row_t1 + row_t2
            valid = valid_join(temp_join_row, table_1, table_1_var, table_2, table_2_var, join_on_args)
            #joined elements pass the provided arguments
            if(valid):
                joined_table.append(temp_join_row)
    return joined_table


#outer join implementation that purly joins the specified tables on the spcified column arguments
def outer_join(table_1, table_1_var, table_2, table_2_var, join_on_args, axis='left'):
    joined_table = []
    #create joined table metadata
    joined_table.append(table_1[0] + table_2[0])
    joined_table.append(table_1[1] + table_2[1])

    for row_t1 in table_1[2:]:
        valid_found = False
        for row_t2 in table_2[2:]:
            temp_join_row = row_t1 + row_t2
            valid = valid_join(temp_join_row, table_1, table_1_var, table_2, table_2_var, join_on_args)
            #joined elements pass the provided arguments
            if(valid):
                joined_table.append(temp_join_row)
                valid_found = True
        #if no valid join for this particular row in table 1, then add it anyways with null values
        if(not valid_found):
            null_list = []
            for ele in table_2[0]:
                null_list.append("NULL")
            joined_table.append(row_t1 + null_list)
    return joined_table

#function that takes a record and a list representing the columns to check the equivlancy of, returns wheter the specified columns are equal or not
def valid_join(temp_join_row, table_1, table_1_var, table_2, table_2_var, join_on_args):
    valid = True
    for arg in range(0, len(join_on_args), 3):
        left = join_on_args[arg]
        right = join_on_args[arg + 2]
        #left var is the var for table 1
        if(left[0].lower() == table_1_var.lower()):
            if(right[0].lower() == table_2_var.lower()):
                #left is table 1, right is table 2
                #gets index of table 1's element  and table 2's
                table_1_index = helper.abs_index(table_1[0], left[2:])
                #need to factor in len of tabe 1 to find proepr index in join
                table_2_index = len(table_1[0]) + helper.abs_index(table_2[0], right[2:])
                if(temp_join_row[table_1_index] != temp_join_row[table_2_index]):
                    valid = False
            else:
                #error
                pass
        #right var is the var for table 1
        elif(right[0].lower() == table_1_var.lower()):
            if(left[0].lower() == table_2_var.lower()):
                #left is table 2, right is table 1
                #gets index of table 1's element  and table 2's
                table_1_index = helper.abs_index(table_1[0], right[2:])
                #need to factor in len of tabe 1 to find proepr index in join
                table_2_index = len(table_1[0]) + helper.abs_index(table_2[0], left[2:])
                if(temp_join_row[table_1_index] != temp_join_row[table_2_index]):
                    valid = False
            else:
                #error
                pass
    return valid