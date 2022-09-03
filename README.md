# Payment Parser  
Parses a payment file, with multiple blocks of data, into individual CSVs.  
  
## The payments file is
- Stored in fixed-width format  
- Contains hyphen line for calculating column widths  
- Can be split into blocks of text on a `split_term`  

## Installation
```text
pip3 install payment-parser
```

## Example Code Usage:
```Python3
from payment_parser import parse_doc
parse_doc(
    file="payment_parser/T140_sample.txt", 
    output_dir="payment_parser/output/", 
    split_term="MASTERCARD WORLDWIDE", 
    verbose=True,
)
```

## Example CLI Usage:
```text
payment_parser --file "payment_parser/T140_sample.txt" --output_dir "payment_parser/output/" --verbose=False
```  
  
  
### CLI Output:  
```text
File: payment_parser/T140_sample.txt, Split Term: MASTERCARD WORLDWIDE, Output Dir: payment_parser/output/, Verbose: False
Block: 1/13, Report: 1IP727010-AA, Table type: 1
*****   No data found in block above.
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

## Help/Docs Usage:
```text
payment_parser --help                                                                                     
```

### Help/Docs Output:
```text
usage: payment_parser [-h] [--file FILE] [--output_dir OUTPUT_DIR] [--split_term SPLIT_TERM] [--verbose VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           The absolute path of the file to parse.
  --output_dir OUTPUT_DIR
                        The absolute folder path for saving the parse results.
  --split_term SPLIT_TERM
                        Word or phrase used to split file into chunks.
  --verbose VERBOSE     Whether to enable extra logging.
```