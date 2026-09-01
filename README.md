# WhatsApp Blaster APK

This project contains a simple Kivy Android app that lets a user:

- select an Excel file with phone numbers
- optionally choose a media file
- type a WhatsApp message
- send bulk WhatsApp messages from an Android device

It also includes a GitHub Actions workflow and a Buildozer configuration for generating an APK.

## Project Files

- `main.py` – Kivy application logic
- `buildozer.spec` – Buildozer Android build configuration
- `setup_github_repo.py` – creates or updates a GitHub repository and uploads the project files
- `.github/workflows/build.yml` – GitHub Actions workflow to build the APK

## Requirements

For local Python validation in this workspace:

```bash
pip install -r requirements.txt
```

For Android APK building with Buildozer, you need a Linux environment and the standard Buildozer toolchain.

## Example Excel format

Your Excel file should contain a column named `Phone` with phone numbers such as:

| Phone |
|---|
| 15551234567 |
| 15557654321 |

The app cleans the digits from each value before sending.

## Run the app locally

This app is designed for Android via Kivy, but the Python code will also run in a simulated mode on non-Android systems.

```bash
python main.py
```

On Android, the app launches WhatsApp intents for each contact.

## Create the GitHub repository and push project files

Set your GitHub token and username, then run:

```bash
export GITHUB_TOKEN="your_token_here"
export GITHUB_USERNAME="your_github_username"
python setup_github_repo.py
```

The script creates the repository if it does not exist and uploads:

- `main.py`
- `buildozer.spec`
- `.github/workflows/build.yml`

## Build the APK with GitHub Actions

After pushing the repo to GitHub:

1. Open the repository on GitHub
2. Go to the Actions tab
3. Run the workflow manually or push to `main` / `master`
4. Download the generated APK artifact

## Notes

- This project is intended for educational and automation use.
- Be sure to follow WhatsApp and platform policies before sending bulk messages.
- Publishing or distributing spam-like messaging may be restricted or illegal in some regions.
