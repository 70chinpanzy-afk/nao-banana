# Security Policy

Nano Banana Pro handles user-provided API keys, so security reports are welcome.

## Supported Versions

The `main` branch is the only currently supported version.

## Reporting a Vulnerability

Please open a GitHub issue if the report does not expose secrets or exploit details.

If a report includes sensitive details, contact the maintainer privately first, then open a public issue after the risk is understood.

## Security Notes

- The app is intended for local use.
- The API key is used by the running Streamlit process to call Google Gemini.
- The app should not write API keys to disk.
- `.streamlit/secrets.toml`, `.env`, and similar files must not be committed.
- Public deployments require additional review before accepting user-provided API keys.

## Review Priorities

Security-sensitive pull requests include changes to:

- API key input and storage
- network requests
- generated file downloads
- dependency versions
- deployment documentation
