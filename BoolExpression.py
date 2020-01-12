class BooleanExpression:

    class BoolExprError(Exception):pass
    #operators ordered from highest to lowest priority
    #!or is an OR with a higher priority as an AND
    #!and has a higher priority as an 1or
    #as if it were surrounded by ()
    operators_by_priority = ["!and", "!or", "and", "or"]

    #------------- INTERNAL CLASS FUNCTIONS ---------------------
    def _evaluate_and(bool_array):
        """
        Evaluates the given logical boolean array.
        All elements are linked with a logical AND.

        Parameters:
        -----------
            bool_array: the list of bool values to evaluate

        Returns:
        --------
            True or False: if bool_array has at least one element
            None: if bool_array is empty
        """
        l = len(bool_array)
        if l > 1:
            if sum(bool_array) == l:
                return True
            else:
                return False
        elif l == 1:
            return bool_array[0]
        else:
            return None
    
    def _evaluate_or(bool_array):
        """
        Evaluates the given logical boolean array.
        All elements are linked with a logical OR.

        Parameters:
        -----------
            bool_array: the list of bool values to evaluate

        Returns:
        --------
            True or False: if bool_array has at least one element
            None: if bool_array is empty
        """
        l = len(bool_array)
        if l > 1:
            if sum(bool_array) == 0:
                return False
            else:
                return True
        elif l == 1:
            return bool_array[0]
        else:
            return None
        
    def _split_and_eval(bool_array, indices, operator):
        """
        Splits the expression at the given operators and evaluates the sub arrays.
        Example:
        --------
            BooleanExression._split_and_eval([True, False, True], ["!or", "and"])
            True !or False and True is equal to:
           (True  or False) and True
            True and True; after evaluating !or
            True; after evaluating and

        Parameters:
        -----------
            bool_array: a list of bool values
            indices: a list of all consecutive operator indices
            operator: the operator to evaluate

        Returns:
        --------
            list: new list of bool values, after operator was evaluated
        """
        new_arr = []
        last_index = 0
        for i, x in enumerate(indices):
            index, length, op = x
            if op == operator:
                if i > 0:
                    #add all elements from last index that were before the operator
                    new_arr += bool_array[last_index:index]
                #set last index to after the operators
                last_index = index + length + 1
                #exclude lowest priority operator(logical OR)
                if operator in BooleanExpression.operators_by_priority[0:-1]:
                    #evaluate the expression
                    if operator.find("or") != -1:
                        new_arr.append(BooleanExpression._evaluate_or(bool_array[index:last_index]))
                    elif operator.find("and") != -1:
                        new_arr.append(BooleanExpression._evaluate_and(bool_array[index:last_index]))
            elif i == len(indices)-1:
                #if the last element is not an operator
                #add all the elements from last index to the end of the array
                new_arr += bool_array[last_index:]
                break
        return new_arr

    def _create_indices(operator_array):
        """
        Creates an index list for a given operator list.
        Each index is the starting index for a sequence of the same operators.
        Example: (0, 1, "or")
        This index starts at 0 and has 1 "or" operator(s).

        Parameters:
        -----------
            operator_array: a list of operators(as strings)

        Returns:
        --------
            list: a list containing all indices for each operator sequence as a touple

        """
        indices = []
        count_op = 0
        count_other = 0
        if len(operator_array) > 0:
            last_op = operator_array[0]
            last_index = 0
            for i, x in enumerate(operator_array):
                if x != last_op:
                    indices.append((last_index, i-last_index, last_op))
                    last_op = x
                    last_index = i
            if last_index < len(operator_array)-1:
                indices.append((last_index, len(operator_array)-last_index, last_op))
            elif last_index == len(operator_array)-1:
                indices.append((last_index, len(operator_array)-last_index, last_op))
            return indices

    #-------------- INSTANCE FUNCTIONS ---------------
    def __init__(self, bool_array, operator_array):
        if len(bool_array)-1 != len(operator_array):
            raise BooleanExpression.BoolExprError("Length mismatch. Expression and operator length don't match.")
        self.bool_array = bool_array
        self.operator_array = operator_array

    def _debug_eval(self):
        """
        Evaluates the logical expression without changing the expression.
        FOR DEBUGGING PURPOSES, prints the individual steps

        Raises:
        -------
            BoolExprError: if lowest priority operator could not be resolved
                           if one step failed to create matching bool and operator lists
        """
        #exclude lowest priority operator
        bools = self.bool_array
        operators = self.operator_array
        print(self)
        for operator in BooleanExpression.operators_by_priority[0:-1]:
            if operator not in operators:
                #if the operator is not found, skip to the next one
                continue
            print("Eliminate: %s"%operator)
            #create indices for all operators
            #(index, length of consecutive operators, operator type)
            indices = BooleanExpression._create_indices(operators)
            #split array at the given operator and evaluate sub arrays
            bools = BooleanExpression._split_and_eval(bools, indices, operator)
            #remove the operators that were evaluated above
            operators = [op for op in operators if op != operator]
            print(BooleanExpression(bools, operators))
            if len(operators) == 0:
                #print("Zero Len:", bool_array)
                print("Zero Length: " + str(bools[0]))
        #eval lowest priority operator
        if BooleanExpression.operators_by_priority[-1].find("or") != -1:
            print("Result: " + str(BooleanExpression._evaluate_or(bools)))
        elif BooleanExpression.operators_by_priority[-1].find("and") != -1:
            print("Result: " + str(BooleanExpression._evaluate_and(bools)))
        else:
            raise BoolExprError("Couldn't evaluate lowest priority operator.")
        
    def evaluate(self):
        """
        Evaluates the logical expression without changing the expression.
        Example: True and False evaluates to False

        Raises:
        -------
            BoolExprError: if lowest priority operator could not be resolved

        Returns:
        --------
            bool: the boolean value the expression evaluates to
        """
        #exclude lowest priority operator
        bools = self.bool_array
        operators = self.operator_array
        for operator in BooleanExpression.operators_by_priority[0:-1]:
            if operator not in operators:
                #if the operator is not found, skip to the next one
                continue
            #create indices for all operators
            #(index, length of consecutive operators, operator type)
            indices = BooleanExpression._create_indices(operators)
            #split array at the given operator and evaluate sub arrays
            bools = BooleanExpression._split_and_eval(bools, indices, operator)
            #remove the operators that were evaluated above
            operators = [op for op in operators if op != operator]
            if len(operators) == 0:
                return bools[0]
        #eval lowest priority operator
        if BooleanExpression.operators_by_priority[-1].find("or") != -1:
            return BooleanExpression._evaluate_or(bools)
        elif BooleanExpression.operators_by_priority[-1].find("and") != -1:
            return BooleanExpression._evaluate_and(bools)
        else:
            raise BoolExprError("Couldn't evaluate lowest priority operator.")

    def __str__(self):
        """
        Prints a logical expression.

        Returns:
        --------
            str: a string representation of the logical expression

        """
        s = ""
        for value, operator in zip(self.bool_array, self.operator_array):
                s += " ".join([str(value), operator]) + " "
        s += str(self.bool_array[-1])
        return s.strip()
        

def bool_expression_from_string(s):
    def str2bool(s):
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            return None
    arr = s.split(" ")
    #all bools
    bools = [str2bool(x) for x in arr if x == "True" or x == "False"]
    #all logical operators
    operators = [x for x in arr if x.find("or") != -1 or x.find("and") != -1]
    return BooleanExpression(bools, operators)


if __name__ == "__main__":
    print("False and False == "+str(bool_expression_from_string("False and False").evaluate()))
    print("False and True  == "+str(bool_expression_from_string("False and True").evaluate()))
    print("True  and False == "+str(bool_expression_from_string("True and False").evaluate()))
    print("True  and True  == "+str(bool_expression_from_string("True and True").evaluate()))
    print("False or  False == "+str(bool_expression_from_string("False or False").evaluate()))
    print("False or  True  == "+str(bool_expression_from_string("False or True").evaluate()))
    print("True  or  False == "+str(bool_expression_from_string("True or False").evaluate()))
    print("True  or  True  == "+str(bool_expression_from_string("True or True").evaluate()))
    import random
    def rand_expression(length = 15):
        b = []
        o = []
        for x in range(length):
            n = random.randint(-128, 127)
            if n%3 == 1:
                b.append(True)
            else:
                b.append(False)
            if n%7 == 0:
                o.append("!or")
            elif n%5 == 2:
                o.append("!and")
            elif n%2 == 1:
                o.append("and")
            else:
                o.append("or")
        return BooleanExpression(b, o[0:-1])

    for m in range(1):
        print("-------- NEW EXPRESSION --------")
        expr = rand_expression()
        expr._debug_eval()
