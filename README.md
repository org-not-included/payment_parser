# Parser_For_Payment_Files  
Parses a payments file with multiple blocks of data into individual csvs.  
  
## The payments file is:  
- Stored in fixed-width format  
- Contains hyphen line for calculating column widths  
- Can be split into blocks of text on a `split_term`  
  
  
## Sample Command Usage:  
```text
python3 payment_parser --file payment_parser/T140_sample.txt --output_dir="payment_parser/output/" --verbose=False
```  
  
  
## Sample Command Output:  
```text
File: T140_sample.txt, Split Term: MASTERCARD WORLDWIDE, Output Dir: output/, Verbose: False
Block: 1/13, Report: 1IP727010-AA, Table type: 1
*****    No Data to Report.
Block: 2/13, Report: 1IP727020-AA, Table type: 2
Block: 3/13, Report: 1IP727020-AA, Table type: 2
Block: 4/13, Report: 1IP727020-AA, Table type: 2
Block: 5/13, Report: 1IP727020-AA, Table type: 2
Block: 6/13, Report: 1IP727020-AA, Table type: 2
Block: 7/13, Report: 1IP727020-AA, Table type: 2
Block: 8/13, Report: 1IP728010-AA, Table type: 4
Block: 9/13, Report: 1IP728010-AA, Table type: 4
Block: 10/13, Report: 1IP728010-AA, Table type: 3
Block: 11/13, Report: 1IP728010-AA, Table type: 3
Block: 12/13, Report: 1IP728010-AA, Table type: 3
Block: 13/13, Report: 1IP728010-AA, Table type: 5
```  
  