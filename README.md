# Implementation of MSApriori Algorithm (Excluding rule generation) 

## Group Memebers:
  1.	Ahmed Metwally (UIN: 678120810)  
  2.	Vishal Bansal (UIN: 669773290)  

## Description:
	
The Msapriori algorithm works in two steps:

1.	Generate all frequent item sets; A frequent itemset is an itemset that has transaction support above MIS(minimum item support).  
2.	Eliminate the items that do not fulfil the given constraints like SDC, Cannot-be-together, and Must-have. 

## Getting Started:

### Prerequisites:
* Python >3.6 must be installed.

### Installing, Testing and Running:

Clone the project to your local repository:
```
git clone git@bitbucket.org:ametwally/msapriori.git
```

Navigate to the project directory:
```
cd msapriori/
```

To execute the program from command line, use:
```
python3 ahmed_vishal.py -i <input-file.txt> -p <parameters-file.txt> -o <output-filet.txt>
```

### Example:
```
python3 ahmed_vishal.py -i data/inputdata3.txt -p data/parameters3.txt -o test.txt
```

### Implementation Notes:
* In the outputfile, the Tailcount for any listed frequent k-itemset is the count of the individual item which has the highest MIS.
