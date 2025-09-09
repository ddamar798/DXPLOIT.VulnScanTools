from collections import Counter

def aggregate_findings(findings: list):
    severity_count = Counter([f["severity"] for f in findings])
    return {
        "summary": dict(severity_count),
        "findings": findings
    }
