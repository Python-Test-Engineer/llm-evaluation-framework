import csv


def parse_seventh_column_to_dict(csv_file_path):
    """
    Parse CSV with pipe delimiter, extract 7th column and convert to dictionary
    """
    results = []

    with open(csv_file_path, "r") as file:
        # Use csv.reader with pipe delimiter
        reader = csv.reader(file, delimiter="|")

        for row in reader:
            if len(row) >= 7:  # Ensure row has at least 7 columns
                seventh_item = row[6]  # 7th item (0-indexed)

                # Parse the key=value pairs
                item_dict = {}
                pairs = seventh_item.split(" ")

                for pair in pairs:
                    if "=" in pair:
                        key, value = pair.split("=", 1)  # Split only on first =
                        # Remove quotes from values
                        value = value.strip("'\"")
                        item_dict[key] = value

                results.append(item_dict)

    return results


if __name__ == "__main__":

    results = parse_seventh_column_to_dict(
        "./src/case_study1/langgraph/evaluations/run_01_30_titles/04_article_writer_publishable.csv"
    )
    for result in results:
     
        if result["can_be_posted"] == "yes":
            if (
                result["meets_word_count"] == "yes"
                and result["is_not_sensationalistic"] == "yes"
                and result["is_language_french"] == "yes"
            ):
                print(f"{result} PASS")
            else:
                print("FAIL")
