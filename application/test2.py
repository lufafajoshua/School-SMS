subjects = ["chemistry", "Biology", "physics"]
requirements = ["History", "chemistry"]
test = ['Biology', 'Chemistry', 'Submath']#Requirements
lst = ['Chemistry', 'Biology', 'Submath', 'Economics ']#Result subjects
for i in test:
    print("{}".format(i))

for i in test:
    if i in lst:
        print(True) 
        #break#Stop if true when there is a choice found in the 
    else:
        print("False") 

for i in requirements:
    if i in subjects:
        print(True) 
        #break#Stop if true when there is a choice found in the 
    else:
        print("False")  

points = float(1.2)
err = float(4.7)
you = float(2.1)
list = [points, err, you]

total = sum([i for i in list])
print(total)
stu = [1.2, 6.7, 9.8, 3.5]
print(sum([k for k in stu]))
