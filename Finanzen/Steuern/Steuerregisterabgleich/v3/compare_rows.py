import sys
import pandas as pd

# Script usage: python compare_rows.py <file1> <file2> <key_column> <value_column>

if __name__ == "__main__":
    # Get args
    if len(sys.argv) != 5:
        print("Usage: python compare_rows.py <file1> <file2> <key_column> <value_column>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    key_column = sys.argv[3]
    value_column = sys.argv[4]

    # Read files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Create dicts
    dict1 = dict(zip(df1[key_column], df1[value_column]))
    dict2 = dict(zip(df2[key_column], df2[value_column]))

    # Compare dicts
    for key, value in dict1.items():
        if key in dict2:
            if value != dict2[key]:
                print(f"Row {key} has different values: {value} and {dict2[key]}")
        else:
            print(f"Row {key} is not in file2")

    # Export a list of all keys whose values are different
    keys = []

    for key, value in dict1.items():
        if key in dict2:
            if value != dict2[key]:
                keys.append(key)

    df_keys = pd.DataFrame(keys, columns=[key_column])

    df_keys.to_excel("different_values.xlsx", index=False)

    print("Done")

