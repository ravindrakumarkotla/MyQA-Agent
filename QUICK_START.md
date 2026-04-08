# 🚀 AI QA Agent - Quick Start Guide

## ✅ Current Status

Your **AI QA Agent** application is **fully operational** with a professional web-based UI!

---

## 📍 Access Points

### Web UI (Interactive Dashboard)
```
🌐 http://localhost:8000
🌐 http://localhost:8000/ui/index.html
```

### API Documentation
```
📚 Swagger UI: http://localhost:8000/docs
📚 ReDoc: http://localhost:8000/redoc
```

### Health Check
```
❤️ Status: http://localhost:8000/health
```

---

## 🎬 Getting Started in 5 Minutes

### 1️⃣ Open the UI
```
Open browser → http://localhost:8000
```

### 2️⃣ Upload a Document
- Click the upload area or drag a file
- Use `sample_requirements.txt` from the project folder
- Supported formats: PDF, DOCX, TXT

### 3️⃣ Analyze the Document
- Click **"Analyze Document"** button
- Wait for analysis to complete
- Review extracted requirements

### 4️⃣ Generate Test Cases
- Select number of test cases (10 recommended)
- Keep all test types checked (Positive, Negative, Boundary)
- Click **"Generate Test Cases"**

### 5️⃣ Export Results
- Click **"Word"** or **"Excel"** to export
- File automatically downloads
- Use for your test execution

---

## 📁 Project Structure

```
MyQA_Agent/
├── app/
│   ├── main.py                 # FastAPI backend
│   ├── api/                    # REST endpoints
│   ├── services/               # Business logic
│   ├── models/                 # Data models
│   └── utils/                  # Export utilities
├── public/                     # Web UI
│   ├── index.html             # Main page
│   ├── style.css              # Styling
│   ├── script.js              # Functionality
├── uploads/                    # Uploaded files
├── exports/                    # Generated exports
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── UI_GUIDE.md                # UI Documentation
└── sample_requirements.txt     # Sample file
```

---

## 🛠️ Installation Status

✅ All dependencies installed:
- FastAPI
- Uvicorn
- Pydantic
- PyPDF2
- python-docx
- openpyxl
- python-multipart

✅ Backend running on `http://127.0.0.1:8000`
✅ Static UI files served from `/public/`
✅ CORS enabled for API access

---

## 🎨 UI Features

### Upload Section
- ✅ Drag & drop support
- ✅ File validation
- ✅ Progress bar
- ✅ File information display

### Analysis Section
- ✅ User stories extraction
- ✅ Acceptance criteria
- ✅ Business rules
- ✅ Constraints identification

### Test Generation
- ✅ Configurable count (5-20)
- ✅ Multiple test types
- ✅ Filter options
- ✅ Priority levels

### Export Options
- ✅ Word (.docx) with formatting
- ✅ Excel (.xlsx) with sheets
- ✅ Timestamp in filename
- ✅ Auto-download

---

## 📊 Supported File Types

| Format | Extension | Max Size |
|--------|-----------|----------|
| PDF | .pdf | 50 MB |
| Word | .docx | 50 MB |
| Text | .txt | 50 MB |

---

## 🔄 API Endpoints

### Upload
```
POST /api/upload/document
Content-Type: multipart/form-data
Response: { file_id, file_name, file_size, upload_time }
```

### Analyze
```
POST /api/analyze/document
Body: { "file_id": "..." }
Response: { analysis: { user_stories, acceptance_criteria, ... } }
```

### Generate
```
POST /api/generate/test-cases
Body: { 
    "file_id": "...",
    "num_test_cases": 10,
    "include_positive": true,
    "include_negative": true,
    "include_boundary": true
}
Response: { test_cases: [...], total_count: 10 }
```

### Export
```
POST /api/export/test-cases
Body: { 
    "file_id": "...",
    "format": "docx" or "xlsx",
    "num_test_cases": 10
}
Response: Binary file (Word/Excel)
```

---

## 💡 Pro Tips

### Best Practices
1. **Organize Requirements**: Use clear, structured format
2. **Use Standard Terms**: Help AI understand better
3. **Include Examples**: Provide context for test generation
4. **Start Small**: Generate 5 cases first, then increase
5. **Review Results**: Always review generated cases

### Performance Optimization
1. Keep documents under 10MB
2. Use plain text or DOCX (faster than PDF)
3. One module/feature per document
4. Use Firefox/Chrome for best performance

### Workflow Optimization
1. Prepare template documents
2. Use batch processing if available
3. Export to Excel for team collaboration
4. Keep files organized by date/module

---

## 🐛 Troubleshooting

### Backend not running?
```powershell
cd C:\Users\ravikotl\MyQA_Agent\Myqa_agent
.venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### UI not loading?
1. Check if backend is running
2. Verify URL: `http://localhost:8000`
3. Check browser console (F12) for errors
4. Clear browser cache (Ctrl+Shift+Delete)

### File upload failing?
1. Check file format (PDF/DOCX/TXT)
2. Verify file size < 50MB
3. Try refresh and retry
4. Check backend logs

### Test cases not generating?
1. Verify document was analyzed first
2. Select at least one test case type
3. Increase number of test cases
4. Check browser console for errors

### Export not working?
1. Verify test cases were generated
2. Check browser download settings
3. Allow pop-ups if needed
4. Try different format (Word vs Excel)

---

## 📚 Documentation Files

1. **README.md** - Project overview
2. **SETUP_GUIDE.md** - Installation instructions
3. **API_TESTING_GUIDE.md** - API usage examples
4. **UI_GUIDE.md** - UI documentation
5. **PROJECT_SUMMARY.md** - Quick reference

---

## 🎯 Next Steps

### Immediate Actions
- [ ] Open `http://localhost:8000` in browser
- [ ] Upload `sample_requirements.txt`
- [ ] Generate test cases
- [ ] Export to Word and Excel
- [ ] Review generated files

### Short Term
- [ ] Integrate with your test management tool
- [ ] Create document templates
- [ ] Standardize requirements format
- [ ] Train team on using the system

### Medium Term
- [ ] Set up scheduled generation
- [ ] Create custom LLM integration
- [ ] Build CI/CD pipeline integration
- [ ] Deploy to production server

### Long Term
- [ ] Multi-user deployment
- [ ] Test execution tracking
- [ ] Analytics dashboard
- [ ] Advanced filtering and search

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Web UI | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Sample File | /sample_requirements.txt |
| UI Guide | UI_GUIDE.md |
| API Guide | API_TESTING_GUIDE.md |

---

## 📞 Support Resources

### Debugging
1. **Browser Console**: F12 → Console tab (shows JS errors)
2. **Network Tab**: F12 → Network tab (shows API calls)
3. **Terminal Output**: Check backend logs
4. **Log Files**: Check for error messages

### Documentation
1. README.md - Comprehensive overview
2. API_TESTING_GUIDE.md - API examples
3. UI_GUIDE.md - UI features
4. Code comments - Implementation details

---

## ✨ System Features Summary

✅ **Multi-format Support**: PDF, DOCX, TXT
✅ **AI Test Generation**: Positive, Negative, Boundary
✅ **Smart Analysis**: Extract key requirements
✅ **Professional Export**: Word, Excel
✅ **Responsive UI**: Desktop, Tablet, Mobile
✅ **RESTful API**: Well-documented
✅ **Real-time Feedback**: Status messages
✅ **Error Handling**: Comprehensive validation
✅ **CORS Enabled**: Cross-origin requests
✅ **Scalable**: Easy to extend

---

## 🎉 Success!

Your AI QA Agent is ready to use!

**Start generating professional test cases in seconds!**

---

*Last Updated: April 7, 2024*
*Version: 1.0.0*
*Status: ✅ Production Ready*
