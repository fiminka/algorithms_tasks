import random as r
import math


class Vector:
    """
    This is a class Vector that makes simple calculations
    on vector(s) of given dimension.
    It has methods below:
        1. random_values
        2. from_list
        3. len_vec
        4. elem_sum
        5. scalar_prod
    And operators:
        1. add
        2. sub
        3. mul and rmul
        5. repr
        6. len
        7. getitem
        8. contains
    """
    def __init__(self, n = 3):
        """ 
        Creating a dimension and an empty list for values of the vector.
        :param n: (int) dimension(default value is 3).
        """
        self.list_values = []
        self.n = n 
        if self.n <= 0 or type(self.n) != int:
            raise ValueError("The dimension can't be less than 0 or other type than int.")

    def random_values(self):
        """ 
        Create n random values of vector.
        :return: (list) n-element vector/n-th dimension vector
        """
        for i in range(self.n):
            self.list_values.append(r.randint(-15, 15))
        return self.list_values
    
    def from_list(self, list1):
        """ 
        Create a vector with values from given list.
        :param list1: n-length list of int elements.
        :return: n-th dimension vector with elements from the given list.
        """
        if self.n == len(list1) and len(list1) != 0:
            for i in range(0, len(list1)):
                if type(list1[i]) == int:
                    self.list_values.append(list1[i])
                else:
                    raise ValueError("List should have int elements.")
            return self.list_values
        else:
            raise ValueError("List lenght should be same as vector dimension.")

    def __add__(self, other):
        """
        An operator that sums each value of the vector with another's.
        :param other: another vector from the class
        :return: (list) a new vector whose values are summed values of the given ones
        """
        if len(self.list_values) != len(other.list_values):
            raise ValueError("Can't add vectors of different dimensions.")
        else:
            vector = Vector()
            for el in range(self.n):
                vector.list_values.append(self.list_values[el] + other.list_values[el])
            return vector

    def __sub__(self, other):
        """
        An operator that subtracts each value of the vector with another's.
        :param other: another vector from the class
        :return: (list) a new vector whose values are summed values of the given vectors
        """
        if len(self.list_values) != len(other.list_values):
            raise ValueError("Can't subtract vectors of different dimensions.")
        else:
            vector = Vector()
            for el in range(self.n):
                vector.list_values.append(self.list_values[el] - other.list_values[el])
            return vector
        
    def __mul__(self, other):
        """
        An operator that multiplies each value of the vector by given scalar.
        :param other: (int) given scalar
        :return: multiplied vector
        """
        vector = Vector()
        mul_values = []
        for i in range(self.n):
            if type(other) is int:
                mul_values.append(other*self.list_values[i])
            else:
                raise ValueError("Scalar should be type int.")
        return vector.from_list(mul_values)

    def __rmul__(self, other):
        """
        An operator that multiplies each value of the vector by given scalar.
        :param other: (int) given scalar
        :return: multiplied vector
        """
        vector = Vector()
        mul_values = []
        for i in range(self.n):
            if type(other) is int:
                mul_values.append(other*self.list_values[i])
            else:
                raise ValueError("Scalar should be type int.")
        return vector.from_list(mul_values)
    
    def vec_len(self):
        """ 
        Returns length of the vector(Euclidean formula).
        """
        if len(self.list_values) != 0:
            return math.sqrt(sum(el**2 for el in self.list_values))
        else:
            raise ValueError("Vector has no values.")
    
    def elem_sum(self):
        """ 
        Returns sum of all elements of the vector.
        """
        return sum(el for el in self.list_values)
    
    def scalar_prod(self, Vector2):
        """ 
        Calculates the sum of multiplications the products of the corresponding entries of the two sequences of number.
        :param Vector2: another vector from the class
        :return: dot product of given vectors
        """
        vec_scal = 0
        if self.n != Vector2.n:
            raise ValueError("Can't calculate dot product vectors of different dimensions.")
        elif len(self.list_values) == 0:
            return 0
        else:
            for i in range(self.n):
                vec_scal += (self.list_values[i] * Vector2.list_values[i])
            return vec_scal

    def __repr__(self):
        return str(self.list_values)
    
    def __getitem__(self, item):
        """
        An operator that gets a value on given index.
        :param item: (int) index of demanding value
        :return: demanding value
        """
        if type(item) == int and item in range(-self.n, self.n):
            return self.list_values[item]
        else:
            raise ValueError("Value type not int or value out of range.")
            
    def __contains__(self, item):
        """
        An operator that tells if given item is a value of the vector.
        :param item: (int) given value
        :return: True if item is a vector's value, False if not
        """
        if type(item) == int:
            if item in self.list_values:
                return True
            else:
                return False
        else:
            raise ValueError("Vector values should be int.")        
