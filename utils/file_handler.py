def read_sales_file(path):
    try:
        with open(path, "r", encoding="latin-1") as f:
            return f.readlines()
    except Exception as e:
        print("Error reading file:", e)
        return []


def write_output(filename, content):
    try:
        with open(f"output/{filename}", "w") as f:
            f.write(content)
    except Exception as e:
        print("Error writing file:", e)
