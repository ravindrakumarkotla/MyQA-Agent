"""
API Testing Guide - AI QA Agent

This document provides comprehensive examples for testing all API endpoints
using curl, PowerShell, Python, and other tools.
"""

# ============================================================================
# API ENDPOINT TESTING GUIDE
# ============================================================================

## Base URL
BASE_URL = "http://localhost:8000"

## Health Check Endpoint

### Using curl
GET http://localhost:8000/health

curl -X GET "http://localhost:8000/health"

### Using PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

### Using Python
import requests
response = requests.get("http://localhost:8000/health")
print(response.json())

---

## API Endpoints Reference

### 1. Upload Document
**Endpoint**: POST /api/upload/document
**Description**: Upload a document for analysis (PDF, DOCX, TXT)
**Request**: Multipart form data with file
**Response**: JSON with file_id and upload details

#### Example: Upload with curl
```bash
curl -X POST "http://localhost:8000/api/upload/document" \
  -F "file=@sample_requirements.txt"
```

#### Example: Upload with PowerShell
```powershell
$file = "sample_requirements.txt"
curl -X POST "http://localhost:8000/api/upload/document" `
  -F "file=@$file"
```

#### Example: Upload with Python
```python
import requests

file_path = "sample_requirements.txt"
with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/api/upload/document",
        files=files
    )
    print(response.json())
```

#### Response Example:
```json
{
  "success": true,
  "file_id": "20240407_123456_sample_requirements.txt",
  "file_name": "sample_requirements.txt",
  "file_size": 4521,
  "upload_time": "2024-04-07T12:34:56.789123",
  "message": "File 'sample_requirements.txt' uploaded successfully"
}
```

---

### 2. Analyze Document
**Endpoint**: POST /api/analyze/document
**Description**: Extract structured information from uploaded document
**Request**: JSON with file_id
**Response**: JSON with extracted analysis

#### Example: Analyze with curl
```bash
curl -X POST "http://localhost:8000/api/analyze/document" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "20240407_123456_sample_requirements.txt"}'
```

#### Example: Analyze with PowerShell
```powershell
$body = @{
    file_id = "20240407_123456_sample_requirements.txt"
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/analyze/document" `
  -H "Content-Type: application/json" `
  -d $body
```

#### Example: Analyze with Python
```python
import requests
import json

file_id = "20240407_123456_sample_requirements.txt"
response = requests.post(
    "http://localhost:8000/api/analyze/document",
    json={"file_id": file_id}
)
analysis = response.json()
print(json.dumps(analysis, indent=2))
```

#### Response Example:
```json
{
  "success": true,
  "file_id": "20240407_123456_sample_requirements.txt",
  "analysis": {
    "user_stories": [
      "As a new user of the e-commerce platform, I want to register a new account with email and password"
    ],
    "acceptance_criteria": [
      "Given I am on the registration page, when I enter valid email and password, then my account should be created"
    ],
    "preconditions": [
      "The registration page is accessible and loaded"
    ],
    "business_rules": [
      "Email must be unique in the system"
    ],
    "constraints": [
      "Registration process must complete within 3 seconds"
    ],
    "document_summary": "Project: E-Commerce Platform - User Authentication Module..."
  },
  "message": "Document analysis completed successfully"
}
```

---

### 3. Generate Test Cases
**Endpoint**: POST /api/generate/test-cases
**Description**: Generate manual test cases based on document analysis
**Request**: JSON with file_id and generation parameters
**Response**: JSON with generated test cases

#### Request Parameters:
- `file_id` (string, required): File ID from upload
- `num_test_cases` (integer, optional): Number of test cases (1-20, default: 5)
- `include_positive` (boolean, optional): Include positive scenarios (default: true)
- `include_negative` (boolean, optional): Include negative scenarios (default: true)
- `include_boundary` (boolean, optional): Include boundary scenarios (default: true)

#### Example: Generate with curl
```bash
curl -X POST "http://localhost:8000/api/generate/test-cases" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_sample_requirements.txt",
    "num_test_cases": 10,
    "include_positive": true,
    "include_negative": true,
    "include_boundary": true
  }'
```

#### Example: Generate with PowerShell
```powershell
$body = @{
    file_id = "20240407_123456_sample_requirements.txt"
    num_test_cases = 10
    include_positive = $true
    include_negative = $true
    include_boundary = $true
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/generate/test-cases" `
  -H "Content-Type: application/json" `
  -d $body
```

#### Example: Generate with Python
```python
import requests

file_id = "20240407_123456_sample_requirements.txt"
response = requests.post(
    "http://localhost:8000/api/generate/test-cases",
    json={
        "file_id": file_id,
        "num_test_cases": 10,
        "include_positive": True,
        "include_negative": True,
        "include_boundary": True
    }
)
test_cases = response.json()
print(f"Generated {test_cases['total_count']} test cases")
for tc in test_cases['test_cases'][:3]:
    print(f"  - {tc['test_case_id']}: {tc['name']}")
```

#### Response Example:
```json
{
  "success": true,
  "file_id": "20240407_123456_sample_requirements.txt",
  "test_cases": [
    {
      "test_case_id": "TC_POS_001",
      "name": "Positive Test Case 1 - Feature Test",
      "description": "Verify successful execution of the feature described in user story",
      "pre_condition": "User is logged in and has necessary permissions",
      "test_steps": [
        {
          "step_number": 1,
          "action": "Navigate to the feature page",
          "expected_result": "Feature page loads successfully"
        },
        {
          "step_number": 2,
          "action": "Fill in required fields with valid data",
          "expected_result": "All fields accept the valid data"
        },
        {
          "step_number": 3,
          "action": "Submit the form",
          "expected_result": "Form submission is successful with confirmation message"
        }
      ],
      "expected_result": "Feature operates as expected with all acceptance criteria met",
      "test_type": "positive",
      "priority": "high"
    }
  ],
  "total_count": 10,
  "message": "Successfully generated 10 test cases"
}
```

---

### 4. Export Test Cases to Word
**Endpoint**: POST /api/export/test-cases
**Description**: Export generated test cases to Word (.docx) format
**Request**: JSON with file_id and format
**Response**: Binary file (Word document)

#### Example: Export to Word with curl
```bash
curl -X POST "http://localhost:8000/api/export/test-cases" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_sample_requirements.txt",
    "format": "docx",
    "num_test_cases": 10
  }' \
  -o TestCases.docx
```

#### Example: Export to Word with PowerShell
```powershell
$body = @{
    file_id = "20240407_123456_sample_requirements.txt"
    format = "docx"
    num_test_cases = 10
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d $body `
  -o TestCases.docx

Write-Host "Word document exported: TestCases.docx"
```

#### Example: Export to Word with Python
```python
import requests

file_id = "20240407_123456_sample_requirements.txt"
response = requests.post(
    "http://localhost:8000/api/export/test-cases",
    json={
        "file_id": file_id,
        "format": "docx",
        "num_test_cases": 10
    }
)

if response.status_code == 200:
    with open("TestCases.docx", "wb") as f:
        f.write(response.content)
    print("Word document exported successfully")
else:
    print(f"Error: {response.status_code}")
```

---

### 5. Export Test Cases to Excel
**Endpoint**: POST /api/export/test-cases
**Description**: Export generated test cases to Excel (.xlsx) format
**Request**: JSON with file_id and format
**Response**: Binary file (Excel spreadsheet)

#### Example: Export to Excel with curl
```bash
curl -X POST "http://localhost:8000/api/export/test-cases" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_sample_requirements.txt",
    "format": "xlsx",
    "num_test_cases": 10
  }' \
  -o TestCases.xlsx
```

#### Example: Export to Excel with PowerShell
```powershell
$body = @{
    file_id = "20240407_123456_sample_requirements.txt"
    format = "xlsx"
    num_test_cases = 10
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d $body `
  -o TestCases.xlsx

Write-Host "Excel document exported: TestCases.xlsx"
```

#### Example: Export to Excel with Python
```python
import requests

file_id = "20240407_123456_sample_requirements.txt"
response = requests.post(
    "http://localhost:8000/api/export/test-cases",
    json={
        "file_id": file_id,
        "format": "xlsx",
        "num_test_cases": 10
    }
)

if response.status_code == 200:
    with open("TestCases.xlsx", "wb") as f:
        f.write(response.content)
    print("Excel document exported successfully")
else:
    print(f"Error: {response.status_code}")
```

---

## Complete Workflow Scripts

### PowerShell Complete Workflow
```powershell
# AI QA Agent - Complete Workflow Script for PowerShell

# Configuration
$baseUrl = "http://localhost:8000"
$filePath = "sample_requirements.txt"

# Step 1: Upload Document
Write-Host "Step 1: Uploading document..." -ForegroundColor Green
$uploadResponse = curl -X POST "$baseUrl/api/upload/document" `
  -F "file=@$filePath" | ConvertFrom-Json

$fileId = $uploadResponse.file_id
Write-Host "  ✓ File uploaded with ID: $fileId" -ForegroundColor Green

# Step 2: Analyze Document
Write-Host "`nStep 2: Analyzing document..." -ForegroundColor Green
$analysisBody = @{
    file_id = $fileId
} | ConvertTo-Json

$analysisResponse = curl -X POST "$baseUrl/api/analyze/document" `
  -H "Content-Type: application/json" `
  -d $analysisBody | ConvertFrom-Json

Write-Host "  ✓ Analysis completed" -ForegroundColor Green
Write-Host "  • User stories: $($analysisResponse.analysis.user_stories.Count)" -ForegroundColor Cyan
Write-Host "  • Acceptance criteria: $($analysisResponse.analysis.acceptance_criteria.Count)" -ForegroundColor Cyan

# Step 3: Generate Test Cases
Write-Host "`nStep 3: Generating test cases..." -ForegroundColor Green
$generateBody = @{
    file_id = $fileId
    num_test_cases = 10
    include_positive = $true
    include_negative = $true
    include_boundary = $true
} | ConvertTo-Json

$generateResponse = curl -X POST "$baseUrl/api/generate/test-cases" `
  -H "Content-Type: application/json" `
  -d $generateBody | ConvertFrom-Json

Write-Host "  ✓ Test cases generated: $($generateResponse.total_count)" -ForegroundColor Green
foreach ($tc in $generateResponse.test_cases | Select-Object -First 3) {
    Write-Host "    - $($tc.test_case_id): $($tc.name)" -ForegroundColor Cyan
}

# Step 4: Export to Word
Write-Host "`nStep 4: Exporting to Word (.docx)..." -ForegroundColor Green
$exportBody = @{
    file_id = $fileId
    format = "docx"
    num_test_cases = 10
} | ConvertTo-Json

curl -X POST "$baseUrl/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d $exportBody `
  -o "TestCases.docx"

Write-Host "  ✓ Word document exported: TestCases.docx" -ForegroundColor Green

# Step 5: Export to Excel
Write-Host "`nStep 5: Exporting to Excel (.xlsx)..." -ForegroundColor Green
$exportBody = @{
    file_id = $fileId
    format = "xlsx"
    num_test_cases = 10
} | ConvertTo-Json

curl -X POST "$baseUrl/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d $exportBody `
  -o "TestCases.xlsx"

Write-Host "  ✓ Excel document exported: TestCases.xlsx" -ForegroundColor Green

Write-Host "`n✅ Workflow completed successfully!" -ForegroundColor Green
```

### Python Complete Workflow
```python
#!/usr/bin/env python
"""AI QA Agent - Complete Workflow Script for Python"""

import requests
import json

def main():
    base_url = "http://localhost:8000"
    file_path = "sample_requirements.txt"
    
    # Step 1: Upload Document
    print("\nStep 1: Uploading document...")
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(
            f"{base_url}/api/upload/document",
            files=files
        )
    
    upload_data = response.json()
    file_id = upload_data["file_id"]
    print(f"  ✓ File uploaded with ID: {file_id}")
    
    # Step 2: Analyze Document
    print("\nStep 2: Analyzing document...")
    response = requests.post(
        f"{base_url}/api/analyze/document",
        json={"file_id": file_id}
    )
    
    analysis = response.json()
    print("  ✓ Analysis completed")
    print(f"  • User stories: {len(analysis['analysis']['user_stories'])}")
    print(f"  • Acceptance criteria: {len(analysis['analysis']['acceptance_criteria'])}")
    
    # Step 3: Generate Test Cases
    print("\nStep 3: Generating test cases...")
    response = requests.post(
        f"{base_url}/api/generate/test-cases",
        json={
            "file_id": file_id,
            "num_test_cases": 10,
            "include_positive": True,
            "include_negative": True,
            "include_boundary": True
        }
    )
    
    test_cases = response.json()
    print(f"  ✓ Test cases generated: {test_cases['total_count']}")
    for tc in test_cases["test_cases"][:3]:
        print(f"    - {tc['test_case_id']}: {tc['name']}")
    
    # Step 4: Export to Word
    print("\nStep 4: Exporting to Word (.docx)...")
    response = requests.post(
        f"{base_url}/api/export/test-cases",
        json={
            "file_id": file_id,
            "format": "docx",
            "num_test_cases": 10
        }
    )
    
    with open("TestCases.docx", "wb") as f:
        f.write(response.content)
    print("  ✓ Word document exported: TestCases.docx")
    
    # Step 5: Export to Excel
    print("\nStep 5: Exporting to Excel (.xlsx)...")
    response = requests.post(
        f"{base_url}/api/export/test-cases",
        json={
            "file_id": file_id,
            "format": "xlsx",
            "num_test_cases": 10
        }
    )
    
    with open("TestCases.xlsx", "wb") as f:
        f.write(response.content)
    print("  ✓ Excel document exported: TestCases.xlsx")
    
    print("\n✅ Workflow completed successfully!")

if __name__ == "__main__":
    main()
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Unsupported file format. Allowed formats: {'.pdf', '.docx', '.txt'}"
}
```

#### 404 Not Found
```json
{
  "error": "Not Found",
  "detail": "File with ID 'invalid_id' not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "detail": "An unexpected error occurred. Please try again later."
}
```

---

## Testing Checklist

- [ ] Test upload endpoint with valid files (PDF, DOCX, TXT)
- [ ] Test upload with unsupported file format
- [ ] Test upload with missing file
- [ ] Test analyze endpoint with valid file_id
- [ ] Test analyze endpoint with invalid file_id
- [ ] Test generate endpoint with various num_test_cases values
- [ ] Test generate with include_positive/negative/boundary combinations
- [ ] Test export to DOCX format
- [ ] Test export to XLSX format
- [ ] Test export with invalid format
- [ ] Test health check endpoint
- [ ] Test API documentation (Swagger UI)
- [ ] Test concurrent requests
- [ ] Verify exported files are readable

---

**Last Updated**: April 7, 2024
