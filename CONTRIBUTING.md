# Contributing to Remote Crafter

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/remote-crafter.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `make dev`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `make test`
4. Run linting: `make lint`
5. Format code: `make format`
6. Commit with clear messages
7. Push to your fork
8. Create a Pull Request

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
[Type] Short description (50 chars max)

Longer explanation if needed (72 chars max per line)
- Bullet points for multiple changes
- Keep it concise and informative

Co-Authored-By: Your Name <your.email@example.com>
```

Types: feat, fix, docs, style, refactor, test, chore

## Code Standards

- Follow PEP 8 style guide
- Write type hints for functions
- Include docstrings for modules and functions
- Keep functions focused and testable
- Write tests for new features

## Testing

- Write tests for all new features
- Ensure all tests pass: `make test`
- Aim for >80% code coverage
- Test edge cases and error scenarios

## Submitting a Pull Request

1. Ensure tests pass and code is formatted
2. Write a clear PR description
3. Reference any related issues
4. Wait for review and address feedback
5. Ensure CI/CD checks pass

## Questions?

Open an issue or start a discussion. We're here to help!

Thank you for contributing!
