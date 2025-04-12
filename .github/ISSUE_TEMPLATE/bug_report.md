name: 🐛 Bug Report
description: Create a report to help us improve
title: "[Bug]: "
labels: ["bug", "triage"]
assignees:
  - juanfkurucz
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: what-happened
    attributes:
      label: Describe the bug
      description: A clear and concise description of what the bug is. Please include any error messages, logs, or screenshots.
      placeholder: Tell us what you see!
    validations:
      required: true

  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior.
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected behavior
      description: A clear and concise description of what you expected to happen.
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      description: What operating system are you using?
      options:
        - Windows
        - macOS
        - Linux
        - Other
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Version
      description: What version of book-reader are you running? (e.g., `book-reader --version` or Docker tag)
      placeholder: e.g., 0.1.0 or :latest
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Please copy and paste any relevant log output. This will be automatically formatted into code, so no need for backticks.
      render: shell

  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our [Code of Conduct](link/to/code/of/conduct) (we'll add this later!)
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
