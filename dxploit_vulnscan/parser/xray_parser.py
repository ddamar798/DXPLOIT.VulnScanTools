"""
Parser to normalize Xray result JSON into internal schema.
The parser is defensive — Xray versions differ. Adjust mapping if your xray JSON differs.
Internal schema:
{
  "target": "...",
  "scan_date": "...",
  "findings": [
    {
      "id": "F-0001",
      "vuln_type": "sql_injection",
      "location": "/vuln.php?id=1",
      "severity": "high",
      "confidence": "medium",
      "evidence": [...],
      "recommended_action": "...",
      "recommended_tools": [...],
      "references": [...]
    }, ...
  ],
  "summary": {...}
}
"""
from datetime import datetime
from typing import Dict, Any, List
from ..recommender import recommend_for

def now_ts():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def parse_xray_raw(raw: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    items = []

    if isinstance(raw, dict):
        for k in ("results", "data", "vulnerabilities", "issues"):
            if k in raw and isinstance(raw[k], list):
                items = raw[k]
                break
        if not items:
            # try values that are lists
            for v in raw.values():
                if isinstance(v, list):
                    items = v
                    break
    elif isinstance(raw, list):
        items = raw

    if not items:
        items = [raw]

    for idx, it in enumerate(items, start=1):
        vuln_type = it.get("type") or it.get("vuln") or it.get("vulnerability") or "unknown"
        location = it.get("url") or it.get("path") or it.get("location") or it.get("uri") or "-"
        severity = (it.get("severity") or it.get("level") or it.get("risk") or "medium").lower()
        confidence = it.get("confidence") or it.get("score") or "medium"
        evidence = []
        for k in ("detail", "desc", "evidence", "payload"):
            if k in it:
                v = it[k]
                if isinstance(v, str):
                    evidence.append(v)
                elif isinstance(v, list):
                    evidence.extend([str(x) for x in v])
        rec = recommend_for(vuln_type)
        finding = {
            "id": f"F-{now_ts()}-{idx}",
            "vuln_type": vuln_type,
            "location": location,
            "severity": severity,
            "confidence": confidence,
            "evidence": evidence,
            "recommended_action": rec.get("rec_mitigate"),
            "recommended_tools": [rec.get("rec_verify")],
            "references": it.get("references", [])
        }
        findings.append(finding)

    summary = {"total_findings": len(findings), "high": 0, "medium": 0, "low": 0}
    for f in findings:
        s = f.get("severity", "medium")
        if s in ("critical", "high"):
            summary["high"] += 1
        elif s == "medium":
            summary["medium"] += 1
        else:
            summary["low"] += 1

    return {"target": raw.get("target") if isinstance(raw, dict) and raw.get("target") else "(unknown)", "scan_date": datetime.now().isoformat(), "findings": findings, "summary": summary}
