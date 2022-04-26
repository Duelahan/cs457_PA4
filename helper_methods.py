#Author: Tristan Bailey
#Date Created: 3/15/2022
#Last Modified: 4/26/2022
#Assignment: PA 4
#Class: CS457
#File: File for the table methods

#helper function: returns the index of the keyword in the list of tokens, or -1 if keyword is not present in tokens
def keyword_index(tokens, keyword):
    exit = False
    index = 0
    while(not(exit) and (index < len(tokens))):
        if (tokens[index].lower() == keyword.lower()):
            exit = True
        else:
            index += 1
    if(index >= len(tokens)):
        return -1
    else:
        return index

#helper fuinction that converts tokens(strings) into thier appropriate datatypes
def convert_token(data_type, token):
    #int conversion
    if(data_type == "int"):
        return int(token)
    #float conversion
    elif(data_type == "float"):
        return float(token)
    #char conversion
    elif(data_type == "char"):
        return str(token)[0]
    #varchar conversion
    else:
        try:
            #remove ')' and then split string based on presence of '('
            temp_list = ((data_type)[:-1]).split("(")
            #check if cur string is larger than the max size allower for varchar
            #if it is make the appropriate reduction
            #if not then do nothing to it
            if(int(temp_list[1]) < len(token)):
                return token[:int(temp_list[1])]
            else:
                return token
        except:
            raise Exception("Invalid datatype for conversion")

#takes in a list of tokens and the join variables for two tables
# it then creates and returns three lists, one comprised of arguments for the first table, one for arguments for the second table,
# and the third for the column equivlences to join on
def three_arg_lists(tokens, table_1_var, table_2_var):
    table_1_args = []
    table_2_args = []
    join_on_args = []
    #itterate through arguemnts by threes
    for arg in range(0, len(tokens), 3):
        left = tokens[arg]
        operator = tokens[arg + 1]
        right = tokens[arg + 2]
        #single table
        left_has_var = "." in left
        right_has_var = "." in right

        if(not(left_has_var and right_has_var)):
            #lhs var
            if(left_has_var):
                if(left[0].lower() == table_1_var.lower()):
                    table_1_args.append(left[2:])
                    table_1_args.append(operator)
                    table_1_args.append(right)
                elif(left[0].lower() == table_2_var.lower()):
                    table_2_args.append(left[2:])
                    table_2_args.append(operator)
                    table_2_args.append(right)
            #rhs var
            elif(right_has_var):
                if(left[0].lower() == table_1_var.lower()):
                    table_1_args.append(left)
                    table_1_args.append(operator)
                    table_1_args.append(right[2:])
                elif(left[0].lower() == table_2_var.lower()):
                    table_2_args.append(left)
                    table_2_args.append(operator)
                    table_2_args.append(right[2:])
            else:
                #invalid operation
                pass
        #join on because both sides have a var
        else:
            join_on_args.append(left)
            #join by definition uses '=' so here we enforce that
            join_on_args.append("=")
            join_on_args.append(right)
    return table_1_args, table_2_args, join_on_args

#gets the index of a string within a list regardless of the caseing in the list or the input string
def abs_index(string_list, desired_string):
    exit = False
    index = 0
    while(not exit):
        if string_list[index].lower() == desired_string.lower():
            exit = True
        elif index >= len(string_list):
            exit = True
            index = -1
        else:
            index += 1
    return index
