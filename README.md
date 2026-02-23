# Math Step Checker

A full-stack application that validates multi-step math solutions symbolically. Users enter each step of their algebra or calculus work and get immediate feedback on where their reasoning goes wrong.

## Tech Stack

**Backend** — Python, FastAPI, SymPy  
**Frontend** — Next.js 16, TypeScript, Tailwind CSS

## How It Works

Rather than pattern-matching or rule-detection, the validator uses symbolic math:
- **Algebra steps** are checked by comparing solution sets via SymPy's `solve`
- **Derivative steps** are verified by differentiating the previous expression and comparing symbolically
- **Integral steps** are verified by differentiating the user's answer and checking it matches the integrand

This means the validator handles arbitrary valid algebraic manipulations without needing to know which rule was applied.

## Project Structure

```
math-checker/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── check.py        # POST /check endpoint
│   │   └── core/
│   │       ├── models.py       # Step, Operation, StepSchema
│   │       ├── parser.py       # parse_equation, parse_expression
│   │       ├── algebra.py      # Algebraic equivalence
│   │       ├── calculus.py     # Derivative and integral validation
│   │       └── validator.py    # Dispatcher, find_first_error
│   └── tests/
│       ├── conftest.py
│       ├── test_parser.py
│       ├── test_algebra.py
│       ├── test_calculus.py
│       ├── test_validator.py
│       └── test_api.py
└── frontend/
    ├── app/
    │   ├── components/
    │   │   └── StepInput.tsx
    │   ├── lib/
    │   │   └── api.ts
    │   ├── types/
    │   │   └── api.ts
    |   ├── layout.tsx
    │   └── page.tsx
    └── package.json
```

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`, backend on `http://127.0.0.1:8000`.

### Tests

```bash
cd backend
pytest tests/ -v
```

## Supported Operations

| Operation | Example | How it's validated |
|---|---|---|
| Simplify | `2x + 4x` → `6x` | Symbolic equivalence |
| Differentiate | `x² + 3x` → `2x + 3` | `diff(prev) == curr` |
| Integrate | `6x` → `3x² + C` | `diff(curr) == prev` |
