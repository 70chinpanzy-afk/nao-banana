# Contributing

Thanks for considering a contribution to Nano Banana Pro.

This project is early, so the most valuable contributions are clear bug reports, setup feedback, small documentation improvements, and focused pull requests.

## Ways to Help

- Report setup problems with your OS, Python version, and full error message.
- Improve README steps when something is unclear.
- Add screenshots or demo material.
- Improve Streamlit UI copy.
- Add tests around prompt construction and error handling.
- Review security-sensitive changes, especially credential handling.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Pull Request Guidelines

- Keep pull requests focused on one change.
- Explain the user-facing impact.
- Include screenshots for UI changes when possible.
- Do not commit API keys, generated private images, `.env`, or `secrets.toml`.
- Update README or CHANGELOG when behavior changes.

## Issue Triage

Maintainers use these labels conceptually:

- `bug`: broken behavior or error handling
- `docs`: documentation improvements
- `security`: credential handling or dependency safety
- `enhancement`: new user-facing capability
- `good first issue`: small, well-scoped contribution

## Code of Conduct

Be kind, specific, and practical. Assume good intent, but keep discussions focused on making the project safer and easier to use.
