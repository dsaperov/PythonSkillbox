class Parent:
    class_var_1 = 12
    __class_var_3 = 34

    def print_hidden_attr(self):
        print(self.__class_var_3)


class Child(Parent):
    # __class_var_3 = 43

    def print_hidden_attr(self):
        print(self.__class_var_3)


my_object = Parent()
my_object1 = Child()

# print(my_object1._Parent__class_var_3)

print(dir(my_object1))

# class MyClass:
#     __attribute = 'value'
#
#
# my_object = MyClass()
# print(my_object._MyClass__attribute)