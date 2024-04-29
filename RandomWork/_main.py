#names = ["Bob", "Steve", "Ellen", "Joshua", "jose", "Adam"]
#names[-1] = "Amy"
'''
names.append("Ashton")
print(names[6])
'''

'''
names.pop(2)
print(names)
'''

'''
names2 = ["Ashton" , "Nick"]
names.extend(names2)
print(names)
'''

'''
print(len(names))
'''

'''
if "Bob" in names:
    print("bob is in names")
else:
    print("bob is not in names")
'''

'''
studentIDs = {"Bob" : 1234,
              "Steve" : 1235,
              "Ellen" : 1236}

print("Steves id is" , studentIDs["Steve"])

#flow control
for i in range(0, len(names)):
    print("Value of I ", i)
    print(names[i])
    '''
#///////////////////////////////////////////////////////////////

#contiunes
#breaks
#in a function if you use *args inside of the requirements then you can turn in anything forever
#in a function if you use **kwargs inside of the requirements then you can define variables in the function call
#then use it to define something by using 'local variable' = kwargs["name of variable"]
names = ["Steve", "Adam","Bob","Ellen"]

for name in names:
    if name == "Bob":
        print("i find bob")
        break
    else:
        print("i am still looking for bob")

ids = {"Bob":1234, "Steve":11235, "Adam":1236, "Ellen":11237}

for name, id in ids.items():
    if id > 10000:
        continue # move on to the next loop
    ids[name] += 10000

print(ids)
