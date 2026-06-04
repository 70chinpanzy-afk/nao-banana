# Nano Banana Pro

Nano Banana Pro is a Streamlit app for running Google Gemini image generation from a local, friendly web UI.

The project is designed for creators, educators, and small teams who want a simple open-source starting point for prompt-based image generation without building a full web application stack.

## Why This Project Exists

Image generation tools are useful, but many examples are either too minimal for real use or too tied to hosted services. Nano Banana Pro keeps the workflow local-first:

- bring your own Google AI Studio API key
- generate images from Japanese or English prompts
- choose a visual style before generation
- download generated images
- keep a session history while the app is running
- inspect and modify the full source code

The project is still early, but it is maintained as a public OSS application rather than a private demo. The near-term goal is to make it a dependable, easy-to-run reference app for local AI image generation.

## Features

- Text-to-image generation with Google Gemini
- Optional style presets such as anime, watercolor, 3D rendering, pixel art, and cyberpunk
- Password-style API key input
- Generated image preview
- Download button for generated images
- In-session image history gallery
- Japanese-first UI copy with English prompt support
- Error handling for authentication, quota, and safety-filter failures

## Screenshots

Screenshots and demo assets are planned for the next release. See [ROADMAP.md](ROADMAP.md).

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/70chinpanzy-afk/nao-banana.git
cd nao-banana
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Google API Key

1. Open [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create an API key.
3. Copy the key.

### 5. Run the App

```bash
streamlit run app.py
```

## Usage

1. Enter your Google API key in the sidebar or API settings area.
2. Write a detailed prompt.
3. Optionally choose a visual style.
4. Click the generation button.
5. Download the generated image if needed.

## Prompt Tips

- Include subject, style, color, lighting, mood, and composition.
- Be concrete: "a watercolor illustration of a small cafe at night" works better than "nice cafe".
- Japanese and English prompts can both work.
- If a prompt is blocked by a safety filter, rewrite it with safer, more specific language.

## Privacy and Security

Nano Banana Pro is intended to run locally.

- API keys are entered through Streamlit's password input.
- API keys are not written to files by this app.
- The app uses the key in the running Streamlit process to call Google Gemini.
- Do not deploy a public shared instance where users enter private API keys unless you have reviewed the hosting and secrets model.
- Never commit `.env`, `secrets.toml`, or other credential files.

For vulnerability reports, see [SECURITY.md](SECURITY.md).

## Project Status

This is an early-stage open-source project. Current maintenance priorities are:

- accurate setup documentation
- safer API key handling guidance
- reproducible local development
- issue templates for bug reports and feature requests
- release notes for visible project history
- tests and CI for future refactors

See [ROADMAP.md](ROADMAP.md) for planned work.

## Contributing

Contributions are welcome. Good first contributions include:

- improving setup instructions
- adding screenshots
- testing the app on different Python versions
- improving error messages
- adding model configuration options
- reporting bugs with clear reproduction steps

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## Maintainer

This repository is maintained by [@70chinpanzy-afk](https://github.com/70chinpanzy-afk).

Maintainer responsibilities include reviewing issues, triaging bugs, improving documentation, managing releases, and keeping dependency/security guidance current.

## Codex for Open Source

This repository is being prepared for open-source maintainer workflows. Planned Codex use cases include:

- reviewing pull requests for Streamlit and Python issues
- triaging bug reports and reproductions
- improving setup and troubleshooting documentation
- generating release checklist drafts
- scanning for risky credential-handling changes

See [docs/CODEX_FOR_OSS_APPLICATION.md](docs/CODEX_FOR_OSS_APPLICATION.md) for a short application draft.

## Tech Stack

- Python
- Streamlit
- Google GenAI SDK
- Pillow

## License

MIT License. See [LICENSE](LICENSE).
