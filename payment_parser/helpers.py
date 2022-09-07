import argparse
from functools import reduce
import os
import pandas as pd
from pprint import pformat
import re
from re import finditer
import unicodedata


def slugify(value):
    """
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase.
    Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('-_')


def get_start_end(search_key, block):
    """
    Searches for the start and end location of search_key in block.

    Args:
        search_key: the string segement to return index of
        block: the blob containing search_key and likely other text
    Returns:
        (start, end)
    """
    search_result = ""
    if bool(re.search(search_key, block)):
        search_result = str(str(re.split(search_key, block, flags=re.M)[1]).split()[0])
    return search_result


def parse_block_metadata(block):
    """
    Parse block for categorical information about the data.

    Args:
        block:(str) blob of text, containing metadata and a table
    Returns:
        (table_type, report_id, report_type, is_table_empty)
    """

    # Category of table
    if bool(re.search("CLEARING CYCLE [0-9]+ - ACKNOWLEDGEMENT", block)):
        table_type = 1
        table_id = "clearing_cycle_acknowledgment"
    elif bool(re.search("CLEARING CYCLE [0-9]+ - NOTIFICATION", block)):
        table_type = 2
        table_id = "clearing_notification"
    elif bool(re.search("CLEARING CYCLE [0-9]+ SUMMARY", block)):
        table_type = 3
        table_id = "clearing_cycle_summary"
    elif bool(re.search("CLEARING CYCLE [0-9]+", block)):
        table_type = 4
        table_id = "clearing_cycle"
    elif bool(re.search("CLEARING DAY TOTAL", block)):
        table_type = 5
        table_id = "clearing_day_total"
    else:
        table_type = 0
        table_id = "other"

    report_id = block.split(" ")[0]
    # Category of Report
    if report_id == "1IP727010-AA":
        report_type = 1
    elif report_id == "1IP727020-AA":
        report_type = 2
    elif report_id == "1IP728010-AA":
        report_type = 3
    elif report_id == "1IP142110-AA":
        report_type = 4
    else:
        report_type = 0

    #  Whether table has data
    if bool(re.search("NO DATA TO REPORT", block)):
        is_table_empty = 1
    else:
        is_table_empty = 0
    return table_id, table_type, report_id, report_type, is_table_empty


def append_meta_data_to_each_row(block_data, block_meta_data):
    """
    Append metadata about the data to each row in the data.

    Args:
        block_data: (dict) table data
        block_meta_data: (dict) table metadata

    Returns:
        Updated version of block_data, with values from block_meta_data.
    """
    my_new_block = {}
    for col, val in block_data.items():
        my_new_block[col] = val
    for meta_col, meta_val in block_meta_data.items():
        my_new_block[meta_col] = meta_val
    return my_new_block


def parse_block_table_data(table_type, report_type, block, verbose):
    """
    Parses block for table data, using different parsing logic
        depending on the table_type and report_type.

    Args:
        table_type: (int) Category number for type of table
        report_type: (int) Category number for type of report
        block: (str) A blob of text
        verbose: whether to print every print statement
    Returns:
        A dictionary representation of the table's data.
    """
    result_dict = {}
    regex_empty_line = r'^[\s]+$'
    searchcols = r'[-]{2,}|[_]{2,}'
    raw_lines = block.split('\n')
    line_count = len(raw_lines)
    col_count = 0
    col_start_line_index = 99
    table_start_line_index = 99
    table_end_line_index = line_count
    col_start_end = []
    empty_line_numbers = []
    hypen_line_numbers = []

    if report_type == 0:
        print("Bad Report:" + str(block))
        return
    # Find empty lines
    for i in range(line_count):
        if bool(re.search(regex_empty_line, str(raw_lines[i]), flags=re.M)):
            empty_line_numbers.append(i)
    empty_line_count = len(empty_line_numbers)

    # Find lines containing "--" or "__"
    for i in range(line_count):
        if bool(re.search(searchcols, str(raw_lines[i]))):
            hypen_line_numbers.append(i)
    hypen_line_count = len(hypen_line_numbers)

    # Find the first empty line after hyphen line, which denotes start of data
    if hypen_line_numbers:
        for i in range(empty_line_count):
            if (hypen_line_numbers[0] - empty_line_numbers[i]) < 5 and (
                    hypen_line_numbers[0] - empty_line_numbers[i]) > 0:
                table_start_line_index = empty_line_numbers[i]
                break
        col_start_line_index = hypen_line_numbers[0]

    # Fetch column count by looping over hyphen lines
    for i in range(line_count):
        if bool(re.search(searchcols, str(raw_lines[i]))):
            for match in finditer(searchcols, str(raw_lines[i])):
                col_start_end.append(match.span())
                col_count = col_count + 1

    # If there are multiple hyphen lines, then we only need to consider first
    if hypen_line_count > 1:
        col_start_end = col_start_end[:int(len(col_start_end) / hypen_line_count)]
        col_count = int(col_count / hypen_line_count)

    col_names = [""] * col_count
    for colum_idx in range(col_count):
        for line_num in range(table_start_line_index, col_start_line_index):
            if line_num not in empty_line_numbers and 0 <= line_num < line_count:
                start = int(col_start_end[colum_idx][0])
                end = int(col_start_end[colum_idx][1])
                col_names[colum_idx] = raw_lines[line_num][start:end]

    data_rows = range(col_start_line_index + 1, table_end_line_index)
    col_names = [slugify(col) for col in set(col_names)]
    col_count = len(col_names)
    for i in range(col_count):
        result_dict[col_names[i]] = {}
    if verbose:
        # print(raw_lines)
        print(f"Line Count:                           {line_count}")
        print("=======================" * 6)
        print(f"Hyphen Line Numbers:                  {hypen_line_numbers}")
        print("=======================" * 6)
        print(f"Empty Line Numbers:                   {empty_line_numbers}")
        print("=======================" * 6)
        print("Column Indexes:")
        for col_idx in range(len(col_names)):
            print("\t- " + f"{col_start_end[col_idx]} {col_names[col_idx]}")
        print("=======================" * 6)
    # CLEARING CYCLE 001 - ACKNOWLEDGEMENT
    if table_type == 1:
        for col_idx in range(col_count):
            for row_num in data_rows:
                if row_num not in empty_line_numbers and 0 <= row_num < empty_line_numbers[1]:
                    result_dict[col_names[col_idx].strip()][row_num] = raw_lines[row_num][
                                                   int(col_start_end[col_idx][0]):int(
                                                       col_start_end[col_idx][1])].strip()
                else:
                    break
    else:
        for colum_idx in range(col_count):
            for row_num in data_rows:
                if row_num not in empty_line_numbers and 0 <= row_num < line_count:
                    result_dict[col_names[colum_idx].strip(), row_num] = raw_lines[row_num][
                                                   int(col_start_end[colum_idx][0]):int(
                                                       col_start_end[colum_idx][1])].strip()
                else:
                    break
    return result_dict


def parse_doc(file, output_dir, split_term, verbose):
    """
    Loop over the file,
    parse each section into a dataframe,
    write the dataframe to a csv.

    Args:
        file: input file to parse
        output_dir: where to save parsed csvs
        verbose: whether to print every print statement
        split_term: word used to split file into chunks
    Returns:
        List of output file details [Filepath, table_name, report_name]
    """
    results = []
    meta_cols = [
        "BUSINESS SERVICE ID:",
        "FILE ID:",
        "MEMBER ID:",
        "PAGE NO:",
        "RUN DATE:",
        "ACCEPTANCE BRAND:",
        "BUSINESS SERVICE LEVEL:",
        "RUN TIME:",
        "CURRENCY CODE :",
        "PAGE NO:",
    ]
    with open(file, "r") as f:
        lines = f.read()
    # Split on start of line, if line contains split_term
    pattern = re.compile(r'\n(?=^.+?' + split_term + ')', re.MULTILINE)
    blocks = pattern.split(lines)
    for idx in range(0, len(blocks)):
        block = blocks[idx]
        table_id, table_type, report_id, report_type, is_table_empty = parse_block_metadata(block)
        details = f"Block: {idx + 1}/{len(blocks)}, Report: {report_id}, Table type: {str(table_type)}"
        if verbose:
            print(block)
            print("=======================" * 6)
            print(details)
            print("=======================" * 6)
        else:
            print(details)

        if 0 in (table_type, report_type):
            print("*****    Table or Report Type Undefined for block above.")
            continue
        if is_table_empty == 1:
            print("*****   No data found in block above.")
            continue
        block_meta = {"REPORT": report_id}
        for meta_column in meta_cols:
            block_meta[meta_column] = get_start_end(meta_column, block)
        raw_result = parse_block_table_data(table_type, report_type, block, verbose)
        cleaned_result = {}
        for key in raw_result.keys():
            if type(key) == tuple:
                if key[0] not in cleaned_result:
                    cleaned_result[key[0]] = {}
                cleaned_result[key[0]][key[1]] = raw_result[key]
            else:
                cleaned_result[key] = raw_result[key]
        if cleaned_result:
            full_result = append_meta_data_to_each_row(cleaned_result, block_meta)
            df = pd.DataFrame(full_result)
            filename = os.path.join(output_dir, f"block_{idx+1}.csv")
            df.to_csv(filename, index=None)
            results.append([filename, table_id, report_id])
            if verbose:
                print(pformat(full_result))
                print("=======================" * 6)
                print(df)
                print("=======================" * 6)
        else:
            print("*****    No data found in block above.")
            if verbose:
                print("=======================" * 6)
    return results
