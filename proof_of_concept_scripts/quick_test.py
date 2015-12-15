# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:50:25 2015

@author: bethanygarcia
"""

my_list = [1,2,5,6,7,9,10]
offset = 3

#if offset == 2:
    
    
#if offset == 3:


tuple_test = zip(new_list, new_list[1:], new_list[2:])

#for i in range(1, offset):
#    this_slice = offset - i
#    print this_slice

#slices = [new_list[offset-i for i in range(1,offset):]]
 
''' 
if offset == 2:
    working_list = zip(my_list, my_list[1:])
    min_diff = min(y-x for x, y in working_list)
    print min_diff
    
if offset == 3:
    working_list = zip(my_list, my_list[1:], my_list[2:])
    working_list    
    min_diff = min(z-x for x, y, z in working_list)
    print min_diff    
 '''   
''' 
if self.sequence == 2:
          working_list = zip(self.num_list, self.num_list[1:])
          self.answer = min(y-x for x, y in working_list)

if self.sequence == 3:
    working_list = zip(self.num_list, self.num_list[1:], self.num_list[2:])
    self.answer = min(z-x for x, y, z in working_list)
'''


class SmallestDifference(object):
    def __init__(self, num_list, k):
        self.num_list = sorted(num_list)
        self.sequence = k
        self.answer = 1
        
        min_difference = max(num_list) - min(num_list)
        
        for i in range(len(self.num_list)+(self.sequence)):
            current_slice = tuple(self.num_list[i:i+self.sequence])    
            
            if len(current_slice) == self.sequence:
                current_min = max(current_slice) - min(current_slice)
                
                if current_min < min_difference:
                    min_difference = current_min                
            else:
                continue
            
        self.answer = min_difference
            
        
 
    
first_test = SmallestDifference([1,2,3,4,5], 2)
second_test = SmallestDifference([10,20,30,100,101,103,200], 3)
third_test = SmallestDifference([1,2,5,6,7,9,10], 3)
fourth_test = SmallestDifference([500, 600, 1000], 2)

print first_test.answer
print second_test.answer
print third_test.answer
print fourth_test.answer

'''
    def testOne(self):
        sd = SmallestDifference([1,2,3,4,5], 2)
        self.assertEqual(1, sd.answer)
        
    def testTwo(self):
        sd = SmallestDifference([10,20,30,100,101,103,200], 3)
        self.assertEqual(3, sd.answer)

    def testThree(self):
        sd = SmallestDifference([1,2,5,6,7,9,10], 3)
        self.assertEqual(2, sd.answer)
        
    def testFour(self):
        sd = SmallestDifference([500, 600, 1000], 2)
        self.assertEqual(100, sd.answer)
        
        
        
        if current_min < min_difference:
            self.answer = current_min'''