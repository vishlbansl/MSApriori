# IMPLEMENTATION OF MSAPRIORI ALGORITHM (EXCLUDING RULE GENERATION) 

## Group Memebers:
  1.	Ahmed Metwally (UIN: 678120810)  
  2.	Vishal Bansal (UIN 669773290)  

## Description:
	
The Msapriori algorithm works in two steps:
1.	Generate all frequent item sets; A frequent itemset is an itemset that has transaction support above MIS(minimum item support).
2.	Eliminate the items that do not fulfil the given constraints like SDC, Cannot-be-together and Must-have

## Getting Started:

### Prerequisites:
Python >3.6 must be installed.

### Testing and Running:
```
python3 CS583_MSApriori_v0.8.py -i inputdata3.txt -p parameters3.txt -o text_piazza_input3_3.txt
```
•	To run the pyhton script- pyhton ahmedvihsal.py
•	2. To read the input file-  i inputdata.txt
•	3. To read the paramemeters file- p parameters.txt
•	4. to save the out put file- o output.txt

### Implementation Notes:
In output.txt file, Tailcount for any listed frequent k-itemset is the count of that individual item which has maximum MIS.




## Example 
```
python3 ahmed_vishal.py -i data/inputdata3.txt -p data/parameters3.txt -o test.txt
```