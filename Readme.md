# Jibble Automator

This project automates clocking in and out on Jibble using Selenium WebDriver. It runs automatically on a scheduled basis via GitHub Actions.

## Features

- Automated sign-in (clock-in) functionality: Monday to Saturday at 9 AM IST
- Automated sign-out (clock-out) functionality: Tuesday to Sunday at 3 AM IST
- GitHub Actions workflow with scheduled execution
- Headless browser support for CI/CD environments
- Secure credential management through GitHub Secrets

## Schedule

- **Sign-in**: Monday to Saturday at 9:00 AM Indian Standard Time (IST)
- **Sign-out**: Tuesday to Sunday at 3:00 AM Indian Standard Time (IST)

## Setup

### GitHub Actions Setup (Required)

1. Go to your repository Settings > Secrets and variables > Actions
2. Add the following repository secrets:
   - `JIBBLE_EMAIL`: Your Jibble login email
   - `JIBBLE_PASSWORD`: Your Jibble login password

3. The workflow will run automatically according to the schedule above
4. You can also trigger it manually from the Actions tab

### Workflow Configuration

The GitHub Actions workflow (`jibble-automation.yml`) includes:
- Scheduled triggers for sign-in and sign-out
- Modern Chrome and ChromeDriver installation with version compatibility
- Virtual display setup (Xvfb) for headless browser operation
- Environment variables for secure credential management
- Error handling and debugging features
- JavaScript-based clicking to handle dialog overlays

## Security Notes

- **No hardcoded credentials**: All credentials must be provided via GitHub Secrets
- Scripts will fail with clear error message if credentials are not provided

## Troubleshooting

If the workflow fails:
1. Check the Actions logs for detailed error messages
2. Verify that your GitHub Secrets are set correctly
3. Ensure your Jibble credentials are valid
4. Check if Jibble's UI has changed (element selectors may need updating)