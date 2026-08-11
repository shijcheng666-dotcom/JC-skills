# Daily-log policy

Apply the workspace governance file first. The values below are conservative defaults when governance does not define them.

```yaml
summary_max_chars: 20
topic_tag_required: true
allow_output_path_line: false
ignore_before_effective_date: true
auto_distill: false
auto_delete_expired: false
auto_archive_expired: false
require_confirmation_for_archive: true
```

## Valid compact entry

```text
[topic] One short summary
```

An output-path line is allowed only when the governance file explicitly allows it. Do not treat a long multi-line explanation, heading tree, audit notes, or implementation diary as a compact daily log.

## Date handling

If the governance effective date is known, classify earlier logs as historical. Report them without applying current violations unless the user explicitly requests a historical audit. Do not delete or archive any log automatically.
