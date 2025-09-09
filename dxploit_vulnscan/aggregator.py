from typing import Dict, Any
def aggregate(parsed: Dict[str, Any]) -> Dict[str, Any]:
    findings = parsed.get("findings", [])
    seen = set()
    dedup = []
    for f in findings:
        key = (f.get("vuln_type"), f.get("location"))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(f)
    parsed["findings"] = dedup
    parsed["summary"]["total_findings"] = len(dedup)
    return parsed
