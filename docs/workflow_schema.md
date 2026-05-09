# Workflow Schema

Each workflow is a JSON array.

Each step contains:

- step → step number
- component → tool/component name
- params → parameters object

Example:

[
  {
    "step": 1,
    "component": "email_reader",
    "params": {
      "folder": "inbox"
    }
  }
]