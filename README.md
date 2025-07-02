# Documentation for Indexing Search Project

This project provides functionality to manage document indexing using Python and Elasticsearch.

## Features

- Search for a tag and retrieve its index.
- Add new tags to an `undefine` index if not found.
- Easy integration with Elasticsearch.

## Requirements

- Python 3.x
- pip
- Elasticsearch Python client



## Installation

```bash
pip install -r requirements.txt
pip install elasticsearch

Start API server:
uvicorn main:app --reload
```

## Running the `main` API Locally

1. Make sure you have FastAPI and Uvicorn installed:
   ```bash
   pip install fastapi uvicorn
   
2. Start the API server from your project directory:
   ```bash
   uvicorn main:app --reload
   
3. Access the API at:
http://127.0.0.1:8000/search_tags/?search_string=your_query


4. You can also view the interactive SWAGGER docs at:
http://127.0.0.1:8000/docs