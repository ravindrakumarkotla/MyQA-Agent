# AI QA Agent - Developer Guide

## 👨‍💻 For Developers & Contributors

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Code Style & Standards](#code-style--standards)
4. [Module Documentation](#module-documentation)
5. [Adding New Features](#adding-new-features)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Performance Optimization](#performance-optimization)
9. [Deployment](#deployment)

---

## Development Setup

### Prerequisites
- Python 3.9+
- Virtual environment (venv, conda, or similar)
- Git (optional)
- VS Code or similar IDE

### Installation Steps

```bash
# Clone or download repository
cd MyQA_Agent/Myqa_agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload

# Server running on http://localhost:8000
```

### IDE Setup (VS Code)

**Install Extensions**:
- Python (Microsoft)
- Pylance
- REST Client
- Thunder Client or Postman extension

**Create `.vscode/settings.json`**:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

---

## Project Structure

### Codebase Organization

```
app/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI app entry point
│
├── api/                        # REST API endpoints
│   ├── __init__.py
│   ├── upload.py              # POST /api/upload/document
│   ├── analyze.py             # POST /api/analyze/document
│   ├── generate.py            # POST /api/generate/test-cases
│   └── export.py              # POST /api/export/test-cases
│
├── models/                     # Pydantic data models
│   ├── __init__.py
│   └── testcase.py            # TestStep, TestCase, etc.
│
├── services/                   # Business logic
│   ├── __init__.py
│   ├── document_parser.py     # PDF/DOCX/TXT parsing
│   └── ai_agent.py            # Test case generation
│
└── utils/                      # Utility functions
    ├── __init__.py
    ├── word_exporter.py       # Word export (.docx)
    └── excel_exporter.py      # Excel export (.xlsx)

public/                        # Frontend files
├── index.html                 # Main UI page
├── style.css                  # Styling
└── script.js                  # JavaScript interactivity
```

### Key Directory Functions

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `app/` | Backend application logic | `main.py` |
| `app/api/` | REST API endpoints | `*.py` route handlers |
| `app/models/` | Data validation & schemas | `testcase.py` |
| `app/services/` | Core business logic | `document_parser.py`, `ai_agent.py` |
| `app/utils/` | Export functionality | `word_exporter.py`, `excel_exporter.py` |
| `public/` | Frontend UI assets | `index.html`, `style.css`, `script.js` |
| `uploads/` | Temporary uploaded files | Generated at runtime |
| `exports/` | Generated export files | Generated at runtime |

---

## Code Style & Standards

### Python Style Guide (PEP 8)

**Naming Conventions**:
```python
# Variables and functions: snake_case
file_id = "123"
def parse_document():
    pass

# Classes: PascalCase
class DocumentParser:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 50_000_000
SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"]
```

**Docstring Format**:
```python
def parse_document(file_path: str) -> dict:
    """
    Parse a document and extract content.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Dictionary containing parsed content with keys:
        - 'content': str, extracted text
        - 'metadata': dict, document metadata
        - 'success': bool, parse status
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file format is unsupported
        
    Example:
        >>> result = parse_document('requirements.pdf')
        >>> print(result['content'])
    """
    pass
```

**Import Organization**:
```python
# Standard library imports
import os
import json
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field

# Local imports
from app.models.testcase import TestCase
from app.services.document_parser import DocumentParser
```

**Type Hints**:
```python
# Always use type hints for function arguments and return values
def analyze_content(
    content: str,
    format: str = "pdf"
) -> Dict[str, List[str]]:
    """Analyze document content."""
    pass

# Use Optional for nullable types
def get_test_case(test_id: Optional[str] = None) -> Optional[TestCase]:
    """Retrieve test case or None if not found."""
    pass

# Use Union for multiple types
from typing import Union
def process_data(data: Union[str, bytes]) -> str:
    """Process string or bytes data."""
    pass
```

**Error Handling**:
```python
# Be specific with exceptions
try:
    with open(file_path) as f:
        content = f.read()
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise
except IOError as e:
    logger.error(f"IO error reading file: {e}")
    raise
```

### JavaScript Style Guide

**Naming Conventions**:
```javascript
// Variables and functions: camelCase
const fileId = "123";
function parseDocument() {
  // code
}

// Classes and constructors: PascalCase
class DocumentParser {
  // code
}

// Constants: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 50_000_000;
const SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"];
```

**Comments & Documentation**:
```javascript
/**
 * Parse a document and extract content.
 *
 * @param {string} filePath - Path to the document file
 * @returns {Promise<Object>} Object with content and metadata
 * @throws {Error} If file parsing fails
 *
 * @example
 * const result = await parseDocument('requirements.pdf');
 * console.log(result.content);
 */
async function parseDocument(filePath) {
  // implementation
}
```

**Error Handling**:
```javascript
// Use try-catch for async operations
async function fetchData() {
  try {
    const response = await fetch('/api/endpoint');
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch data:', error);
    throw error;
  }
}

// Use console for debugging in development
console.log('Debug info:', variable); // logs
console.error('Error occurred:', error); // errors
console.warn('Warning:', message); // warnings
```

---

## Module Documentation

### app/main.py

**Purpose**: FastAPI application entry point and configuration

**Key Components**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Create app instance
app = FastAPI(
    title="MyQA Agent API",
    description="AI-powered Test Case Generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
public_dir = Path(__file__).parent.parent / "public"
if public_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(public_dir)), name="static")

# Include routers
from app.api import upload, analyze, generate, export
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(generate.router)
app.include_router(export.router)

# Root endpoint
@app.get("/")
async def serve_ui():
    """Serve main UI page."""
    pass

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    pass
```

**Common Modifications**:
- Add new routers: `app.include_router(new_router.router)`
- Modify CORS: Update `allow_origins` list
- Add middleware: Use `app.add_middleware()`

### app/services/document_parser.py

**Purpose**: Parse uploaded documents (PDF, DOCX, TXT)

**Key Methods**:
```python
class DocumentParser:
    def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF."""
        
    def parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX."""
        
    def parse_txt(self, file_path: str) -> str:
        """Extract text from TXT."""
        
    def analyze_content(self, content: str) -> dict:
        """Analyze content and extract requirements."""
```

**Example Usage**:
```python
parser = DocumentParser()
text = parser.parse_pdf("requirements.pdf")
analysis = parser.analyze_content(text)
```

**Extending**: Add new file format support
```python
def parse_xlsx(self, file_path: str) -> str:
    """Extract text from XLSX (if needed)."""
    # Implementation
    pass
```

### app/services/ai_agent.py

**Purpose**: Generate test cases using AI

**Key Methods**:
```python
class AIAgent:
    def generate_positive_test_case(self, requirements: str) -> TestCase:
        """Generate positive test case."""
        
    def generate_negative_test_case(self, requirements: str) -> TestCase:
        """Generate negative test case."""
        
    def generate_boundary_test_case(self, requirements: str) -> TestCase:
        """Generate boundary test case."""
```

**Example Usage**:
```python
agent = AIAgent()
test_case = agent.generate_positive_test_case(user_story)
```

**Extending**: Integrate real LLM
```python
def generate_with_llm(self, prompt: str) -> str:
    """Generate response using LLM API."""
    # Call OpenAI, Claude, etc.
    pass
```

### app/models/testcase.py

**Purpose**: Define data schemas using Pydantic

**Key Models**:
```python
from pydantic import BaseModel, Field

class TestStep(BaseModel):
    step_number: int = Field(..., description="Step sequence number")
    action: str = Field(..., description="Action to perform")
    expected_result: str = Field(..., description="Expected outcome")

class TestCase(BaseModel):
    test_case_id: str
    name: str
    description: str
    test_type: str  # positive, negative, boundary
    priority: str   # high, medium, low
    test_steps: List[TestStep]
    expected_result: str
    pre_conditions: str
    post_conditions: str
```

### app/utils/word_exporter.py

**Purpose**: Export test cases to Word format (.docx)

**Key Methods**:
```python
class WordExporter:
    def export_to_word(
        self,
        test_cases: List[TestCase],
        output_path: str
    ) -> bool:
        """Export test cases to Word document."""
        # Create document
        # Add tables, formatting
        # Save file
        pass
```

### app/utils/excel_exporter.py

**Purpose**: Export test cases to Excel format (.xlsx)

**Key Methods**:
```python
class ExcelExporter:
    def export_to_excel(
        self,
        test_cases: List[TestCase],
        output_path: str
    ) -> bool:
        """Export test cases to Excel workbook."""
        # Create workbook
        # Add sheets, data, formatting
        # Save file
        pass
```

---

## Adding New Features

### Feature: Add New File Format Support

**Steps**:

1. **Create parser method** in `app/services/document_parser.py`:
```python
def parse_xml(self, file_path: str) -> str:
    """Extract data from XML file."""
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Extract text content
    text = ET.tostring(root, encoding='unicode')
    return text
```

2. **Update upload validation** in `app/api/upload.py`:
```python
SUPPORTED_FORMATS = [".pdf", ".docx", ".txt", ".xml"]  # Add .xml

if not file.filename.lower().endswith(tuple(SUPPORTED_FORMATS)):
    raise HTTPException(status_code=400, detail="Unsupported format")
```

3. **Add parser routing** in `app/api/analyze.py`:
```python
def get_file_content(file_path: str) -> str:
    """Route to appropriate parser based on file extension."""
    if file_path.endswith('.pdf'):
        return parser.parse_pdf(file_path)
    elif file_path.endswith('.docx'):
        return parser.parse_docx(file_path)
    elif file_path.endswith('.txt'):
        return parser.parse_txt(file_path)
    elif file_path.endswith('.xml'):
        return parser.parse_xml(file_path)
```

4. **Test the feature**:
```python
# In test_new_feature.py
def test_xml_parsing():
    parser = DocumentParser()
    content = parser.parse_xml("test.xml")
    assert len(content) > 0
```

### Feature: Add Authentication

1. **Create auth module**:
```python
# app/auth/tokens.py
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

2. **Add auth dependency**:
```python
# app/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    return username
```

3. **Protect endpoints**:
```python
from app.auth.dependencies import verify_token

@router.post("/api/upload/document")
async def upload_document(
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):
    """Protected endpoint - requires authentication."""
    pass
```

### Feature: Add Caching

```python
from functools import lru_cache
import time

class CacheManager:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str):
        """Get cached value if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value):
        """Store value in cache."""
        self.cache[key] = (value, time.time())

# Usage
cache = CacheManager()
analysis = cache.get(file_id)
if analysis is None:
    analysis = parse_and_analyze(file_id)
    cache.set(file_id, analysis)
```

---

## Testing

### Unit Tests

**Create** `tests/test_document_parser.py`:
```python
import pytest
from app.services.document_parser import DocumentParser

class TestDocumentParser:
    @pytest.fixture
    def parser(self):
        return DocumentParser()
    
    def test_parse_txt_file(self, parser):
        """Test parsing text file."""
        content = parser.parse_txt("tests/samples/test.txt")
        assert len(content) > 0
        assert isinstance(content, str)
    
    def test_parse_invalid_file(self, parser):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            parser.parse_txt("nonexistent.txt")
    
    def test_analyze_content(self, parser):
        """Test content analysis."""
        content = "As a user, I want to login"
        analysis = parser.analyze_content(content)
        assert "user_stories" in analysis
        assert len(analysis["user_stories"]) > 0
```

**Run Tests**:
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_document_parser.py::TestDocumentParser::test_parse_txt_file
```

### Integration Tests

**Create** `tests/test_api_workflow.py`:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_complete_workflow():
    """Test complete workflow from upload to export."""
    
    # Upload
    with open("tests/samples/requirements.pdf", "rb") as f:
        response = client.post(
            "/api/upload/document",
            files={"file": f}
        )
    assert response.status_code == 200
    file_id = response.json()["file_id"]
    
    # Analyze
    response = client.post(
        "/api/analyze/document",
        json={"file_id": file_id}
    )
    assert response.status_code == 200
    
    # Generate
    response = client.post(
        "/api/generate/test-cases",
        json={
            "file_id": file_id,
            "num_test_cases": 5
        }
    )
    assert response.status_code == 200
    assert len(response.json()["test_cases"]) == 5
    
    # Export
    response = client.post(
        "/api/export/test-cases",
        json={
            "file_id": file_id,
            "format": "docx"
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == \
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
```

---

## Debugging

### Enable Debug Logging

**Create** `app/config/logging.py`:
```python
import logging
import sys

def setup_logging():
    """Configure logging for development."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

logger = logging.getLogger(__name__)
```

**Use in code**:
```python
from app.config.logging import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Browser DevTools

**Network Tab**:
- Monitor API requests
- Check response headers
- View request/response payloads

**Console Tab**:
```javascript
// Check if API is accessible
fetch('/api/health').then(r => r.json()).then(console.log)

// Monitor WebSocket (if added)
ws = new WebSocket('ws://localhost:8000/ws')

// Log all fetch calls
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('Fetch:', args[0]);
    return originalFetch(...args);
}
```

**Application Tab**:
- Check localStorage
- View cookies
- Inspect session storage

---

## Performance Optimization

### Backend Optimization

**1. Async Processing**:
```python
# Slow - blocks execution
def process_file(file_path):
    result = expensive_operation()
    return result

# Fast - non-blocking
async def process_file(file_path):
    result = await expensive_operation()
    return result
```

**2. Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def parse_file(file_path: str) -> str:
    """Cached parsing - returns stored result on repeated calls."""
    # Implementation
    pass
```

**3. Lazy Loading**:
```python
# Load dependencies only when needed
from typing import Optional

class DocumentParser:
    _pdf_parser = None
    
    @property
    def pdf_parser(self):
        if self._pdf_parser is None:
            import PyPDF2
            self._pdf_parser = PyPDF2
        return self._pdf_parser
    
    def parse_pdf(self, file_path):
        """PDF parser loaded only when first used."""
        return self.pdf_parser.PdfReader(file_path)
```

### Frontend Optimization

**1. Code Splitting**:
```javascript
// Load modules on demand
async function loadFeature() {
    const module = await import('./features/heavy-module.js');
    module.initialize();
}
```

**2. Minimize DOM Operations**:
```javascript
// Slow - causes multiple reflows
for (let i = 0; i < 1000; i++) {
    document.body.innerHTML += '<div>' + i + '</div>';
}

// Fast - batch DOM updates
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
    const div = document.createElement('div');
    div.textContent = i;
    fragment.appendChild(div);
}
document.body.appendChild(fragment);
```

**3. Debouncing**:
```javascript
// Slow - fires on every keystroke
input.addEventListener('input', (e) => {
    fetch(`/api/search?q=${e.target.value}`);
});

// Fast - waits for user to stop typing
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

input.addEventListener('input', debounce((e) => {
    fetch(`/api/search?q=${e.target.value}`);
}, 300));
```

---

## Deployment

### Local Development

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Production Deployment

**Using Gunicorn + Uvicorn**:
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Using Docker**:

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY public/ ./public/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t myqa-agent .
docker run -p 8000:8000 myqa-agent
```

**Using Docker Compose**:

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_API_KEY=${LLM_API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./exports:/app/exports
```

Run:
```bash
docker-compose up
```

### Environment Configuration

Create `.env` file:
```
LLM_API_KEY=your-api-key-here
DEBUG=false
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=50000000
ALLOWED_ORIGINS=https://myapp.com
```

Load in code:
```python
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

## Troubleshooting

### Common Issues

**Issue**: ModuleNotFoundError
```python
# Solution: Ensure app package is installed in development mode
pip install -e .
```

**Issue**: Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

**Issue**: CORS errors in browser
```python
# Check CORS configuration in app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Best Practices](https://www.python.org/dev/peps/pep-0008/)
- [JavaScript Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [REST API Design](https://restfulapi.net/)

---

**Last Updated**: April 7, 2024
**Version**: 1.0.0
**Status**: ✅ Ready for Development
