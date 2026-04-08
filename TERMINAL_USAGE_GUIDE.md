# MyQA Agent - Terminal/CLI Usage Guide

## 🖥️ Using MyQA Agent Without UI (Pure Python/Command Line)

This guide provides all Python commands and scripts to use MyQA Agent programmatically without the web interface.

---

## Table of Contents

1. [Setup & Installation](#setup--installation)
2. [Python API Examples](#python-api-examples)
3. [Complete Workflow Scripts](#complete-workflow-scripts)
4. [Individual Operation Examples](#individual-operation-examples)
5. [Advanced Usage](#advanced-usage)

---

## Setup & Installation

### Step 1: Activate Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 2: Verify Installation

```python
python -c "import fastapi, pydantic, PyPDF2; print('All dependencies installed!')"
```

### Step 3: Start Server (Background)

```bash
# Windows - Start in background
START /B .venv\Scripts\uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# macOS/Linux - Start in background
nohup .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
```

---

## Python API Examples

### Basic Setup

```python
import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
UPLOADS_DIR = Path("uploads")
EXPORTS_DIR = Path("exports")

# Ensure directories exist
UPLOADS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)
```

### 1. Health Check

```python
import requests

response = requests.get("http://localhost:8000/health")
print("Server Status:", response.json())

# Output: {'status': 'healthy', 'timestamp': '2024-04-07T...'}
```

### 2. Upload Document

```python
import requests

def upload_document(file_path):
    """Upload a document (PDF, DOCX, or TXT)"""
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(
            f"{BASE_URL}/api/upload/document",
            files=files
        )
    
    if response.status_code == 200:
        data = response.json()
        file_id = data["file_id"]
        print(f"✓ File uploaded successfully!")
        print(f"  File ID: {file_id}")
        print(f"  File Name: {data['file_name']}")
        print(f"  File Size: {data['file_size']} bytes")
        return file_id
    else:
        print(f"✗ Upload failed: {response.status_code}")
        print(response.json())
        return None

# Usage
file_id = upload_document("sample_requirements.txt")
```

### 3. Analyze Document

```python
import requests
import json

def analyze_document(file_id):
    """Extract requirements from uploaded document"""
    response = requests.post(
        f"{BASE_URL}/api/analyze/document",
        json={"file_id": file_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        analysis = data["analysis"]
        
        print("\n✓ Document Analysis Complete!")
        print("\n📋 User Stories:")
        for story in analysis["user_stories"][:3]:
            print(f"  • {story}")
        
        print("\n✅ Acceptance Criteria:")
        for criteria in analysis["acceptance_criteria"][:3]:
            print(f"  • {criteria}")
        
        print("\n📌 Business Rules:")
        for rule in analysis["business_rules"][:3]:
            print(f"  • {rule}")
        
        print("\n⚠️  Constraints:")
        for constraint in analysis["constraints"][:3]:
            print(f"  • {constraint}")
        
        print("\n📝 Summary:")
        print(f"  {analysis['document_summary'][:100]}...")
        
        return analysis
    else:
        print(f"✗ Analysis failed: {response.status_code}")
        print(response.json())
        return None

# Usage
analysis = analyze_document(file_id)
```

### 4. Generate Test Cases

```python
import requests
import json

def generate_test_cases(file_id, num_cases=10, positive=True, negative=True, boundary=True):
    """Generate test cases from requirements"""
    response = requests.post(
        f"{BASE_URL}/api/generate/test-cases",
        json={
            "file_id": file_id,
            "num_test_cases": num_cases,
            "include_positive": positive,
            "include_negative": negative,
            "include_boundary": boundary
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        test_cases = data["test_cases"]
        
        print(f"\n✓ Generated {data['total_count']} test cases!")
        
        for tc in test_cases:
            print(f"\n📌 {tc['test_case_id']}: {tc['name']}")
            print(f"   Type: {tc['test_type']} | Priority: {tc['priority']}")
            print(f"   Description: {tc['description']}")
            
            print(f"   Steps:")
            for step in tc["test_steps"]:
                print(f"     {step['step_number']}. {step['action']}")
                print(f"        Expected: {step['expected_result']}")
            
            print(f"   Pre-conditions: {tc['pre_conditions']}")
            print(f"   Expected Result: {tc['expected_result']}")
        
        return test_cases
    else:
        print(f"✗ Generation failed: {response.status_code}")
        print(response.json())
        return None

# Usage
test_cases = generate_test_cases(file_id, num_cases=5)
```

### 5. Export to Word

```python
import requests
from datetime import datetime

def export_to_word(file_id, output_file=None):
    """Export test cases to Word (.docx) format"""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"TestCases_{timestamp}.docx"
    
    response = requests.post(
        f"{BASE_URL}/api/export/test-cases",
        json={
            "file_id": file_id,
            "format": "docx"
        }
    )
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✓ Word document exported: {output_file}")
        return output_file
    else:
        print(f"✗ Export failed: {response.status_code}")
        print(response.json())
        return None

# Usage
word_file = export_to_word(file_id)
```

### 6. Export to Excel

```python
import requests
from datetime import datetime

def export_to_excel(file_id, output_file=None):
    """Export test cases to Excel (.xlsx) format"""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"TestCases_{timestamp}.xlsx"
    
    response = requests.post(
        f"{BASE_URL}/api/export/test-cases",
        json={
            "file_id": file_id,
            "format": "xlsx"
        }
    )
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✓ Excel document exported: {output_file}")
        return output_file
    else:
        print(f"✗ Export failed: {response.status_code}")
        print(response.json())
        return None

# Usage
excel_file = export_to_excel(file_id)
```

---

## Complete Workflow Scripts

### Script 1: Full Workflow (Simple)

Create file: `run_full_workflow.py`

```python
#!/usr/bin/env python
"""
MyQA Agent - Complete Workflow Script
Processes a document from upload to export
"""

import requests
import sys
from pathlib import Path
from datetime import datetime

BASE_URL = "http://localhost:8000"

def check_server():
    """Verify server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def upload_document(file_path):
    """Step 1: Upload document"""
    print("\n" + "="*60)
    print("STEP 1: UPLOADING DOCUMENT")
    print("="*60)
    
    if not Path(file_path).exists():
        print(f"✗ File not found: {file_path}")
        return None
    
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/upload/document",
            files={"file": f}
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Upload successful!")
        print(f"  File ID: {data['file_id']}")
        print(f"  Size: {data['file_size']} bytes")
        return data['file_id']
    else:
        print(f"✗ Upload failed: {response.status_code}")
        return None

def analyze_document(file_id):
    """Step 2: Analyze document"""
    print("\n" + "="*60)
    print("STEP 2: ANALYZING DOCUMENT")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/analyze/document",
        json={"file_id": file_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        analysis = data["analysis"]
        
        print(f"✓ Analysis complete!")
        print(f"  User Stories: {len(analysis['user_stories'])}")
        print(f"  Acceptance Criteria: {len(analysis['acceptance_criteria'])}")
        print(f"  Business Rules: {len(analysis['business_rules'])}")
        print(f"  Constraints: {len(analysis['constraints'])}")
        
        return analysis
    else:
        print(f"✗ Analysis failed: {response.status_code}")
        return None

def generate_test_cases(file_id, num_cases=10):
    """Step 3: Generate test cases"""
    print("\n" + "="*60)
    print("STEP 3: GENERATING TEST CASES")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/generate/test-cases",
        json={
            "file_id": file_id,
            "num_test_cases": num_cases,
            "include_positive": True,
            "include_negative": True,
            "include_boundary": True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Test cases generated: {data['total_count']}")
        
        # Show summary
        positive = sum(1 for tc in data['test_cases'] if tc['test_type'] == 'positive')
        negative = sum(1 for tc in data['test_cases'] if tc['test_type'] == 'negative')
        boundary = sum(1 for tc in data['test_cases'] if tc['test_type'] == 'boundary')
        
        print(f"  • Positive: {positive}")
        print(f"  • Negative: {negative}")
        print(f"  • Boundary: {boundary}")
        
        return data['test_cases']
    else:
        print(f"✗ Generation failed: {response.status_code}")
        return None

def export_test_cases(file_id, format_type="docx"):
    """Step 4: Export test cases"""
    print("\n" + "="*60)
    print(f"STEP 4: EXPORTING TO {format_type.upper()}")
    print("="*60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"TestCases_{timestamp}.{format_type}"
    
    response = requests.post(
        f"{BASE_URL}/api/export/test-cases",
        json={
            "file_id": file_id,
            "format": format_type
        }
    )
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✓ Exported successfully!")
        print(f"  File: {output_file}")
        print(f"  Size: {Path(output_file).stat().st_size} bytes")
        return output_file
    else:
        print(f"✗ Export failed: {response.status_code}")
        return None

def main():
    """Run complete workflow"""
    print("\n" + "="*60)
    print("MyQA AGENT - COMPLETE WORKFLOW")
    print("="*60)
    
    # Check server
    print("\nChecking server status...")
    if not check_server():
        print("✗ Server is not running!")
        print("  Start it with: .venv\\Scripts\\uvicorn app.main:app --reload")
        return
    print("✓ Server is running")
    
    # Get input file
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "sample_requirements.txt"
        print(f"\nUsing default file: {file_path}")
    
    # Run workflow
    file_id = upload_document(file_path)
    if not file_id:
        return
    
    analysis = analyze_document(file_id)
    if not analysis:
        return
    
    test_cases = generate_test_cases(file_id, num_cases=10)
    if not test_cases:
        return
    
    # Export in both formats
    word_file = export_test_cases(file_id, "docx")
    excel_file = export_test_cases(file_id, "xlsx")
    
    # Summary
    print("\n" + "="*60)
    print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nGenerated Files:")
    if word_file:
        print(f"  • Word: {word_file}")
    if excel_file:
        print(f"  • Excel: {excel_file}")
    print("\nWorkflow Duration: Complete")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python run_full_workflow.py sample_requirements.txt
```

---

### Script 2: Batch Processing (Multiple Files)

Create file: `batch_process.py`

```python
#!/usr/bin/env python
"""
MyQA Agent - Batch Processing Script
Process multiple documents at once
"""

import requests
from pathlib import Path
import json

BASE_URL = "http://localhost:8000"

def batch_process(input_dir=".", output_dir="batch_results"):
    """Process all documents in a directory"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Find all supported files
    files = list(Path(input_dir).glob("*.txt"))
    files += list(Path(input_dir).glob("*.pdf"))
    files += list(Path(input_dir).glob("*.docx"))
    
    if not files:
        print("No files found to process")
        return
    
    print(f"Found {len(files)} files to process\n")
    
    results = []
    
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Processing: {file_path.name}")
        
        # Upload
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/api/upload/document",
                files={"file": f}
            )
        
        if response.status_code != 200:
            print(f"  ✗ Upload failed")
            continue
        
        file_id = response.json()["file_id"]
        print(f"  ✓ Uploaded (ID: {file_id})")
        
        # Analyze
        response = requests.post(
            f"{BASE_URL}/api/analyze/document",
            json={"file_id": file_id}
        )
        
        if response.status_code != 200:
            print(f"  ✗ Analysis failed")
            continue
        
        analysis = response.json()["analysis"]
        print(f"  ✓ Analyzed")
        
        # Generate
        response = requests.post(
            f"{BASE_URL}/api/generate/test-cases",
            json={"file_id": file_id, "num_test_cases": 10}
        )
        
        if response.status_code != 200:
            print(f"  ✗ Generation failed")
            continue
        
        test_cases = response.json()["test_cases"]
        print(f"  ✓ Generated {len(test_cases)} test cases")
        
        # Export
        response = requests.post(
            f"{BASE_URL}/api/export/test-cases",
            json={"file_id": file_id, "format": "xlsx"}
        )
        
        if response.status_code == 200:
            output_file = f"{output_dir}/{file_path.stem}_TestCases.xlsx"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"  ✓ Exported to {output_file}\n")
            
            results.append({
                "file": file_path.name,
                "output": output_file,
                "test_cases": len(test_cases)
            })
    
    # Summary report
    print("\n" + "="*60)
    print("BATCH PROCESSING SUMMARY")
    print("="*60)
    print(f"Processed: {len(results)} files")
    print(f"Total test cases: {sum(r['test_cases'] for r in results)}")
    print(f"Output directory: {output_dir}")
    print("="*60)

if __name__ == "__main__":
    batch_process()
```

**Run it:**
```bash
python batch_process.py
```

---

### Script 3: Interactive CLI Menu

Create file: `interactive_cli.py`

```python
#!/usr/bin/env python
"""
MyQA Agent - Interactive CLI Menu
User-friendly command-line interface
"""

import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

class MyQAAgent:
    def __init__(self):
        self.file_id = None
        self.analysis = None
        self.test_cases = None
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("MyQA AGENT - Interactive CLI")
        print("="*50)
        print("1. Upload Document")
        print("2. Analyze Document")
        print("3. Generate Test Cases")
        print("4. Export to Word")
        print("5. Export to Excel")
        print("6. View Test Cases")
        print("7. Quick Workflow (All Steps)")
        print("8. Exit")
        print("="*50)
    
    def upload(self):
        """Upload document"""
        file_path = input("\nEnter file path: ").strip()
        
        if not Path(file_path).exists():
            print("✗ File not found")
            return
        
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/api/upload/document",
                files={"file": f}
            )
        
        if response.status_code == 200:
            self.file_id = response.json()["file_id"]
            print(f"✓ Uploaded successfully!")
            print(f"  File ID: {self.file_id}")
        else:
            print(f"✗ Upload failed: {response.json()}")
    
    def analyze(self):
        """Analyze document"""
        if not self.file_id:
            print("✗ No file uploaded. Upload a file first.")
            return
        
        response = requests.post(
            f"{BASE_URL}/api/analyze/document",
            json={"file_id": self.file_id}
        )
        
        if response.status_code == 200:
            self.analysis = response.json()["analysis"]
            print("✓ Analysis complete!")
            print(f"  User Stories: {len(self.analysis['user_stories'])}")
            print(f"  Acceptance Criteria: {len(self.analysis['acceptance_criteria'])}")
            print(f"  Business Rules: {len(self.analysis['business_rules'])}")
            print(f"  Constraints: {len(self.analysis['constraints'])}")
        else:
            print(f"✗ Analysis failed: {response.json()}")
    
    def generate(self):
        """Generate test cases"""
        if not self.file_id:
            print("✗ No file uploaded. Upload a file first.")
            return
        
        num_cases = input("Number of test cases (default 10): ").strip()
        num_cases = int(num_cases) if num_cases.isdigit() else 10
        
        response = requests.post(
            f"{BASE_URL}/api/generate/test-cases",
            json={
                "file_id": self.file_id,
                "num_test_cases": num_cases
            }
        )
        
        if response.status_code == 200:
            self.test_cases = response.json()["test_cases"]
            print(f"✓ Generated {len(self.test_cases)} test cases!")
        else:
            print(f"✗ Generation failed: {response.json()}")
    
    def export_word(self):
        """Export to Word"""
        if not self.file_id:
            print("✗ No file uploaded.")
            return
        
        response = requests.post(
            f"{BASE_URL}/api/export/test-cases",
            json={"file_id": self.file_id, "format": "docx"}
        )
        
        if response.status_code == 200:
            output = "TestCases.docx"
            with open(output, "wb") as f:
                f.write(response.content)
            print(f"✓ Exported to {output}")
        else:
            print(f"✗ Export failed: {response.json()}")
    
    def export_excel(self):
        """Export to Excel"""
        if not self.file_id:
            print("✗ No file uploaded.")
            return
        
        response = requests.post(
            f"{BASE_URL}/api/export/test-cases",
            json={"file_id": self.file_id, "format": "xlsx"}
        )
        
        if response.status_code == 200:
            output = "TestCases.xlsx"
            with open(output, "wb") as f:
                f.write(response.content)
            print(f"✓ Exported to {output}")
        else:
            print(f"✗ Export failed: {response.json()}")
    
    def view_test_cases(self):
        """Display test cases"""
        if not self.test_cases:
            print("✗ No test cases generated. Generate them first.")
            return
        
        for tc in self.test_cases[:5]:
            print(f"\n📌 {tc['test_case_id']}: {tc['name']}")
            print(f"   Type: {tc['test_type']} | Priority: {tc['priority']}")
            for step in tc['test_steps'][:2]:
                print(f"   Step {step['step_number']}: {step['action']}")
    
    def quick_workflow(self):
        """Run all steps"""
        file_path = input("\nEnter file path: ").strip()
        
        print("\n1. Uploading...")
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/api/upload/document",
                files={"file": f}
            )
        self.file_id = response.json()["file_id"]
        print("   ✓ Done")
        
        print("2. Analyzing...")
        response = requests.post(
            f"{BASE_URL}/api/analyze/document",
            json={"file_id": self.file_id}
        )
        self.analysis = response.json()["analysis"]
        print("   ✓ Done")
        
        print("3. Generating...")
        response = requests.post(
            f"{BASE_URL}/api/generate/test-cases",
            json={"file_id": self.file_id, "num_test_cases": 10}
        )
        self.test_cases = response.json()["test_cases"]
        print("   ✓ Done")
        
        print("4. Exporting...")
        response = requests.post(
            f"{BASE_URL}/api/export/test-cases",
            json={"file_id": self.file_id, "format": "xlsx"}
        )
        with open("TestCases.xlsx", "wb") as f:
            f.write(response.content)
        print("   ✓ Done")
        
        print("\n✅ Workflow completed!")
    
    def run(self):
        """Main loop"""
        while True:
            self.show_menu()
            choice = input("Enter choice (1-8): ").strip()
            
            if choice == "1":
                self.upload()
            elif choice == "2":
                self.analyze()
            elif choice == "3":
                self.generate()
            elif choice == "4":
                self.export_word()
            elif choice == "5":
                self.export_excel()
            elif choice == "6":
                self.view_test_cases()
            elif choice == "7":
                self.quick_workflow()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    agent = MyQAAgent()
    agent.run()
```

**Run it:**
```bash
python interactive_cli.py
```

---

## Individual Operation Examples

### Quick Copy-Paste Examples

**Health Check:**
```python
import requests
response = requests.get("http://localhost:8000/health")
print(response.json())
```

**Upload & Get ID:**
```python
import requests
with open("requirements.txt", "rb") as f:
    r = requests.post("http://localhost:8000/api/upload/document", files={"file": f})
file_id = r.json()["file_id"]
print(file_id)
```

**Analyze & Print Summary:**
```python
import requests
response = requests.post("http://localhost:8000/api/analyze/document", 
    json={"file_id": file_id})
analysis = response.json()["analysis"]
print(f"Stories: {len(analysis['user_stories'])}")
print(f"Criteria: {len(analysis['acceptance_criteria'])}")
```

**Generate & Save to File:**
```python
import requests
import json
response = requests.post("http://localhost:8000/api/generate/test-cases",
    json={"file_id": file_id, "num_test_cases": 10})
test_cases = response.json()["test_cases"]
with open("test_cases.json", "w") as f:
    json.dump(test_cases, f, indent=2)
print(f"Saved {len(test_cases)} test cases")
```

**Export & Verify:**
```python
import requests
response = requests.post("http://localhost:8000/api/export/test-cases",
    json={"file_id": file_id, "format": "docx"})
with open("output.docx", "wb") as f:
    f.write(response.content)
print(f"Exported {len(response.content)} bytes")
```

---

## Advanced Usage

### Using Environment Variables

```python
import os
import requests

BASE_URL = os.getenv("MYQA_API_URL", "http://localhost:8000")
FILE_PATH = os.getenv("MYQA_FILE", "sample_requirements.txt")

response = requests.get(f"{BASE_URL}/health")
print(f"Server: {BASE_URL}, Status: {response.status_code}")
```

Set variables:
```bash
# Windows
set MYQA_API_URL=http://localhost:8000
set MYQA_FILE=sample_requirements.txt

# macOS/Linux
export MYQA_API_URL=http://localhost:8000
export MYQA_FILE=sample_requirements.txt
```

### Error Handling

```python
import requests
from requests.exceptions import ConnectionError, Timeout

def safe_api_call(url, method="get", **kwargs):
    """Safe API call with error handling"""
    try:
        if method.lower() == "get":
            response = requests.get(url, timeout=10, **kwargs)
        else:
            response = requests.post(url, timeout=10, **kwargs)
        
        response.raise_for_status()
        return response
    
    except ConnectionError:
        print("✗ Connection failed. Is the server running?")
        return None
    except Timeout:
        print("✗ Request timed out")
        return None
    except requests.HTTPError as e:
        print(f"✗ HTTP Error: {e.response.status_code}")
        return None
```

### Logging Results

```python
import logging
from datetime import datetime

logging.basicConfig(
    filename=f"myqa_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

logger.info(f"Processing file: {file_path}")
logger.info(f"File ID: {file_id}")
logger.info(f"Generated {len(test_cases)} test cases")
logger.info(f"Exported to {output_file}")
```

---

## Commands Reference

| Task | Command |
|------|---------|
| **Start Server** | `.venv\Scripts\uvicorn app.main:app --reload` |
| **Run Full Workflow** | `python run_full_workflow.py sample_requirements.txt` |
| **Batch Process** | `python batch_process.py` |
| **Interactive CLI** | `python interactive_cli.py` |
| **Test Health** | `python -c "import requests; print(requests.get('http://localhost:8000/health').json())"` |

---

## Troubleshooting

### Server Not Responding

```python
import requests
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    print("Server is running")
except:
    print("Server is not running - start it first!")
```

### File Not Found

```python
from pathlib import Path

file_path = "requirements.txt"
if not Path(file_path).exists():
    print(f"File not found: {file_path}")
else:
    print(f"File found: {file_path}")
```

### API Error

```python
response = requests.post(url, json=data)
if response.status_code != 200:
    print(f"Error {response.status_code}:")
    print(response.json())
```

---

## Summary

You now have multiple ways to use MyQA Agent without the UI:

1. **Simple Scripts** - Copy-paste individual operations
2. **Full Workflow** - `run_full_workflow.py` - Single command processing
3. **Batch Processing** - `batch_process.py` - Process multiple files
4. **Interactive CLI** - `interactive_cli.py` - Menu-driven interface

**Choose based on your needs!**

---

**Last Updated**: April 7, 2024
**Version**: 1.0.0
