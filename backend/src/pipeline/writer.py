import json
import os
from datetime import datetime


def write_results(results, output_folder="./outputs"):
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"results_{timestamp}.json")

    output = {
        "processed_at": timestamp,
        "summary": {
            "total": len(results),
        },
        "documents": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n Results written to {output_path}")

    return output_path