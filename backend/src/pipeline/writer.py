import json
import os
from datetime import datetime

def write_results(results, output_folder="./outputs"):
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"results_{timestamp}.json")

    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]
    skipped = [r for r in results if r["status"] == "skipped"]

    output = {
        "processed_at": timestamp,
        "summary": {
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "skipped": len(skipped)
        },
        "documents": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Results written to {output_path}")
    print(f"Processed {len(results)} files — {len(successful)} success, {len(failed)} failed, {len(skipped)} skipped")

    return output_path