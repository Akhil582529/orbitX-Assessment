from extractor import extract_all
from llm import process_document
from writer import write_results

def run_pipeline(docs_folder="./docs"):
    print("Starting pipeline...")

    extracted = extract_all(docs_folder)
    
    results = [process_document(file) for file in extracted]
    write_results(results, output_folder="./outputs")

    print("Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()