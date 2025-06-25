# CoffeeShop ☕️

A simple Flask backend for managing coffee-shop orders and inventory.

---

## 🚀 Quick Start

> Tested with **Python 3.13** on Windows 10 and Ubuntu 22.04.

```bash
# 1. Clone the repo
git clone https://github.com/<your-user>/coffeeshop.git
cd coffeeshop

# 2. Create & activate a virtual environment (recommended)
python -m venv .venv
# ├─ Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# └─ macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Set environment variables (development defaults)
#    Windows PowerShell
set FLASK_APP=app.py
set FLASK_ENV=development
#    macOS / Linux / Git Bash
export FLASK_APP=app.py
export FLASK_ENV=development

# 5. Initialise / upgrade the database (first run only)
flask db upgrade

# 6. Run the server
flask run            # -> http://127.0.0.1:5000/
