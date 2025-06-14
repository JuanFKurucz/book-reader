name: ✨ Feature Request
description: Suggest an idea for this project
title: "[Feature]: "
labels: ["enhancement", "feature"]
assignees:
  - juanfkurucz
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to suggest a new feature!

  - type: textarea
    id: problem-description
    attributes:
      label: Is your feature request related to a problem? Please describe.
      description: A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]
      placeholder: Describe the problem or limitation you're facing.
    validations:
      required: true

  - type: textarea
    id: solution-description
    attributes:
      label: Describe the solution you'd like
      description: A clear and concise description of what you want to happen.
      placeholder: How would this feature work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Describe alternatives you've considered
      description: A clear and concise description of any alternative solutions or features you've considered.

  - type: textarea
    id: additional-context
    attributes:
      label: Additional context
      description: Add any other context or screenshots about the feature request here.
