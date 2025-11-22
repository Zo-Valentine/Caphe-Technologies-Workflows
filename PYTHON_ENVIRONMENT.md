# Python Virtual Environment Setup

## Environment: caphe.env

### ✅ Installation Complete!

A Python virtual environment named `caphe.env` has been successfully created and all dependencies from `requirements.txt` have been installed.

### 📦 Installed Packages (29 packages)

#### Core Dependencies
- **websockets** (15.0.1) - WebSocket client/server library
- **sentry-sdk** (2.45.0) - Error tracking and monitoring

#### Development Tools
- **ruff** (0.14.5) - Fast Python linter and formatter
- **ty** (0.0.1a27) - Type checking tool
- **pytest** (8.4.2) - Testing framework
- **pytest-cov** (7.0.0) - Code coverage for pytest
- **pytest-asyncio** (1.2.0) - Async support for pytest
- **aiohttp** (3.13.2) - Async HTTP client/server

#### Supporting Libraries
- aiohappyeyeballs (2.6.1)
- aiosignal (1.4.0)
- async-timeout (5.0.1)
- attrs (25.4.0)
- backports.asyncio.runner (1.2.0)
- certifi (2025.11.12)
- coverage (7.10.7)
- exceptiongroup (1.3.0)
- frozenlist (1.8.0)
- idna (3.11)
- iniconfig (2.1.0)
- multidict (6.7.0)
- packaging (25.0)
- pluggy (1.6.0)
- propcache (0.4.1)
- Pygments (2.19.2)
- tomli (2.3.0)
- typing_extensions (4.15.0)
- urllib3 (2.5.0)
- yarl (1.22.0)

### 🔧 How to Use

#### Activate the environment:
```bash
source caphe.env/bin/activate
```

Or use the helper script:
```bash
source activate_env.sh
```

#### Deactivate the environment:
```bash
deactivate
```

#### Run Python code with the environment:
```bash
source caphe.env/bin/activate
python your_script.py
```

#### Run tests:
```bash
source caphe.env/bin/activate
pytest
```

#### Check installed packages:
```bash
source caphe.env/bin/activate
pip list
```

### 📝 Notes

- **Python Version**: 3.9.6 (System Python)
- **Required Version**: The n8n task-runner-python requires Python >= 3.13
  - ⚠️ You may need to upgrade Python to use the full task runner functionality
- **Location**: `/Users/Apple/Caphe Workflows/caphe.env/`
- **Package Manager**: pip (25.3)

### 🔄 Updating Dependencies

To update all packages to their latest versions:
```bash
source caphe.env/bin/activate
pip install --upgrade -r requirements.txt
```

### 🗑️ Removing the Environment

If you need to remove the virtual environment:
```bash
rm -rf caphe.env
```

Then recreate it with:
```bash
python3 -m venv caphe.env
source caphe.env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

**Created**: November 19, 2025
**Environment Name**: caphe.env
**Status**: ✅ Active and Ready to Use
