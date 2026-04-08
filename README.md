# AI QA Agent - Agentic QA Application

An intelligent AI-powered QA application that automatically generates comprehensive manual test cases from JIRA tickets, SRS documents, and other requirement specifications.

## Overview

The AI QA Agent application streamlines the test case creation process by:
- Accepting document uploads (PDF, DOCX, TXT)
- Parsing documents to extract user stories, acceptance criteria, and business rules
- Using an AI agent (LLM) to intelligently generate structured test cases
- Providing multiple test scenarios: positive, negative, and boundary/edge cases
- Exporting test cases to Word (.docx) or Excel (.xlsx) formats

## Features

✅ **Document Parsing**
- PDF extraction with PyPDF2
- DOCX parsing with python-docx
- Plain text file support
- Structured information extraction (user stories, acceptance criteria, business rules, constraints)

✅ **Intelligent Test Case Generation**
- AI-powered test case generation using LLM
- Mock AI responses for development/testing (no API key required)
- Supports positive, negative, and boundary test scenarios
- Customizable number of test cases (1-20)

✅ **Test Case Management**
- Structured test case models with Pydantic
- Complete test case details: ID, name, description, steps, expected results
- Priority and test type classification

✅ **Export Capabilities**
- Export to Microsoft Word (.docx) with professional formatting
- Export to Excel (.xlsx) with multiple sheets (test cases + steps)
- Maintains document structure and readability

✅ **RESTful API**
- FastAPI-based backend
- Comprehensive API documentation (Swagger UI)
- Error handling and validation
- CORS support for web integration

## Project Structure

```
agentic-qa/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── upload.py                    # Document upload endpoint
│   │   ├── analyze.py                   # Document analysis endpoint
│   │   ├── generate.py                  # Test case generation endpoint
│   │   └── export.py                    # Export endpoint (Word/Excel)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_parser.py           # Document parsing logic
│   │   └── ai_agent.py                  # LLM agent for test case generation
│   ├── models/
│   │   ├── __init__.py
│   │   └── testcase.py                  # Pydantic models for test cases
│   └── utils/
│       ├── __init__.py
│       ├── word_exporter.py             # Word document export
│       └── excel_exporter.py            # Excel document export
├── uploads/                             # Directory for uploaded files
├── exports/                             # Directory for exported documents
├── requirements.txt                     # Python dependencies
├── README.md                            # This file
└── .env                                 # Environment variables (optional)
```

## Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: See `requirements.txt`

## Installation

### 1. Prerequisites

Ensure you have Python 3.10+ installed:

```bash
python --version
```

### 2. Create Virtual Environment

```bash
# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure Environment Variables

Create a `.env` file in the project root:

```env
# LLM Configuration (optional - uses mock if not set)
LLM_API_KEY=your_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Running the Application

### Start the FastAPI Server

```bash
# With auto-reload (development)
uvicorn app.main:app --reload

# Without auto-reload (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Custom host and port
uvicorn app.main:app --host localhost --port 8000
```

The application will be available at: **http://localhost:8000**

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### 1. Upload Document

**Endpoint**: `POST /api/upload/document`

Upload a document (PDF, DOCX, or TXT) for analysis.

**Request**:
```bash
curl -X POST "http://localhost:8000/api/upload/document" \
  -F "file=@/path/to/document.pdf"
```

**Response**:
```json
{
  "success": true,
  "file_id": "20240407_123456_document.pdf",
  "file_name": "document.pdf",
  "file_size": 102400,
  "upload_time": "2024-04-07T12:34:56.789123",
  "message": "File 'document.pdf' uploaded successfully"
}
```

### 2. Analyze Document

**Endpoint**: `POST /api/analyze/document`

Extract structured information from the uploaded document.

**Request**:
```bash
curl -X POST "http://localhost:8000/api/analyze/document" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_document.pdf"
  }'
```

**Response**:
```json
{
  "success": true,
  "file_id": "20240407_123456_document.pdf",
  "analysis": {
    "user_stories": [
      "As a user, I want to login with my credentials"
    ],
    "acceptance_criteria": [
      "Given valid credentials, the user should be logged in"
    ],
    "preconditions": [
      "User must have a registered account"
    ],
    "business_rules": [
      "Password must be at least 8 characters"
    ],
    "constraints": [
      "Login attempts limited to 5 per hour"
    ],
    "document_summary": "System allows users to authenticate..."
  },
  "message": "Document analysis completed successfully"
}
```

### 3. Generate Test Cases

**Endpoint**: `POST /api/generate/test-cases`

Generate manual test cases based on document analysis.

**Request**:
```bash
curl -X POST "http://localhost:8000/api/generate/test-cases" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_document.pdf",
    "num_test_cases": 5,
    "include_positive": true,
    "include_negative": true,
    "include_boundary": true
  }'
```

**Response**:
```json
{
  "success": true,
  "file_id": "20240407_123456_document.pdf",
  "test_cases": [
    {
      "test_case_id": "TC_POS_001",
      "name": "Positive Test Case 1 - Feature Test",
      "description": "Verify successful execution of the feature",
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
        }
      ],
      "expected_result": "Feature operates as expected",
      "test_type": "positive",
      "priority": "high"
    }
  ],
  "total_count": 5,
  "message": "Successfully generated 5 test cases"
}
```

### 4. Export Test Cases

**Endpoint**: `POST /api/export/test-cases`

Export generated test cases to Word or Excel format.

**Request (Word Export)**:
```bash
curl -X POST "http://localhost:8000/api/export/test-cases" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_document.pdf",
    "format": "docx",
    "num_test_cases": 5
  }' \
  -o test_cases.docx
```

**Request (Excel Export)**:
```bash
curl -X POST "http://localhost:8000/api/export/test-cases" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "20240407_123456_document.pdf",
    "format": "xlsx",
    "num_test_cases": 5
  }' \
  -o test_cases.xlsx
```

### 5. Health Check

**Endpoint**: `GET /health`

Check application health status.

```bash
curl http://localhost:8000/health
```

## Complete Workflow Example

### Using PowerShell (Windows)

```powershell
# 1. Upload document
$uploadResponse = curl -X POST "http://localhost:8000/api/upload/document" `
  -F "file=@C:\path\to\requirements.pdf" | ConvertFrom-Json

$fileId = $uploadResponse.file_id
Write-Host "File ID: $fileId"

# 2. Analyze document
$analysisResponse = curl -X POST "http://localhost:8000/api/analyze/document" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`"}" | ConvertFrom-Json

Write-Host "Extracted user stories: $($analysisResponse.analysis.user_stories.Count)"

# 3. Generate test cases
$generateResponse = curl -X POST "http://localhost:8000/api/generate/test-cases" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`", `"num_test_cases`": 10}" | ConvertFrom-Json

Write-Host "Generated test cases: $($generateResponse.total_count)"

# 4. Export to Word
curl -X POST "http://localhost:8000/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`", `"format`": `"docx`"}" `
  -o "TestCases.docx"

Write-Host "Word document exported: TestCases.docx"

# 5. Export to Excel
curl -X POST "http://localhost:8000/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`", `"format`": `"xlsx`"}" `
  -o "TestCases.xlsx"

Write-Host "Excel document exported: TestCases.xlsx"
```

### Using bash (macOS/Linux)

```bash
# 1. Upload document
UPLOAD_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/upload/document" \
  -F "file=@/path/to/requirements.pdf")

FILE_ID=$(echo $UPLOAD_RESPONSE | jq -r '.file_id')
echo "File ID: $FILE_ID"

# 2. Analyze document
curl -s -X POST "http://localhost:8000/api/analyze/document" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\": \"$FILE_ID\"}" | jq '.'

# 3. Generate test cases
curl -s -X POST "http://localhost:8000/api/generate/test-cases" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\": \"$FILE_ID\", \"num_test_cases\": 10}" | jq '.'

# 4. Export to Word
curl -X POST "http://localhost:8000/api/export/test-cases" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\": \"$FILE_ID\", \"format\": \"docx\"}" \
  -o "TestCases.docx"

# 5. Export to Excel
curl -X POST "http://localhost:8000/api/export/test-cases" \
  -H "Content-Type: application/json" \
  -d "{\"file_id\": \"$FILE_ID\", \"format\": \"xlsx\"}" \
  -o "TestCases.xlsx"
```

## Configuration

### Environment Variables

Create a `.env` file to configure the application:

```env
# LLM Configuration
# Set this to your API key to use real LLM integration
# If not set, the application will use mock responses
LLM_API_KEY=sk-your-api-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Document Upload Configuration
MAX_UPLOAD_SIZE=52428800  # 50MB in bytes
UPLOAD_TIMEOUT=300  # seconds
```

### Supported File Types

- **PDF**: `.pdf` - Extracted using PyPDF2
- **Word**: `.docx` - Extracted using python-docx
- **Text**: `.txt` - Plain text files (UTF-8 or Latin-1 encoding)

## Development

### Project Architecture

The application follows a clean, modular architecture:

1. **API Layer** (`app/api/`): RESTful endpoints for client interaction
2. **Service Layer** (`app/services/`): Business logic for document parsing and AI
3. **Model Layer** (`app/models/`): Pydantic models for data validation
4. **Utility Layer** (`app/utils/`): Export functionality for various formats

### Adding New Features

To add new endpoints or functionality:

1. Create a new router in `app/api/`
2. Implement business logic in `app/services/`
3. Define request/response models in `app/models/`
4. Include the router in `app/main.py`

### Code Quality Standards

- **Type Hints**: All functions have type annotations
- **Docstrings**: All modules and functions have docstrings
- **Error Handling**: Comprehensive exception handling with meaningful messages
- **Validation**: Pydantic models for request/response validation

## LLM Integration

### Mock Mode (Default)

By default, the application uses mock AI responses for testing and development. This requires no API key configuration.

### Real LLM Integration

To use a real LLM provider:

1. Set the `LLM_API_KEY` environment variable
2. Update `app/services/ai_agent.py` to implement actual API calls
3. Supported providers can be extended (OpenAI, Anthropic, etc.)

### Example Integration Points

```python
# In app/services/ai_agent.py
def _generate_ai_test_cases(self, analysis, num_cases):
    # Replace with actual API calls
    # response = openai.ChatCompletion.create(...)
    # return self.parse_ai_response(response)
    pass
```

## Testing

The application includes comprehensive error handling and validation. Test files can be uploaded to verify functionality.

### Sample Test Document

Create a `sample_requirements.txt`:

```
User Story: As a user, I want to log in with my email and password

Acceptance Criteria:
- Given I have a valid email and password, when I click login, then I should be redirected to the dashboard
- When I enter an invalid password, then I should see an error message
- When the email field is empty, then the submit button should be disabled

Preconditions:
- User has a registered account
- User is on the login page

Business Rules:
- Password must be at least 8 characters
- Login attempts are limited to 5 per hour
- Session timeout is 30 minutes

Constraints:
- Login must complete within 2 seconds
- System must support 1000 concurrent users
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Port Already in Use

If port 8000 is already in use:

```bash
uvicorn app.main:app --port 8001
```

### File Upload Issues

- Ensure the `uploads/` directory exists and is writable
- Check file size doesn't exceed system limits
- Verify file format is supported (PDF, DOCX, TXT)

### Export File Not Generated

- Ensure the `exports/` directory exists and is writable
- Check that test cases were successfully generated
- Verify enough disk space is available

## Performance Considerations

- **Document Parsing**: Optimized for documents up to 50MB
- **Test Case Generation**: Mock responses are instant; real LLM may take 5-30 seconds
- **Export Generation**: Word export ~500ms, Excel export ~800ms

## Security

- **File Uploads**: Files are stored with timestamp-based unique IDs
- **Input Validation**: All inputs validated with Pydantic
- **Error Messages**: Generic error messages to prevent information leakage
- **CORS**: Configure allowed origins in production

## Future Enhancements

- [ ] Database integration for persistent storage
- [ ] User authentication and authorization
- [ ] Test case templates and customization
- [ ] Integration with JIRA API for automatic ticket parsing
- [ ] Real-time test case refinement
- [ ] Test execution tracking
- [ ] AI model training on custom test cases
- [ ] Support for additional file formats (XML, JSON)
- [ ] Batch document processing
- [ ] Test case version control

## Contributing

Contributions are welcome! Follow these guidelines:

1. Maintain code quality and add type hints
2. Add docstrings to all functions
3. Write clear, descriptive commit messages
4. Test new features thoroughly
5. Update documentation as needed

## License

This project is provided as-is for QA automation purposes.

## Support

For issues, questions, or suggestions:

1. Check the API documentation at `/docs`
2. Review error messages in application logs
3. Ensure all dependencies are correctly installed
4. Verify file formats and uploads are valid

## Version History

### v1.0.0 (Initial Release)
- Document upload and parsing
- Test case generation with AI agent
- Export to Word and Excel
- RESTful API with comprehensive documentation
- Mock AI responses for development

---

**Built with** ❤️ **for QA Automation**

*Last Updated: April 7, 2024*
