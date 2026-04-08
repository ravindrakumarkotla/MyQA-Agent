# AI QA Agent - Troubleshooting & FAQ

## 🔧 Troubleshooting Guide & Frequently Asked Questions

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Server & Runtime Issues](#server--runtime-issues)
3. [File Upload Issues](#file-upload-issues)
4. [API Issues](#api-issues)
5. [Frontend/UI Issues](#frontendui-issues)
6. [Export Issues](#export-issues)
7. [Performance Issues](#performance-issues)
8. [General FAQ](#general-faq)

---

## Installation Issues

### Issue 1: Python Not Found

**Symptom**:
```
'python' is not recognized as an internal or external command
```

**Cause**: Python not installed or not in PATH

**Solution**:

1. **Check Python installation**:
   ```bash
   python --version
   ```

2. **If not installed**, download from [python.org](https://www.python.org/)
   - Ensure "Add Python to PATH" is checked during installation

3. **If Python is installed but not in PATH**:
   - Windows: Add Python directory to System PATH
   - macOS/Linux: Reinstall Python or add to shell profile

4. **Test installation**:
   ```bash
   python --version
   python -m pip --version
   ```

---

### Issue 2: Virtual Environment Creation Fails

**Symptom**:
```
Error: failed to create virtual environment
```

**Cause**: Insufficient permissions or disk space

**Solution**:

1. **Check disk space**:
   ```bash
   # Windows
   wmic logicaldisk get size,freespace
   
   # macOS/Linux
   df -h
   ```

2. **Run as administrator** (Windows):
   - Right-click Command Prompt → Run as Administrator

3. **Try alternative**:
   ```bash
   python -m venv .venv --copies
   ```

---

### Issue 3: pip Install Fails

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement
```

**Cause**: Package doesn't exist, network issue, or version conflict

**Solution**:

1. **Update pip first**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Check package name**:
   ```bash
   pip search fastapi  # or use PyPI.org
   ```

3. **Install specific version**:
   ```bash
   pip install fastapi==0.104.1
   ```

4. **Check network connection**:
   ```bash
   pip install --index-url https://pypi.org/simple/ fastapi
   ```

5. **Install with verbose output**:
   ```bash
   pip install -vv fastapi
   ```

---

### Issue 4: Dependency Conflicts

**Symptom**:
```
ERROR: pip's dependency resolver does not currently take into account all the packages
```

**Cause**: Incompatible package versions

**Solution**:

1. **Use lightweight requirements**:
   ```bash
   pip install -r requirements-lightweight.txt
   ```

2. **Install one by one**:
   ```bash
   pip install fastapi
   pip install uvicorn
   pip install pydantic
   # etc...
   ```

3. **Clear pip cache**:
   ```bash
   pip cache purge
   pip install -r requirements.txt
   ```

---

## Server & Runtime Issues

### Issue 5: Uvicorn Server Won't Start

**Symptom**:
```
ERROR: [Errno 48] Address already in use
```

**Cause**: Port 8000 already in use

**Solution**:

**Windows**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --port 8001
```

**macOS/Linux**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

---

### Issue 6: ImportError When Starting Server

**Symptom**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:

1. **Activate virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   pip list | grep fastapi
   python -c "import fastapi; print(fastapi.__version__)"
   ```

---

### Issue 7: Module Not Found During Import

**Symptom**:
```
ModuleNotFoundError: No module named 'app.services'
```

**Cause**: Not running from correct directory or `__init__.py` missing

**Solution**:

1. **Check current directory**:
   ```bash
   pwd  # macOS/Linux
   cd   # Windows
   ```

2. **Navigate to project root**:
   ```bash
   cd MyQA_Agent/Myqa_agent
   ```

3. **Verify directory structure**:
   ```bash
   ls -la app/          # macOS/Linux
   dir app\             # Windows
   ```

4. **Ensure all `__init__.py` files exist**:
   ```bash
   # Should exist:
   app/__init__.py
   app/api/__init__.py
   app/models/__init__.py
   app/services/__init__.py
   app/utils/__init__.py
   ```

---

### Issue 8: Application Crashes After Startup

**Symptom**:
```
ERROR: Application startup failed. Exiting.
```

**Cause**: Error in app initialization code

**Solution**:

1. **Check console output**:
   - Look for specific error message before "Exiting"
   - Example: "JSONDecodeError" or "FileNotFoundError"

2. **Run with verbose output**:
   ```bash
   uvicorn app.main:app --reload --log-level debug
   ```

3. **Check `app/main.py`**:
   ```python
   # Ensure all imports work
   from fastapi import FastAPI  # Should not error
   from app.api import upload, analyze, generate, export
   ```

4. **Test imports manually**:
   ```bash
   python -c "from app.main import app; print('OK')"
   ```

---

## File Upload Issues

### Issue 9: File Upload Fails with 413 Error

**Symptom**:
```
HTTP 413 Payload Too Large
```

**Cause**: File exceeds 50MB limit

**Solution**:

1. **Check file size**:
   ```bash
   # Windows
   Get-Item requirements.pdf | Select-Object -Property Length
   
   # macOS/Linux
   ls -lh requirements.pdf
   ```

2. **Reduce file size**:
   - Compress file
   - Remove images/attachments
   - Split into multiple files

3. **Increase server limit** (in `app/main.py`):
   ```python
   app = FastAPI(
       max_request_size=100_000_000  # 100MB
   )
   ```

---

### Issue 10: "Unsupported File Format" Error

**Symptom**:
```
400 Bad Request: Unsupported file format
```

**Cause**: File extension not in supported list

**Solution**:

1. **Check supported formats**:
   - PDF (`.pdf`)
   - Word (`.docx`)
   - Text (`.txt`)

2. **Verify file extension**:
   ```bash
   # File should be named like:
   requirements.pdf
   requirements.docx
   requirements.txt
   ```

3. **Check actual file type**:
   ```bash
   # Windows - Check file properties
   # macOS/Linux
   file requirements.pdf
   ```

4. **Convert file if needed**:
   - Use online converters for format conversion
   - Ensure file content matches extension

---

### Issue 11: Upload Succeeds but File Not Found During Analysis

**Symptom**:
```
File not found error during analysis
```

**Cause**: File upload stored in wrong location

**Solution**:

1. **Check uploads directory**:
   ```bash
   ls -la uploads/     # macOS/Linux
   dir uploads\        # Windows
   ```

2. **Verify file exists**:
   ```bash
   ls -la uploads/20240407_150530_requirements.pdf
   ```

3. **Check file permissions**:
   ```bash
   # macOS/Linux
   ls -la uploads/
   ```

4. **Verify file_id from upload response** matches filename

---

### Issue 12: File Upload Progress Stuck

**Symptom**:
```
Upload progress bar stuck at 0%
```

**Cause**: Large file, slow network, or server not accepting data

**Solution**:

1. **Check network**:
   - Test connection speed
   - Try different network
   - Close bandwidth-heavy apps

2. **Increase timeout** (in `public/script.js`):
   ```javascript
   xhr.timeout = 120000; // 2 minutes instead of 30s
   ```

3. **Test with smaller file first**:
   - Try uploading small test file
   - Gradually increase size

4. **Check server logs**:
   - Look for upload processing messages
   - Check for errors in terminal

---

## API Issues

### Issue 13: API Endpoint Returns 404

**Symptom**:
```
404 Not Found: GET /api/analyze/document
```

**Cause**: Endpoint not registered or URL incorrect

**Solution**:

1. **Verify endpoint URL**:
   - Should be: `POST /api/analyze/document`
   - Check method (GET vs POST)

2. **Check router registration** in `app/main.py`:
   ```python
   from app.api import analyze
   app.include_router(analyze.router)
   ```

3. **View available endpoints**:
   ```bash
   curl http://localhost:8000/docs
   # Look for endpoint in Swagger UI
   ```

4. **Check router prefix**:
   ```python
   router = APIRouter(prefix="/api", tags=["analyze"])
   ```

---

### Issue 14: API Returns 422 Unprocessable Entity

**Symptom**:
```
422 Unprocessable Entity
```

**Cause**: Invalid request format or missing fields

**Solution**:

1. **Check request format**:
   - Ensure Content-Type header is correct
   - Verify JSON syntax is valid

2. **Verify required fields**:
   ```json
   // WRONG - missing file_id
   {
     "num_test_cases": 10
   }
   
   // CORRECT
   {
     "file_id": "20240407_150530_requirements",
     "num_test_cases": 10
   }
   ```

3. **Check field types**:
   ```json
   // WRONG - num_test_cases should be integer
   {
     "file_id": "xxx",
     "num_test_cases": "10"
   }
   
   // CORRECT
   {
     "file_id": "xxx",
     "num_test_cases": 10
   }
   ```

4. **Validate in Swagger UI**:
   - Go to http://localhost:8000/docs
   - "Try it out" to see validation errors

---

### Issue 15: Analysis Returns Empty Results

**Symptom**:
```json
{
  "user_stories": [],
  "acceptance_criteria": [],
  "business_rules": [],
  "constraints": []
}
```

**Cause**: Document content not properly parsed or too short

**Solution**:

1. **Verify document content**:
   - Ensure document has actual text
   - Test with sample file from project
   - Check file is not image-only PDF

2. **Check document format**:
   - Verify PDF has extractable text (not scanned)
   - Test with `.txt` file for simpler processing

3. **Increase content parsing**:
   - Add debug logging in `document_parser.py`
   - Print extracted content to verify

---

### Issue 16: API Timeout on Large Files

**Symptom**:
```
TimeoutError: Request timed out after 30 seconds
```

**Cause**: Large file takes too long to process

**Solution**:

1. **Increase timeout** in FastAPI:
   ```python
   # In app/main.py
   import asyncio
   asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
   ```

2. **Use uvicorn timeout**:
   ```bash
   uvicorn app.main:app --timeout-keep-alive 300
   ```

3. **Enable async processing**:
   ```python
   @app.post("/api/generate/test-cases")
   async def generate_test_cases(request: GenerateRequest):
       # Already async
       pass
   ```

---

## Frontend/UI Issues

### Issue 17: Page Doesn't Load (Blank Screen)

**Symptom**:
```
Blank page at http://localhost:8000
```

**Cause**: Static files not served or HTML error

**Solution**:

1. **Check browser console**:
   - Press F12 to open DevTools
   - Check Console tab for JavaScript errors

2. **Check public directory**:
   ```bash
   ls -la public/
   # Should have: index.html, style.css, script.js
   ```

3. **Verify static files mounting** in `app/main.py`:
   ```python
   public_dir = Path(__file__).parent.parent / "public"
   if public_dir.exists():
       app.mount("/ui", StaticFiles(directory=str(public_dir)), name="static")
   ```

4. **Test direct file access**:
   ```bash
   curl http://localhost:8000/ui/style.css
   curl http://localhost:8000/ui/script.js
   ```

---

### Issue 18: CSS Not Loading (Unstyled Page)

**Symptom**:
```
Page loads but no styling applied
```

**Cause**: CSS file not found or not linked

**Solution**:

1. **Check style.css exists**:
   ```bash
   ls -la public/style.css
   ```

2. **Verify CSS link in HTML**:
   ```html
   <!-- In index.html -->
   <link rel="stylesheet" href="/ui/style.css">
   ```

3. **Check browser console** for 404 errors

4. **Clear browser cache**:
   - Ctrl+Shift+Delete (Windows)
   - Cmd+Shift+Delete (macOS)
   - Check "Disable cache" in DevTools

---

### Issue 19: JavaScript Not Working (Forms Unresponsive)

**Symptom**:
```
Buttons don't respond, file upload not working
```

**Cause**: JavaScript file not loaded or syntax error

**Solution**:

1. **Check script.js exists**:
   ```bash
   ls -la public/script.js
   ```

2. **Verify script tag in HTML**:
   ```html
   <!-- End of body in index.html -->
   <script src="/ui/script.js"></script>
   ```

3. **Check browser console** for JavaScript errors:
   - Open DevTools (F12)
   - Look for red error messages

4. **Fix syntax errors**:
   - Check console for line numbers
   - Look for common issues:
     ```javascript
     // Missing comma
     {a: 1 b: 2}  // WRONG
     {a: 1, b: 2} // CORRECT
     
     // Unclosed bracket
     function test() {
       console.log('test')
     // Missing closing }
     ```

---

### Issue 20: File Drag & Drop Not Working

**Symptom**:
```
Dragging file to upload area has no effect
```

**Cause**: Drag & drop event handlers not attached

**Solution**:

1. **Check JavaScript console** for errors

2. **Verify upload area element** in HTML:
   ```html
   <div id="uploadArea" class="upload-area">
     <!-- Content -->
   </div>
   ```

3. **Verify JavaScript initialization** in `script.js`:
   ```javascript
   setupDragAndDrop() {
       const uploadArea = document.getElementById('uploadArea');
       if (!uploadArea) {
           console.error('Upload area not found');
           return;
       }
       // Event listeners...
   }
   ```

4. **Test by clicking upload area**:
   - Should open file browser
   - If not, check HTML button/input structure

---

### Issue 21: API Calls Fail from Frontend (CORS)

**Symptom**:
```
CORS error in browser console:
No 'Access-Control-Allow-Origin' header
```

**Cause**: CORS not configured or restricted origins

**Solution**:

1. **Check CORS configuration** in `app/main.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Allow all for development
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Verify middleware is first**:
   - CORS middleware should be added first
   - Before other middleware and routers

3. **Restart server** after changes:
   ```bash
   # Ctrl+C to stop
   # Then restart
   uvicorn app.main:app --reload
   ```

4. **Test API directly**:
   - Open http://localhost:8000/docs
   - Try endpoint in Swagger UI
   - If works, CORS is likely configured correctly

---

## Export Issues

### Issue 22: Export Button Doesn't Work

**Symptom**:
```
Export button clicked but nothing happens
```

**Cause**: Test cases not loaded or export endpoint fails

**Solution**:

1. **Verify test cases loaded**:
   - Check UI shows test case cards
   - Open browser console to see what data exists

2. **Check export endpoint**:
   ```bash
   curl -X POST http://localhost:8000/api/export/test-cases \
     -H "Content-Type: application/json" \
     -d '{"file_id":"xxx","format":"docx"}'
   ```

3. **Check file_id is valid**:
   - Should be set after successful upload
   - Verify in browser console: `console.log(currentFileId)`

4. **Check format is valid**:
   - Should be "docx" or "xlsx"
   - Case-sensitive

---

### Issue 23: Export File Downloads as "export"

**Symptom**:
```
Downloaded file named "export" instead of "TestCases_20240407.docx"
```

**Cause**: Filename not extracted from response headers

**Solution**:

1. **Check Content-Disposition header** is set in API:
   ```python
   return FileResponse(
       file_path,
       filename=f"TestCases_{timestamp}.docx",
       media_type="application/vnd.openxmlformats..."
   )
   ```

2. **Check JavaScript download code**:
   ```javascript
   const contentDisposition = response.headers.get('content-disposition');
   const filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
   ```

3. **Test in curl**:
   ```bash
   curl -i http://localhost:8000/api/export/test-cases \
     --output test.docx
   # Check headers for Content-Disposition
   ```

---

### Issue 24: Exported File Corrupted

**Symptom**:
```
Cannot open .docx or .xlsx file
Error: "The file format is not supported"
```

**Cause**: File generation failed or incomplete

**Solution**:

1. **Check file size**:
   ```bash
   # File should be > 1KB
   ls -lh TestCases_*.docx
   ```

2. **Verify export function** in utils:
   ```python
   # Check word_exporter.py
   # Check excel_exporter.py
   # Ensure all data is written
   ```

3. **Test export endpoint**:
   ```bash
   curl http://localhost:8000/api/export/test-cases \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"file_id":"xxx","format":"docx"}' \
     --output test.docx \
     -v
   ```

4. **Check for errors** in server logs

---

## Performance Issues

### Issue 25: Application Runs Slowly

**Symptom**:
```
Upload takes long time
Analysis is slow
Export generation takes forever
```

**Cause**: Unoptimized code, large files, or system resource constraints

**Solution**:

1. **Check system resources**:
   ```bash
   # Windows - Task Manager
   # macOS/Linux
   top
   ps aux
   ```

2. **Monitor server**:
   ```bash
   # Add logging
   import time
   start = time.time()
   # ... code ...
   print(f"Took {time.time() - start} seconds")
   ```

3. **Use smaller test files**:
   - Test with 1MB file instead of 50MB
   - Verify performance improves

4. **Enable caching**:
   - Cache parsed files
   - Avoid re-parsing same file

---

### Issue 26: Browser Becomes Unresponsive

**Symptom**:
```
Page freezes, not responding to input
```

**Cause**: Heavy JavaScript processing or infinite loop

**Solution**:

1. **Check for infinite loops** in `script.js`:
   ```javascript
   // WRONG - infinite loop
   while (true) {
       process_data();
   }
   
   // CORRECT - define termination
   while (data.length > 0) {
       data = process_data(data);
   }
   ```

2. **Avoid blocking operations**:
   ```javascript
   // WRONG - blocks UI
   while (processNext()) {}
   
   // CORRECT - async
   async function processAll() {
       while (processNext()) {
           await new Promise(r => setTimeout(r, 0)); // Yield to browser
       }
   }
   ```

3. **Use Web Workers** for heavy processing:
   ```javascript
   const worker = new Worker('worker.js');
   worker.postMessage(largeData);
   worker.onmessage = (e) => {
       displayResult(e.data);
   };
   ```

---

## General FAQ

### Q: How do I reset the application?

**A**: 
```bash
# Clear uploads
rm -rf uploads/*

# Clear exports
rm -rf exports/*

# Stop and restart server
# Ctrl+C to stop
uvicorn app.main:app --reload
```

---

### Q: Can I run multiple instances?

**A**:
```bash
# Use different ports
uvicorn app.main:app --port 8001
uvicorn app.main:app --port 8002

# Use load balancer for production
# nginx, HAProxy, or cloud provider load balancers
```

---

### Q: How do I modify the test generation?

**A**: Edit `app/services/ai_agent.py` to customize test case generation logic

---

### Q: Can I add custom file formats?

**A**: Yes, add new parser in `app/services/document_parser.py`

---

### Q: How do I secure the API?

**A**: 
1. Add authentication (JWT, OAuth)
2. Implement rate limiting
3. Add input validation
4. Use HTTPS in production
5. Set up firewall rules

---

### Q: Can I run this on Windows/macOS/Linux?

**A**: Yes, the application is cross-platform. Follow the setup guide for your OS.

---

### Q: How do I get logs?

**A**:
```bash
# Run with debug logging
uvicorn app.main:app --log-level debug

# Enable file logging
# Edit app/config/logging.py
```

---

### Q: How do I update dependencies?

**A**:
```bash
pip list --outdated
pip install --upgrade <package-name>
pip freeze > requirements.txt
```

---

### Q: What if the server crashes?

**A**:
```bash
# Check error in terminal
# Fix the issue
# Restart server
uvicorn app.main:app --reload
```

---

### Q: How do I debug JavaScript?

**A**:
1. Press F12 to open DevTools
2. Go to Console tab
3. Go to Sources tab to set breakpoints
4. Use `debugger;` statement in code

---

### Q: How do I debug Python?

**A**:
```python
# Add print statements
print(f"Debug: {variable}")

# Use pdb debugger
import pdb
pdb.set_trace()

# Use logging module
import logging
logging.debug("Message")
```

---

### Q: Where are uploaded files stored?

**A**: In the `uploads/` directory with timestamp-based names

---

### Q: Where are exported files saved?

**A**: In the `exports/` directory with timestamp-based names

---

### Q: Can I customize the UI?

**A**: Yes, edit `public/index.html`, `public/style.css`, and `public/script.js`

---

### Q: How do I change the API port?

**A**:
```bash
uvicorn app.main:app --port 9000
```

---

### Q: Can I use this with a real LLM?

**A**: Yes, integrate OpenAI, Claude, or other APIs in `app/services/ai_agent.py`

---

### Q: How do I handle large files?

**A**:
1. Increase MAX_FILE_SIZE in configuration
2. Use streaming for parsing
3. Process in chunks
4. Consider async processing

---

### Q: What are the system requirements?

**A**:
- Python 3.9+
- 2GB RAM minimum
- 500MB disk space
- 8Mbps internet connection

---

### Q: How do I contribute code?

**A**:
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request
5. Follow code style guide

---

**Last Updated**: April 7, 2024
**Version**: 1.0.0
**Status**: ✅ Comprehensive Guide Available
