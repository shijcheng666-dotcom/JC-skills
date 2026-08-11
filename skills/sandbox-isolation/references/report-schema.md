# Diagnostic report schema

Emit one record per discovered file and one summary record. JSON output should remain stable so callers can automate review.

## File record

```json
{
  "path": "relative/path.md",
  "category": "governance|system_memory|daily_log|state|extra",
  "status": "missing|clean|contaminated|malformed|expired|conflict|unknown",
  "evidence": ["short factual indicator"],
  "proposed_action": "none|reset|review|archive|confirm_separately",
  "requires_confirmation": true
}
```

## Summary record

```json
{
  "mode": "diagnose|cleanup|archive_review",
  "governance": "present|missing|ambiguous",
  "read_only": true,
  "writes_performed": false,
  "limitations": ["..."],
  "files": []
}
```

Do not put secrets, full private file contents, or absolute user paths in reports. Evidence should be short and line-oriented.
