# AI QA Agent - Architecture & System Design

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      Web UI (index.html)                         │  │
│  │  ┌────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │  │
│  │  │  Upload Area   │  │  Analysis Panel  │  │  Test Case Mgmt │  │  │
│  │  │  - Drop zone   │  │  - User stories  │  │  - Card display │  │  │
│  │  │  - Progress    │  │  - Criteria      │  │  - Filtering    │  │  │
│  │  │  - Validation  │  │  - Rules         │  │  - Export BTNs  │  │  │
│  │  └────────────────┘  └──────────────────┘  └─────────────────┘  │  │
│  │         ↓                    ↓                      ↓              │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │            JavaScript (script.js)                        │    │  │
│  │  │  - Event handlers                                       │    │  │
│  │  │  - API communication                                    │    │  │
│  │  │  - DOM manipulation                                     │    │  │
│  │  │  - File handling                                        │    │  │
│  │  └──────────────────────────────────────────────────────────┘    │  │
│  │                          ↓                                        │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │              CSS (Bootstrap + Custom)                    │    │  │
│  │  │  - Responsive layout                                     │    │  │
│  │  │  - Animations & transitions                             │    │  │
│  │  │  - Dark/Light theme support                            │    │  │
│  │  └──────────────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              ↓ HTTP/REST API                           │
└─────────────────────────────────────────────────────────────────────────┘
                             http://localhost:8000
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND                                 │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     main.py (FastAPI App)                       │  │
│  │  - CORS Middleware                                             │  │
│  │  - Static file serving (/ui)                                   │  │
│  │  - Error handlers                                              │  │
│  │  - Route registration                                          │  │
│  └────────────┬─────────────────────────────┬──────────────────────┘  │
│               ↓                             ↓                         │
│  ┌────────────────────────────┐  ┌──────────────────────────────┐    │
│  │    API ROUTERS (api/)       │  │  STATIC FILES (public/)      │    │
│  │                            │  │                             │    │
│  │  ├─ upload.py             │  │  ├─ index.html             │    │
│  │  │  └─ POST /upload/doc   │  │  ├─ style.css              │    │
│  │  │                        │  │  └─ script.js              │    │
│  │  ├─ analyze.py            │  │                             │    │
│  │  │  └─ POST /analyze/doc  │  │  Served as:                │    │
│  │  │                        │  │  /ui/index.html            │    │
│  │  ├─ generate.py           │  │  /ui/style.css             │    │
│  │  │  └─ POST /generate/tc  │  │  /ui/script.js             │    │
│  │  │                        │  │                             │    │
│  │  └─ export.py             │  │                             │    │
│  │     └─ POST /export/tc    │  │                             │    │
│  └────────┬───────────────────┘  └──────────────────────────────┘    │
│           ↓                                                           │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │            SERVICES LAYER (services/)                        │    │
│  │                                                              │    │
│  │  ┌──────────────────────┐        ┌──────────────────────┐   │    │
│  │  │ document_parser.py   │        │   ai_agent.py        │   │    │
│  │  │                      │        │                      │   │    │
│  │  │ - parse_pdf()        │        │ - generate_test_case │   │    │
│  │  │ - parse_docx()       │        │ - mock_generation    │   │    │
│  │  │ - parse_txt()        │        │ - llm_fallback       │   │    │
│  │  │ - analyze_content()  │        │                      │   │    │
│  │  └──────────────────────┘        └──────────────────────┘   │    │
│  └──────────────────────────────────────────────────────────────┘    │
│           ↓                                                           │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │            MODELS LAYER (models/)                            │    │
│  │                                                              │    │
│  │  - TestStep (Pydantic)                                      │    │
│  │  - TestCase (Pydantic)                                      │    │
│  │  - TestCaseCollection (Pydantic)                            │    │
│  │  - DocumentAnalysis (Pydantic)                              │    │
│  │  - Upload/Analyze/Generate/Export Request models            │    │
│  └──────────────────────────────────────────────────────────────┘    │
│           ↓                                                           │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │            UTILS LAYER (utils/)                              │    │
│  │                                                              │    │
│  │  ├─ word_exporter.py                                        │    │
│  │  │  └─ Export to .docx with formatting                     │    │
│  │  │     (tables, borders, styles)                            │    │
│  │  │                                                           │    │
│  │  └─ excel_exporter.py                                       │    │
│  │     └─ Export to .xlsx with sheets                         │    │
│  │        (Test Cases, Steps, Metadata)                        │    │
│  └──────────────────────────────────────────────────────────────┘    │
│           ↓                                                           │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │            FILE SYSTEM                                       │    │
│  │                                                              │    │
│  │  ├─ uploads/          (temporary uploaded files)            │    │
│  │  ├─ exports/          (generated Word/Excel files)          │    │
│  │  └─ public/           (static web UI files)                 │    │
│  └──────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
1. UPLOAD FLOW:
   ┌──────────┐
   │  User    │
   └────┬─────┘
        │ Click/Drag file
        ↓
   ┌──────────────┐      ┌──────────────┐
   │ Browser JS   │─────→│ API Upload   │
   └──────────────┘      └──────┬───────┘
                                 │
                        ┌────────┴────────┐
                        │                 │
                    Validate         Save file
                        │                 │
                        ↓                 ↓
                    ┌────────────────────────┐
                    │ /uploads/timestamp_*   │
                    └────────────────────────┘


2. ANALYSIS FLOW:
   ┌──────────────┐
   │  file_id     │
   └──────┬───────┘
          │
          ↓
   ┌──────────────────┐
   │ DocumentParser   │
   │ - Read file      │
   │ - Extract text   │
   └──────┬───────────┘
          │
          ↓
   ┌──────────────────────────────────────┐
   │ analyze_content()                    │
   │ - Extract user stories               │
   │ - Find acceptance criteria           │
   │ - Identify business rules            │
   │ - Extract constraints                │
   └──────────┬───────────────────────────┘
              │
              ↓
   ┌──────────────────────────────────────┐
   │ DocumentAnalysis (Pydantic Model)    │
   │ - Validated & structured data        │
   └──────────────────────────────────────┘


3. GENERATION FLOW:
   ┌──────────────────────────────────────┐
   │ GenerationRequest                    │
   │ - file_id                            │
   │ - num_test_cases                     │
   │ - include_positive/negative/boundary │
   └──────────┬───────────────────────────┘
              │
              ↓
   ┌──────────────────────────────────────┐
   │ AIAgent                              │
   │ Check: LLM_API_KEY configured?       │
   └──────────┬───────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
 YES│               NO  │
    ↓                   ↓
┌────────────────┐  ┌────────────────────────────┐
│ Real LLM       │  │ Mock Generation            │
│ (Future)       │  │ - Generate positive cases  │
│                │  │ - Generate negative cases  │
└────┬───────────┘  │ - Generate boundary cases  │
     │              └────────┬───────────────────┘
     │                       │
     └───────────┬───────────┘
                 │
                 ↓
        ┌──────────────────────┐
        │ List[TestCase]       │
        │ (Pydantic models)    │
        └──────────────────────┘


4. EXPORT FLOW:
   ┌──────────────────────────────────────┐
   │ ExportRequest                        │
   │ - file_id                            │
   │ - format (docx/xlsx)                 │
   │ - num_test_cases                     │
   └──────────┬───────────────────────────┘
              │
    ┌─────────┴─────────────────────┐
    │                               │
 docx│                           xlsx│
    ↓                               ↓
┌─────────────────┐       ┌─────────────────────┐
│ WordExporter    │       │ ExcelExporter       │
│ - Format cells  │       │ - Multiple sheets   │
│ - Add tables    │       │ - Styling/colors    │
│ - Page breaks   │       │ - Data validation   │
└────────┬────────┘       └────────┬────────────┘
         │                         │
         ↓                         ↓
     ┌──────────┐         ┌──────────────┐
     │ .docx    │         │ .xlsx        │
     │ Binary   │         │ Binary       │
     └──────────┘         └──────────────┘
         │                     │
         └──────────┬──────────┘
                    │
                    ↓
         ┌──────────────────┐
         │ Browser Download │
         │ Auto filename    │
         │ with timestamp   │
         └──────────────────┘
```

---

## 🔀 Request/Response Flow

```
CLIENT REQUEST                      SERVER RESPONSE
═══════════════════════════════════════════════════════════════════

POST /api/upload/document           200 OK
├─ multipart/form-data              ├─ file_id
├─ file: <binary>                   ├─ file_name
                                    ├─ file_size
                                    ├─ upload_time
                                    └─ success: true

POST /api/analyze/document          200 OK
├─ Content-Type: application/json   ├─ file_id
├─ {"file_id": "xxx"}               ├─ analysis:
                                    │  ├─ user_stories
                                    │  ├─ acceptance_criteria
                                    │  ├─ business_rules
                                    │  ├─ constraints
                                    │  └─ document_summary
                                    └─ success: true

POST /api/generate/test-cases       200 OK
├─ Content-Type: application/json   ├─ file_id
├─ {                                ├─ test_cases: [{
│  "file_id": "xxx",                │  "test_case_id": "...",
│  "num_test_cases": 10,            │  "name": "...",
│  "include_positive": true,        │  "test_steps": [...],
│  "include_negative": true,        │  "expected_result": "...",
│  "include_boundary": true         │  "priority": "high"
│ }                                 │ }]
                                    ├─ total_count: 10
                                    └─ success: true

POST /api/export/test-cases         200 OK
├─ Content-Type: application/json   ├─ Content-Type:
├─ {                                │  application/vnd.openxml
│  "file_id": "xxx",                │  formats-officedocument
│  "format": "docx",                │  .wordprocessingml.document
│  "num_test_cases": 10             │
│ }                                 ├─ Content-Disposition:
                                    │  attachment;filename="..."
                                    │
                                    └─ Binary file content
```

---

## 🗂️ Directory Structure

```
MyQA_Agent/
│
├── 📄 Main Files
│   ├── README.md                  (Project overview)
│   ├── SETUP_GUIDE.md             (Installation)
│   ├── API_TESTING_GUIDE.md       (API examples)
│   ├── UI_GUIDE.md                (UI documentation)
│   ├── QUICK_START.md             (Quick reference)
│   ├── PROJECT_SUMMARY.md         (Project overview)
│   ├── requirements.txt           (Dependencies)
│   └── requirements-lightweight.txt (Flexible versions)
│
├── 📁 app/
│   ├── __init__.py
│   ├── main.py                    (FastAPI app, static serving)
│   │
│   ├── 📁 api/                    (REST Endpoints)
│   │   ├── __init__.py
│   │   ├── upload.py              (File upload)
│   │   ├── analyze.py             (Document analysis)
│   │   ├── generate.py            (Test generation)
│   │   └── export.py              (Export to Word/Excel)
│   │
│   ├── 📁 services/               (Business Logic)
│   │   ├── __init__.py
│   │   ├── document_parser.py     (PDF/DOCX/TXT parsing)
│   │   └── ai_agent.py            (Test case generation)
│   │
│   ├── 📁 models/                 (Data Models)
│   │   ├── __init__.py
│   │   └── testcase.py            (Pydantic models)
│   │
│   └── 📁 utils/                  (Utilities)
│       ├── __init__.py
│       ├── word_exporter.py       (Word export)
│       └── excel_exporter.py      (Excel export)
│
├── 📁 public/                     (Web UI - Static Files)
│   ├── index.html                 (Main page)
│   ├── style.css                  (Styling)
│   └── script.js                  (Functionality)
│
├── 📁 uploads/                    (Temporary uploaded files)
│   └── [timestamp]_filename.*
│
├── 📁 exports/                    (Generated files)
│   └── TestCases_[timestamp].{docx,xlsx}
│
├── 📁 .venv/                      (Python virtual environment)
│   ├── Scripts/
│   ├── Lib/
│   └── pyvenv.cfg
│
├── .env.example                   (Environment template)
├── .gitignore                     (Git ignore rules)
└── example_workflow.py            (Example usage)
```

---

## 🔗 Technology Stack

### Frontend (Browser)
- **HTML5**: Semantic markup, accessibility
- **CSS3**: Modern styling, animations
- **JavaScript (ES6+)**: Dynamic interactions
- **Bootstrap 5**: Responsive grid, components
- **Font Awesome 6**: Icon library
- **Fetch API**: REST API calls

### Backend (Server)
- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation, type hints
- **python-multipart**: Form data handling
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file handling
- **openpyxl**: Excel file generation
- **CORS**: Cross-origin resource sharing

### Database
- **File System**: Document and export storage
- **Memory**: Temporary cache during processing

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────┐
│           CLIENT REQUEST                        │
└────────────────┬────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
    Frontend        Input Validation
    Validation      (size, type, format)
         │                │
         └───────┬────────┘
                 │
         ┌───────┴─────────┐
         │                 │
    CORS Check      Rate Limiting
    (allowed         (future)
     origins)
         │                 │
         └───────┬─────────┘
                 │
          ┌──────┴──────┐
          │             │
    Authorization   File Security
    (if needed)      (temp storage)
          │             │
          └──────┬──────┘
                 │
         ┌───────┴──────────┐
         │                  │
    Pydantic         Error Handling
    Validation       (no stack traces)
         │                  │
         └───────┬──────────┘
                 │
         ┌───────┴─────────────┐
         │                     │
    Process        Response     │
    Sanitization   Validation   │
         │                     │
         └───────┬─────────────┘
                 │
          ┌──────┴──────┐
          │             │
       Encrypt       Log
       (future)      Access
          │             │
          └──────┬──────┘
                 │
        ┌────────┴─────────┐
        │                  │
    Send to        Return Status
    Client
```

---

## ⚡ Performance Optimization

```
OPTIMIZATION LAYER:
├─ Frontend
│  ├─ Minimized CSS/JS
│  ├─ CDN for Bootstrap/FontAwesome
│  ├─ Responsive images
│  └─ Local caching
│
├─ Backend
│  ├─ Async processing
│  ├─ Efficient parsing
│  ├─ Connection pooling
│  └─ Error handling
│
└─ Network
   ├─ Compression
   ├─ Caching headers
   ├─ HTTP/1.1 keep-alive
   └─ GZIP compression
```

---

## 📈 Scalability Considerations

### Current (Single Server)
- Single FastAPI instance
- File system storage
- Memory-based processing
- Suitable for: 10-50 concurrent users

### Future (Scalable)
- Load balancer
- Multiple FastAPI instances
- Distributed storage (S3/Cloud)
- Message queue (Redis/RabbitMQ)
- Caching layer
- Database backend
- Suitable for: 1000+ concurrent users

---

**Last Updated**: April 7, 2024
**Version**: 1.0.0
**Status**: ✅ Production Ready
