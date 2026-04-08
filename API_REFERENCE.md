# AI QA Agent - API Reference Guide

## 📚 Complete API Documentation

---

## 1. Upload Document

### Endpoint
```
POST /api/upload/document
```

### Purpose
Upload a document (PDF, DOCX, or TXT) for analysis and test case generation.

### Request

**Content-Type**: `multipart/form-data`

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file` | File | Yes | Document file (PDF, DOCX, or TXT) |

**Constraints**:
- Maximum file size: 50 MB
- Supported formats: `.pdf`, `.docx`, `.txt`
- File must be readable and valid

### Response

**Status**: `200 OK`

**Response Body** (JSON):
```json
{
  "success": true,
  "file_id": "20240407_150530_requirements",
  "file_name": "requirements.pdf",
  "file_size": 245678,
  "upload_time": "2024-04-07T15:05:30.123456",
  "message": "File uploaded successfully"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `file_id` | string | Unique identifier for uploaded file |
| `file_name` | string | Original filename |
| `file_size` | integer | File size in bytes |
| `upload_time` | string | ISO 8601 timestamp |
| `message` | string | Human-readable message |

### cURL Example
```bash
curl -X POST http://localhost:8000/api/upload/document \
  -F "file=@requirements.pdf"
```

### JavaScript Example
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/upload/document', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log('File ID:', data.file_id);
```

### Python Example
```python
import requests

with open('requirements.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/upload/document',
        files=files
    )

file_id = response.json()['file_id']
```

### Error Responses

**400 Bad Request** - No file provided:
```json
{
  "detail": "No file provided"
}
```

**400 Bad Request** - Invalid file format:
```json
{
  "detail": "Unsupported file format. Supported formats: PDF, DOCX, TXT"
}
```

**413 Payload Too Large** - File exceeds size limit:
```json
{
  "detail": "File size exceeds 50MB limit"
}
```

---

## 2. Analyze Document

### Endpoint
```
POST /api/analyze/document
```

### Purpose
Analyze uploaded document to extract requirements, user stories, acceptance criteria, business rules, and constraints.

### Request

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "file_id": "20240407_150530_requirements"
}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file_id` | string | Yes | File ID from upload endpoint |

### Response

**Status**: `200 OK`

**Response Body** (JSON):
```json
{
  "success": true,
  "file_id": "20240407_150530_requirements",
  "analysis": {
    "user_stories": [
      "As a customer, I want to register an account so that I can access the platform",
      "As a user, I want to reset my password so that I can regain access to my account"
    ],
    "acceptance_criteria": [
      "Registration form validates email format",
      "Password must be at least 8 characters",
      "System sends confirmation email",
      "User can login with registered credentials"
    ],
    "business_rules": [
      "Only one account per email address",
      "Password must contain uppercase and lowercase letters",
      "Account must be verified within 24 hours"
    ],
    "constraints": [
      "Must comply with GDPR regulations",
      "Support must work on Chrome, Firefox, Safari",
      "Response time < 2 seconds"
    ],
    "document_summary": "User registration and account management system requirements including email validation, password policies, and account verification."
  },
  "message": "Document analyzed successfully"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `file_id` | string | File ID being analyzed |
| `analysis` | object | Extracted requirements |
| `analysis.user_stories` | array | List of user stories |
| `analysis.acceptance_criteria` | array | List of acceptance criteria |
| `analysis.business_rules` | array | List of business rules |
| `analysis.constraints` | array | List of constraints |
| `analysis.document_summary` | string | Overall document summary |
| `message` | string | Human-readable message |

### cURL Example
```bash
curl -X POST http://localhost:8000/api/analyze/document \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_150530_requirements"
  }'
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:8000/api/analyze/document', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    file_id: '20240407_150530_requirements'
  })
});

const data = await response.json();
console.log('User Stories:', data.analysis.user_stories);
console.log('Acceptance Criteria:', data.analysis.acceptance_criteria);
```

### Python Example
```python
import requests
import json

response = requests.post(
    'http://localhost:8000/api/analyze/document',
    json={'file_id': '20240407_150530_requirements'}
)

analysis = response.json()['analysis']
print(f"User Stories: {analysis['user_stories']}")
print(f"Acceptance Criteria: {analysis['acceptance_criteria']}")
```

### Error Responses

**404 Not Found** - File not found:
```json
{
  "detail": "File not found"
}
```

**500 Internal Server Error** - Parse error:
```json
{
  "detail": "Error parsing document"
}
```

---

## 3. Generate Test Cases

### Endpoint
```
POST /api/generate/test-cases
```

### Purpose
Generate test cases based on extracted requirements with filtering options.

### Request

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "file_id": "20240407_150530_requirements",
  "num_test_cases": 10,
  "include_positive": true,
  "include_negative": true,
  "include_boundary": true
}
```

**Parameters**:
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `file_id` | string | Yes | - | File ID from upload |
| `num_test_cases` | integer | No | 10 | Number of test cases (5-20) |
| `include_positive` | boolean | No | true | Include positive test cases |
| `include_negative` | boolean | No | true | Include negative test cases |
| `include_boundary` | boolean | No | true | Include boundary test cases |

### Response

**Status**: `200 OK`

**Response Body** (JSON):
```json
{
  "success": true,
  "file_id": "20240407_150530_requirements",
  "test_cases": [
    {
      "test_case_id": "TC_001_POSITIVE_REG",
      "name": "Successful User Registration",
      "description": "Verify user can successfully register with valid credentials",
      "test_type": "positive",
      "priority": "high",
      "test_steps": [
        {
          "step_number": 1,
          "action": "Navigate to registration page",
          "expected_result": "Registration form displayed"
        },
        {
          "step_number": 2,
          "action": "Enter valid email: test@example.com",
          "expected_result": "Email field accepts input"
        },
        {
          "step_number": 3,
          "action": "Enter password: SecurePass123",
          "expected_result": "Password meets requirements"
        },
        {
          "step_number": 4,
          "action": "Click Register button",
          "expected_result": "Account created, confirmation email sent"
        }
      ],
      "expected_result": "User successfully registered with confirmation pending",
      "pre_conditions": "User not already registered",
      "post_conditions": "Confirmation email in user's inbox"
    },
    {
      "test_case_id": "TC_002_NEGATIVE_EMAIL",
      "name": "Invalid Email Format Registration",
      "description": "Verify system rejects invalid email formats",
      "test_type": "negative",
      "priority": "high",
      "test_steps": [
        {
          "step_number": 1,
          "action": "Navigate to registration page",
          "expected_result": "Registration form displayed"
        },
        {
          "step_number": 2,
          "action": "Enter invalid email: notanemail",
          "expected_result": "Form shows validation error"
        }
      ],
      "expected_result": "Registration rejected with error message",
      "pre_conditions": "User on registration page",
      "post_conditions": "No account created"
    },
    {
      "test_case_id": "TC_003_BOUNDARY_PWD",
      "name": "Password Length Boundary Test",
      "description": "Test password with exactly 8 characters (minimum)",
      "test_type": "boundary",
      "priority": "medium",
      "test_steps": [
        {
          "step_number": 1,
          "action": "Enter password: Pass1234 (8 chars)",
          "expected_result": "Password accepted as meeting minimum requirement"
        }
      ],
      "expected_result": "Password validation passes",
      "pre_conditions": "On registration form",
      "post_conditions": "User can proceed with registration"
    }
  ],
  "total_count": 3,
  "message": "Test cases generated successfully"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `file_id` | string | File ID used for generation |
| `test_cases` | array | List of generated test cases |
| `test_cases[].test_case_id` | string | Unique test case identifier |
| `test_cases[].name` | string | Test case name |
| `test_cases[].description` | string | Detailed description |
| `test_cases[].test_type` | string | Type: positive, negative, boundary |
| `test_cases[].priority` | string | Priority: high, medium, low |
| `test_cases[].test_steps` | array | Array of test steps |
| `test_cases[].expected_result` | string | Expected outcome |
| `test_cases[].pre_conditions` | string | Setup requirements |
| `test_cases[].post_conditions` | string | Final state after test |
| `total_count` | integer | Number of test cases generated |
| `message` | string | Human-readable message |

### Test Type Definitions

**Positive Test Cases**:
- Valid inputs and normal flows
- Happy path scenarios
- Expected behavior verification

**Negative Test Cases**:
- Invalid inputs and error conditions
- Edge case handling
- Error message validation

**Boundary Test Cases**:
- Minimum/maximum values
- Boundary conditions
- Limit testing

### cURL Example
```bash
curl -X POST http://localhost:8000/api/generate/test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_150530_requirements",
    "num_test_cases": 15,
    "include_positive": true,
    "include_negative": true,
    "include_boundary": true
  }'
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:8000/api/generate/test-cases', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    file_id: '20240407_150530_requirements',
    num_test_cases: 10,
    include_positive: true,
    include_negative: true,
    include_boundary: false  // Exclude boundary tests
  })
});

const data = await response.json();
data.test_cases.forEach(tc => {
  console.log(`${tc.test_case_id}: ${tc.name} (${tc.priority})`);
});
```

### Python Example
```python
import requests

response = requests.post(
    'http://localhost:8000/api/generate/test-cases',
    json={
        'file_id': '20240407_150530_requirements',
        'num_test_cases': 10,
        'include_positive': True,
        'include_negative': True,
        'include_boundary': True
    }
)

test_cases = response.json()['test_cases']
for tc in test_cases:
    print(f"Test ID: {tc['test_case_id']}")
    print(f"Name: {tc['name']}")
    print(f"Type: {tc['test_type']}")
```

### Error Responses

**404 Not Found** - File not found:
```json
{
  "detail": "File not found"
}
```

**422 Unprocessable Entity** - Invalid parameters:
```json
{
  "detail": [
    {
      "loc": ["body", "num_test_cases"],
      "msg": "ensure this value is less than or equal to 20",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

## 4. Export Test Cases

### Endpoint
```
POST /api/export/test-cases
```

### Purpose
Export generated test cases to Word (.docx) or Excel (.xlsx) format.

### Request

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "file_id": "20240407_150530_requirements",
  "format": "docx",
  "num_test_cases": 10
}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file_id` | string | Yes | File ID from upload |
| `format` | string | Yes | Export format: "docx" or "xlsx" |
| `num_test_cases` | integer | No | Number of test cases to export (default: all) |

### Response

**Status**: `200 OK`

**Response Type**: Binary file (application/octet-stream)

**Response Headers**:
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="TestCases_20240407_150530.docx"
```

### Export Formats

#### Word Format (.docx)
- Professional document layout
- Tables with formatted headers
- Page breaks between sections
- Metadata (date, file name)
- Recommended for: Printing, distribution, formal documentation

**Word Document Structure**:
```
┌────────────────────────────────────┐
│ Test Cases Report                  │
│ Generated: 2024-04-07 15:05:30     │
│ Source: requirements.pdf           │
│ Total Test Cases: 10               │
└────────────────────────────────────┘
│
├─ Section 1: Summary
│  └─ Overview table (test counts)
│
├─ Section 2: Test Cases Details
│  ├─ Test Case 1
│  │  ├─ ID, Name, Type, Priority
│  │  ├─ Description
│  │  ├─ Pre-conditions
│  │  ├─ Test Steps (table)
│  │  ├─ Expected Result
│  │  └─ Post-conditions
│  │
│  ├─ Test Case 2
│  │  └─ [Same structure]
│  ...
```

#### Excel Format (.xlsx)
- Structured data with multiple sheets
- Color-coded by test type
- Sortable and filterable columns
- Pivot table ready
- Recommended for: Data analysis, tracking, automation

**Excel Sheet Structure**:
```
Sheet 1: Summary
├─ Total Test Cases
├─ Positive Count
├─ Negative Count
└─ Boundary Count

Sheet 2: Test Cases
├─ Column A: Test ID
├─ Column B: Name
├─ Column C: Type
├─ Column D: Priority
├─ Column E: Description
├─ Column F: Pre-conditions
├─ Column G: Test Steps
├─ Column H: Expected Result
├─ Column I: Post-conditions
│
Row 2: [Test Case 1 data]
Row 3: [Test Case 2 data]
...
```

### cURL Example - Word Export
```bash
curl -X POST http://localhost:8000/api/export/test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_150530_requirements",
    "format": "docx"
  }' \
  --output TestCases.docx
```

### cURL Example - Excel Export
```bash
curl -X POST http://localhost:8000/api/export/test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_150530_requirements",
    "format": "xlsx"
  }' \
  --output TestCases.xlsx
```

### JavaScript Example
```javascript
async function exportTestCases(fileId, format) {
  const response = await fetch('http://localhost:8000/api/export/test-cases', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      file_id: fileId,
      format: format,  // 'docx' or 'xlsx'
      num_test_cases: 10
    })
  });

  // Get the filename from response headers
  const contentDisposition = response.headers.get('content-disposition');
  const filename = contentDisposition
    .split('filename=')[1]
    .replace(/"/g, '');

  // Download the file
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

// Usage
exportTestCases('20240407_150530_requirements', 'docx');
```

### Python Example
```python
import requests

response = requests.post(
    'http://localhost:8000/api/export/test-cases',
    json={
        'file_id': '20240407_150530_requirements',
        'format': 'docx',
        'num_test_cases': 10
    }
)

# Extract filename from headers
filename = response.headers.get('content-disposition').split('filename=')[1]

# Save file
with open(filename, 'wb') as f:
    f.write(response.content)

print(f"File saved: {filename}")
```

### Error Responses

**404 Not Found** - File not found:
```json
{
  "detail": "File not found"
}
```

**400 Bad Request** - Invalid format:
```json
{
  "detail": "Invalid format. Supported formats: docx, xlsx"
}
```

---

## 5. Health Check

### Endpoint
```
GET /health
```

### Purpose
Check if the API is running and healthy.

### Response

**Status**: `200 OK`

**Response Body** (JSON):
```json
{
  "status": "healthy",
  "timestamp": "2024-04-07T15:05:30.123456"
}
```

### cURL Example
```bash
curl http://localhost:8000/health
```

---

## 6. OpenAPI Documentation

### Endpoint
```
GET /docs
```

### Purpose
Interactive API documentation (Swagger UI).

### Access
- **URL**: http://localhost:8000/docs
- **Features**: 
  - Try it out functionality
  - Request/response examples
  - Parameter documentation
  - Schema definitions

---

## Error Response Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters or missing file |
| 404 | Not Found | File or resource not found |
| 413 | Payload Too Large | File exceeds size limit |
| 422 | Unprocessable Entity | Invalid request format or validation error |
| 500 | Internal Server Error | Server processing error |
| 503 | Service Unavailable | Server temporarily unavailable |

---

## Rate Limiting (Future)

Currently unlimited. Future versions will include:
- 100 requests per minute per IP
- File size quotas per user
- Concurrent upload limits

---

## Authentication (Future)

Currently unauthenticated. Future versions will include:
- API key authentication
- JWT tokens
- OAuth 2.0 integration

---

## CORS Policy

**Current Configuration**:
```
Access-Control-Allow-Origins: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

**Browser Access**: Enabled from all origins

**Considerations**: 
- Restrict origins in production
- Use API Gateway for CORS management

---

## Common Workflows

### Workflow 1: Complete Analysis & Export
```
1. POST /api/upload/document
   ↓ (returns file_id)
   
2. POST /api/analyze/document
   ↓ (analyze requirements)
   
3. POST /api/generate/test-cases
   ↓ (generate 10 test cases)
   
4. POST /api/export/test-cases
   ↓ (export to Word/Excel)
   
5. Download file
```

### Workflow 2: Multiple Exports
```
1. POST /api/upload/document
   ↓ (returns file_id)
   
2. POST /api/analyze/document
   
3. POST /api/generate/test-cases
   
4. POST /api/export/test-cases (format: docx)
   ↓ Download .docx
   
5. POST /api/export/test-cases (format: xlsx)
   ↓ Download .xlsx
```

### Workflow 3: Filtered Generation
```
1. POST /api/upload/document
   
2. POST /api/analyze/document
   
3. POST /api/generate/test-cases (only positive cases)
   ↓ Set include_negative=false, include_boundary=false
   
4. Review & Export
```

---

## Best Practices

1. **Always upload before analyzing**: File ID required for all subsequent operations
2. **Validate responses**: Check `success` field in response
3. **Handle errors gracefully**: Implement retry logic for network failures
4. **Cache file IDs**: Reuse file IDs for multiple exports
5. **Use appropriate test type filters**: Reduce unnecessary test cases
6. **Monitor file sizes**: Optimize documents before upload
7. **Implement progress tracking**: Show user feedback during operations

---

## Testing Tools

### Postman Collection
- Import JSON collection from `/exports/Postman_Collection.json` (if available)

### Curl Examples
Available in each endpoint section above

### Python Script
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Upload
upload_response = requests.post(
    f"{BASE_URL}/api/upload/document",
    files={'file': open('requirements.pdf', 'rb')}
)
file_id = upload_response.json()['file_id']

# Analyze
analyze_response = requests.post(
    f"{BASE_URL}/api/analyze/document",
    json={'file_id': file_id}
)

# Generate
generate_response = requests.post(
    f"{BASE_URL}/api/generate/test-cases",
    json={
        'file_id': file_id,
        'num_test_cases': 10,
        'include_positive': True,
        'include_negative': True,
        'include_boundary': True
    }
)

# Export
export_response = requests.post(
    f"{BASE_URL}/api/export/test-cases",
    json={
        'file_id': file_id,
        'format': 'docx'
    }
)

with open('TestCases.docx', 'wb') as f:
    f.write(export_response.content)
```

---

**Last Updated**: April 7, 2024
**API Version**: 1.0.0
**Status**: ✅ Production Ready
