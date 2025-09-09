def parse_xray_output(raw_data: dict):
    findings = []
    for item in raw_data.get("findings", []):
        findings.append({
            "id": item.get("id", "F-XXXX"),
            "vuln_type": item.get("vuln_type", "unknown"),
            "location": item.get("location", "-"),
            "severity": item.get("severity", "low"),
            "confidence": item.get("confidence", "low")
        })
    return findings
