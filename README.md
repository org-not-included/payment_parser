# Payment Parser  
Parses a payment file, with multiple blocks of data, into individual CSVs.  
  
## The payments file is
- Stored in fixed-width format  
- Contains hyphen line for calculating column widths  
- Can be split into blocks of text on a `split_term`  

## Installation
```text
python3 -m pip install payment-parser
```

## Example CLI Usage:
```text
python3 -m payment_parser --file "payment_parser/T140_sample.txt" --output_dir "payment_parser/output/" --verbose=False
```  
  
  
### CLI Output:  
```text
File: payment_parser/T140_sample.txt, Split Term: MASTERCARD WORLDWIDE, Output Dir: payment_parser/output/, Verbose: False
Block: 1/13, Report: 1IP727010-AA, Table type: 1
*****   No rows found in block above.
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

## Example Code Usage
```Python3
# from payment_parser.__main__ import parse_doc
from payment_parser import parse_doc
file = 'payment_parser/T140_sample.txt'
output_dir = "payment_parser/output/"
verbose = True
split_term = "MASTERCARD WORLDWIDE"
parse_doc(file, output_dir, split_term, verbose)
```