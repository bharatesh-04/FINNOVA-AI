# Contributing to Finnova AI

Thank you for your interest in contributing to Finnova AI! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Make your changes
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

See [GETTING_STARTED.md](GETTING_STARTED.md) for setup instructions.

## Code Guidelines

### Backend (Python/FastAPI)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions focused and small
- Add tests for new features

```python
def calculate_savings_rate(income: float, expenses: float) -> float:
    """Calculate savings rate as percentage.
    
    Args:
        income: Total monthly income
        expenses: Total monthly expenses
    
    Returns:
        Savings rate as percentage (0-100)
    """
    if income == 0:
        return 0
    return ((income - expenses) / income) * 100
```

### Frontend (TypeScript/React)
- Use TypeScript for all components
- Follow React hooks best practices
- Use meaningful component names
- Keep components focused
- Add proper error handling

```typescript
interface StatCardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
}

export function StatCard({ title, value, icon }: StatCardProps) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{value}</p>
      {icon}
    </div>
  );
}
```

## Commit Messages

Use clear and descriptive commit messages:
- `feat: Add expense categorization`
- `fix: Fix budget calculation bug`
- `docs: Update API documentation`
- `refactor: Improve transaction service`
- `test: Add tests for fraud detection`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Describe your changes in PR description
6. Link related issues

## Code Review

All submissions require code review. We look for:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

## Reporting Bugs

Create an issue with:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details

## Feature Requests

Suggest features by creating an issue with:
- Description of feature
- Use case/problem it solves
- Proposed implementation (optional)

## Questions?

- Open an issue for questions
- Check existing documentation
- Review existing issues

Thank you for contributing! 🎉
