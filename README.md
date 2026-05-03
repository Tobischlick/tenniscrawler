![PyLint](https://github.com/Tobischlick/tenniscrawler/actions/workflows/linter.yml/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Tobischlick/tenniscrawler)
![GitHub](https://img.shields.io/github/license/Tobischlick/tenniscrawler)
![GitHub top language](https://img.shields.io/github/languages/top/Tobischlick/tenniscrawler)

# 🎾 TennisCrawler

**TennisCrawler** is a Python-based automation tool designed to scrape contact information from the Badischer
Tennisverband (nuliga) website. It navigates through regional "Bezirk" pages to extract specific email addresses and
exports them into a structured CSV format for easy management and data processing.

The tool is specifically built to help tennis club administrators and regional coordinators streamline the process of
gathering contact data from official association pages.

## 🚀 Installation & Setup

Follow these steps to set up the environment and prepare the project for its first run.

### 1. Clone the Repository

Start by cloning the repository from GitHub to your local machine:

#### HTTPS

```bash
git clone https://github.com/Tobischlick/tenniscrawler.git
cd tenniscrawler
```

#### SSH

```bash
git clone git@github.com:Tobischlick/tenniscrawler.git
cd tenniscrawler
```

### 2. Set up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install requests
pip install bs4
```

### 4. Prepare Directories

```bash
mkdir Logfiles
mkdir Excelfiles
```

## ⚙️ Configuration

The crawler's behavior is defined in the `.config/config.ini` file. This allows you to customize which regions are
targeted and what types of contacts are extracted.

### 📍 URLS

In this section, list the URLs for the specific districts (Bezirk) of the Badischer Tennisverband you wish to crawl.

* **Flexible Keys:** The names of the keys (e.g., `link1`, `link2`) do not matter; the script simply iterates through
  all values provided.
* **Default:** By default, the project is set up to include all districts in Baden.

### 📧 MAILS

This section defines the filters for the types of email addresses you want to extract.

* **Targeting:** You can specify keywords related to the positions or mail types you are interested in.
* **Flexible Keys:** Similar to the URLs section, only the values are used by the crawler.

## 🛠 Usage

Once you have configured your `.config/config.ini` file, you can start the extraction process with a single command.

### Running the Crawler

Execute the main script from the root directory of the project:

```bash
python crawler.py
```