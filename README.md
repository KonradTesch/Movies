# Movies

## Project Description

**Movies** is a Python-based movie database application designed to showcase programming skills in Python, SQL, API integration, and HTML generation.  
It allows users to manage their own movie collection via a command-line interface, fetch data directly from the OMDb API, generate statistics and visualizations, and even build a simple HTML website with movie details.

This project demonstrates the integration of multiple technologies — Python scripting, SQL storage, API usage, HTML rendering, and data visualization with matplotlib.

## Features

- **Interactive CLI menu** to manage your movie collection
- **Add, update, delete, and search movies**
- **Fetch movie details from the OMDb API**
- **Generate a HTML website with your movie list**
- **Statistics & visualizations**:
  - Show collection statistics
  - Create histograms of ratings
- **Sort movies** by rating or release year
- **Filter movies** by user-defined criteria

---

## Usage

### Requisites

Make sure that Python 3 is installed. Then install the requirements:

```bash
pip install -r requirements.txt
```

### Configuration

Create an `.env` file in the root directory (if not present) with the following content:

```env
API_KEY=*your_api_key*
```

### Running the Application

Start the program by running:

Windows:
```bash
python main.py
```
Mac:
```bash
python3 main.py
```

The interactive menu will appear, offering options to list, add, update, delete, or search movies, as well as fetch new movie data, generate websites, and create histograms.

---
### Example Workflow

1. Run the program and choose **Add Movie**.  
2. Enter a title (e.g., *Inception*) — data will be fetched from the OMDb API.  
3. Explore your movie collection via the menu options.  
4. Generate a simple **HTML website** to view your collection in a browser.  
5. Create a **histogram** of ratings to visualize your data. 

---

## Author

Created by Konrad Tesch