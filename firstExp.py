import os
# This is the class which helped me learn the first commands in python
# I have background in Java and C
print("hello world")
message = 'Hello there'
print(message)
# we can use slicing- by using the format "include : not include"
# we will get the content of the string strarting on the index to index
print(message[1:-1])  # will result "ello ther"
# we can use replace in a string:
message = message.replace('there', 'universe')
print(message)
# we can combine strings into a long string by setting a format with curled brackets:
# by using the syntax: "str = '{..1..},{..2..}'.format(1,2)
firstname = 'nadav'
lastname = 'pld'
fullname = ('first name: {} \nlast name: {}').format(firstname, lastname)
print(fullname)
# results in first name:nadav last name: pld
# we can do the same thing with an f_string, which is using a string in format way without the .format like this-
fullnameF = f'firstname: {firstname} lastname: {lastname}'
print(fullnameF)
# results the same(except the \n)"

# Numeric attributes
print(3 / 2)  # note that the result is 1.5, and not 1 as we are used to
print(3 // 2)  # this is a whole division, will result 1

# casting:
str1 = '100'
str2 = '200'
print(int(str1) + int(str2))  # results "300"

# lists: the syntax is "listName = [content1, content2,]..."
# we can "extend" lists by listName.extends(secondListName):
list1 = ['a', 'b', 'c']
print(list1)
list2 = ['A', 'B']
list1.extend(list2)
print(list1)  # results ['a', 'b', 'c', 'A', 'B']
# we can add an obj to a list with "append", which will add the object as an object(for example if we append a list,
# the last object will be the whole list)
# print(list1.extend(list2))
# there are many builtin methods for lists: max/min/sum/sorted(lst), all of the gets and returns as you think
# also, we can just sort the list object itself(instead of getting a sorted instance)
# by using: list1.sort, or list1.sort(reverse=True) to get a reveresed order
# index of: by using list1.index("to_find") we will get the index of the obj, or an error if it doesnt exist
# to check if it appears in the list we use the boolean syntax:
# ("obj" is in list_name) will result True/False

# ##     Tuples   ####
# Tuples are immutable object like list. the diffrence is in the syntax,
# While lists are using square brackets, tuples uses curled ones:

# sets - values unordered, no duplicateds (set like in logics course)
# we make a set by using {} brackets
# as the name suggests, it has function like:
# set1.intersection(set2) and set1.difference(set2), union, and more

# important: making an empty set is by the syntax: empty_set = set()
# if we use "empty_set = {}" we will get an empty dict.

# Dict - are hash maps, defined by keys(number/strings) and value of the key
# we can access all keys, all value, specific key or specifi valuse:
student = {'name': 'Nadav', 'lastname': 'pld', 3: "likes programing"}
print(student.keys())
print(student.values())
print(student.pop(3))
print(student)
print("see how the 3rd key is missing because we poped it? now we will add it back")
student[3] = "likes program"
print(student)

# Loops:
nums = [1, 2, 3, 4, 5]
# for num in nums:
#   print(num)

for num in nums:  # sing continue skips to the next iteration
    if num == 3:
        continue
    print(num)   # if we used a "break" than it would stop the loop for

# if we want a java style loop with indexing we can use:
for i in range(5):
    print(i)
    print('i*10 is ' + str(i*10) )
# if we want to satrt in diffrent index then we do
for i in range (2,5):
    print(i) #results printing 2,3,4

print(os.__file__)