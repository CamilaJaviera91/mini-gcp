import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import csv
import datetime
import os
import re

INPUT_DIR = "data/extract"
OUTPUT_DIR = "data/processed"
FILE_PREFIX = "copy_raw_sales_"
OUTPUT_PREFIX = "clean_sales_"

def get_latest_input_file():
    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.startswith(FILE_PREFIX) and f.endswith(".csv")
    ]
    if not files:
        raise FileNotFoundError("❌ No input CSV files found in 'data/extract/'")

    files_with_numbers = []
    for f in files:
        match = re.search(rf"{FILE_PREFIX}(\d+)\.csv", f)
        if match:
            files_with_numbers.append((int(match.group(1)), f))

    if not files_with_numbers:
        raise ValueError("❌ No input files match expected naming pattern")

    files_with_numbers.sort(reverse=True)
    latest_number, latest_file = files_with_numbers[0]

    input_path = os.path.join(INPUT_DIR, latest_file)
    output_filename = f"{OUTPUT_PREFIX}{latest_number}.csv"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    return input_path, output_path

class ParseCSVLine(beam.DoFn):
    def process(self, line):
        try:
            values = next(csv.reader([line]))
            yield {
                "id": values[0],
                "customer": values[1],
                "product": values[2],
                "price": values[3],
                "sale_date": values[4]
            }
        except Exception:
            return

class CleanRecord(beam.DoFn):
    def process(self, record):
        try:
            required_fields = ["id", "customer", "product", "price", "sale_date"]

            is_header = all(
                str(record.get(field)).lower() == field for field in required_fields
            )
            if is_header:
                yield record
                return

            if any(not record.get(field) for field in required_fields):
                return

            if record["product"] == "UNKNOWN_PRODUCT":
                return

            float(record["price"])
            datetime.datetime.strptime(record["sale_date"], "%Y-%m-%d")

            yield record
        except Exception:
            return

class ToCSVLine(beam.DoFn):
    def process(self, record):
        yield f'{record["id"]},{record["customer"]},{record["product"]},{record["price"]},{record["sale_date"]}'

def run():
    try:
        input_file, output_file = get_latest_input_file()
    except Exception as e:
        print(str(e))
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    pipeline_options = PipelineOptions()
    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read CSV" >> beam.io.ReadFromText(input_file, skip_header_lines=0)
            | "Parse CSV" >> beam.ParDo(ParseCSVLine())
            | "Clean Data" >> beam.ParDo(CleanRecord())
            | "To CSV Line" >> beam.ParDo(ToCSVLine())
            | "Write Clean CSV" >> beam.io.WriteToText(output_file, file_name_suffix=".tmp", shard_name_template="")
        )

    os.rename(output_file + ".tmp", output_file)
    print(f"✅ Clean file saved as: {output_file}")

if __name__ == "__main__":
    run()
