# Pin Collector

A **Streamlit**-powered web application for managing and organizing pin collections. Import/export Excel files, edit entries in real-time with card or table views, and maintain your collection locally with ease.

## ✨ Features

- 🎴 **Card & Table Views**: switch between visual card layout and editable data tables
- 📊 **Excel Import/Export**: seamless .xlsx file handling with automatic column alignment
- 🔍 **Powerful Filters**: search by text, series, collection, or trade status
- 💾 **Local Persistence**: save your data to `data/pins.xlsx` for offline use
- 🖼️ **Image Support**: display pin images via URL (HTTP/HTTPS)
- ✏️ **Inline Editing**: modify entries directly in card view with save/cancel options
- 🎯 **Smart Validation**: automatic URL sanitization and data type enforcement

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Streamlit 1.37+ | Interactive web UI |
| **Data Processing** | pandas 2.2+ | DataFrame operations, Excel I/O |
| **Excel Engine** | openpyxl 3.1+ | .xlsx file read/write |
| **Language** | Python 3.9+ | Core application logic |

## 📁 Project Structure

```
pin-collector/
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env.example               # Environment configuration template
├── data/
│   ├── pins.xlsx              # Local pin database (auto-created)
│   └── sample_pins.xlsx       # Example dataset
├── launcher/                  # Cross-platform launch scripts
│   ├── index.html             # Visual launcher interface
│   ├── start_windows.bat      # Windows batch launcher
│   ├── setup_and_run.ps1      # PowerShell automated setup
│   └── start_unix.sh          # macOS/Linux launcher
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

```bash
# Clone or download the repository
cd pin-collector

# Create virtual environment (recommended)
python -m venv .venv

# Activate environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the application
streamlit run streamlit_app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

### Alternative: Visual Launcher

Open `launcher/index.html` in a browser for a guided setup with copy-paste commands and platform-specific scripts:
- **Windows**: `launcher/start_windows.bat` or `launcher/setup_and_run.ps1`
- **macOS/Linux**: `launcher/start_unix.sh`

## 📋 Data Schema

### Default Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `name` | Text | Pin identifier | "Pikachu #001" |
| `serie` | Text | Series name | "Kanto" |
| `collection` | Text | Collection group | "Starter Pack" |
| `quantity` | Integer | Number owned | 3 |
| `state` | Text | Condition | "Neuf", "Bon", "Usé" |
| `tradeable` | Boolean | Available for trade | true/false |
| `price` | Float | Value in € | 9.99 |
| `tags` | Text | Comma-separated keywords | "rare, limited" |
| `notes` | Text | Additional info | "Gift from 2024" |
| `image_url` | URL | Image link (HTTP/HTTPS) | "https://..." |

### Excel Import Behavior

- **Missing columns**: automatically added with default values
- **Extra columns**: preserved in the dataset
- **Type coercion**: quantity → int, price → float, tradeable → bool
- **URL validation**: non-HTTP/HTTPS URLs are cleared

Example Excel template: `data/sample_pins.xlsx`

## 🎯 Usage Guide

### Adding New Pins

1. Expand the **"Nouveau pin"** section
2. Fill in details (minimum: name)
3. Click **"Ajouter"** to append to collection

### Importing Data

- **Sidebar**: Use **"Importer un Excel"** file uploader
- **Or**: Click **"Charger data/pins.xlsx si dispo"** to load local file
- Columns are aligned automatically; no schema pre-processing needed

### Filtering

- **Text search**: matches any field content (case-insensitive)
- **Series/Collection**: partial string match
- **Trade status**: show only tradeable/non-tradeable pins

### Editing Entries

**Card View:**
1. Click **"Editer"** on any card
2. Modify fields in the inline form
3. **"Enregistrer"** to save or **"Annuler"** to discard

**Table View:**
- Toggle **"Mode tableau editable"** in sidebar
- Edit cells directly in the data editor
- Changes apply immediately

### Exporting & Saving

- **Export Excel**: Specify filename → **"Exporter Excel"** → download button
- **Save Locally**: **"Enregistrer dans data/pins.xlsx"** writes to disk

## ⚙️ Configuration

Copy `.env.example` to `.env` and customize:

```env
# Data directory path
DATA_DIR=data

# Default Excel filename
DEFAULT_EXCEL=pins.xlsx

# Maximum upload size (MB)
MAX_UPLOAD_SIZE_MB=200

# Debug mode
DEBUG=false
```

> **Note**: Streamlit configuration (port, theme, etc.) is managed via `.streamlit/config.toml`. See [Streamlit docs](https://docs.streamlit.io/library/advanced-features/configuration) for details.

## 🔒 Security Best Practices

- **URL Validation**: Only `http://` and `https://` image URLs are accepted
- **File Upload Limits**: Default 200MB; adjust `MAX_UPLOAD_SIZE_MB` as needed
- **Local-Only Mode**: No external database; all data stays on your machine
- **Input Sanitization**: Text fields are stripped and trimmed automatically
- **Type Safety**: Quantity/price coerced to numeric types with error handling

### Data Privacy

- Pin Collector runs **entirely locally** with no external API calls
- Excel files never leave your device unless explicitly exported
- Image URLs are loaded client-side by your browser (consider privacy implications if using sensitive images)

## 🧪 Testing

Create a test dataset:

```python
import pandas as pd

test_data = pd.DataFrame([
    {"name": "Test Pin 1", "serie": "Alpha", "quantity": 5},
    {"name": "Test Pin 2", "serie": "Beta", "quantity": 2, "tradeable": True}
])
test_data.to_excel("test_import.xlsx", index=False)
```

Launch the app and upload `test_import.xlsx` to verify import behavior.

## 🗺️ Roadmap

- [ ] **Image Thumbnails**: Generate local previews for offline use
- [ ] **CSV Export**: Add alternative export format
- [ ] **Multi-Collection Management**: Separate collections with tabs
- [ ] **Advanced Search**: Regex patterns, date ranges, price filters
- [ ] **Theming**: Custom color schemes and dark mode
- [ ] **Backup/Restore**: Automated snapshots with version history
- [ ] **Statistics Dashboard**: Collection value, completion metrics
- [ ] **Mobile Optimization**: Responsive card layouts for smaller screens

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

**Developed with ❤️ for pin collectors everywhere**

For issues or feature requests, open an issue on [GitHub](https://github.com/Adam-Blf/pin-collector).
