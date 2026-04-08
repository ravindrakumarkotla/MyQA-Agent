# AI QA Agent - Web UI Documentation

## 🎯 Quick Start

### Access the UI
Your AI QA Agent web interface is now running and accessible at:

```
http://localhost:8000/
http://localhost:8000/ui/index.html
```

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- FastAPI backend running on `http://localhost:8000`
- Internet connection (for CDN resources: Bootstrap, Font Awesome)

---

## 📱 User Interface Overview

### Layout
The web interface is divided into two main sections:

#### **Left Sidebar (25% width)**
- **Upload Document**: Drag-and-drop or click to upload files
- **Document Analysis**: View extracted requirements, user stories, and acceptance criteria

#### **Main Content Area (75% width)**
- **Generation Settings**: Configure test case type and count
- **Test Cases Display**: View, filter, and export generated test cases

### Navigation
- **Top Navigation Bar**: Shows app branding and version
- **Alert Messages**: Contextual feedback for user actions
- **Footer**: Application information and version

---

## 🚀 Workflow

### Step 1: Upload Document
1. Click on the upload area or drag a file
2. Supported formats: **PDF, DOCX, TXT**
3. Maximum file size: **50 MB**

```
✓ Feedback: "File uploaded successfully!"
✓ File information displayed (name, size, ID)
✓ "Analyze Document" button enabled
```

### Step 2: Analyze Document
1. Click **"Analyze Document"** button
2. System extracts:
   - User Stories
   - Acceptance Criteria
   - Business Rules
   - Constraints
   - Preconditions

```
✓ Feedback: "Document analyzed successfully!"
✓ Analysis results displayed in sidebar
✓ "Generate Test Cases" button enabled
```

### Step 3: Configure Generation
1. Select **Number of Test Cases** (5-20)
2. Choose **Test Case Types**:
   - ✅ **Positive**: Valid inputs/scenarios
   - ⚠️ **Negative**: Invalid inputs/edge cases
   - 🔲 **Boundary**: Boundary value analysis

### Step 4: Generate Test Cases
1. Click **"Generate Test Cases"** button
2. System creates test cases with:
   - Test Case ID
   - Name & Description
   - Pre-conditions
   - Step-by-step instructions
   - Expected results
   - Priority level

```
✓ Feedback: "Successfully generated X test cases!"
✓ Test cases displayed with visual indicators
✓ Export buttons enabled
```

### Step 5: Export Results
1. Click **Word** or **Excel** button
2. Select export format:
   - 📄 **Word (.docx)**: Professional formatted document
   - 📊 **Excel (.xlsx)**: Spreadsheet with multiple sheets

```
✓ File automatically downloads with timestamp
✓ Feedback: "Successfully exported to [FORMAT]!"
```

---

## 🎨 UI Components

### Upload Area
- **Visual Feedback**: Color change on hover/drag
- **Progress Bar**: Real-time upload progress
- **File Information**: Displays after successful upload

### Test Case Cards
Each test case displays:

```
┌─ Test Case Card ─────────────────────────────────┐
│ TC_POS_001    [Positive Test Case]               │
│                                                   │
│ Test Name: Feature registration validation       │
│ Description: Verify successful account creation  │
│                                                   │
│ Pre-condition: User on registration page         │
│                                                   │
│ Steps:                                           │
│  ① Fill email field with valid email             │
│  ② Fill password field with strong password     │
│  ③ Click submit button                          │
│                                                   │
│ Expected Result: Account created successfully   │
│ Priority: High   Type: Positive                 │
└──────────────────────────────────────────────────┘
```

### Color Coding

| Element | Color | Meaning |
|---------|-------|---------|
| Test Case Border | Green | Positive scenario |
| Test Case Border | Orange | Negative scenario |
| Test Case Border | Red | Boundary scenario |
| Priority Badge | Red | High priority |
| Priority Badge | Orange | Medium priority |
| Priority Badge | Green | Low priority |

### Alert Messages

| Type | Icon | Meaning |
|------|------|---------|
| ✅ Success | Green checkmark | Operation successful |
| ❌ Danger | Red X mark | Operation failed |
| ⚠️ Warning | Yellow triangle | Warning or validation issue |
| ℹ️ Info | Blue circle | Information message |

---

## 🔄 Features

### Drag & Drop Upload
- Click upload area or drag files
- Visual feedback during drag
- Progress bar during upload

### Real-time Analysis
- Quick document parsing
- Structured information extraction
- Immediate feedback

### Smart Test Generation
- Filter by test type
- Customize test case count
- AI-powered test scenarios

### Professional Export
- Word documents with tables and formatting
- Excel spreadsheets with multiple sheets
- Timestamped filenames

### Responsive Design
- **Desktop**: Full layout (1200px+)
- **Tablet**: Optimized for 768px-1199px
- **Mobile**: Single column, touch-friendly

---

## 📱 Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Mobile | < 576px | Single column, stacked |
| Tablet | 576px - 767px | 1 column |
| Small Desktop | 768px - 991px | 2 columns |
| Desktop | 992px+ | Full 2-column layout |

---

## 🛠️ Technical Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Dynamic interactions
- **Bootstrap 5**: Responsive grid system
- **Font Awesome 6**: Icon library

### Backend
- **FastAPI**: RESTful API
- **Pydantic**: Data validation
- **CORS**: Cross-origin resource sharing
- **Static Files**: UI serving

### APIs Used (Frontend → Backend)
- `POST /api/upload/document`: File upload
- `POST /api/analyze/document`: Document analysis
- `POST /api/generate/test-cases`: Test case generation
- `POST /api/export/test-cases`: Export to Word/Excel

---

## ⚡ Performance Tips

### Optimization
- CSS and JS are inline for better performance
- Bootstrap CDN cached by browser
- Font Awesome icons loaded from CDN
- Responsive images (no bloat on mobile)

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 🔐 Security

### Client-Side
- File type validation before upload
- File size checking (50MB max)
- XSS protection through proper escaping
- CORS configuration

### Server-Side
- File upload validation
- Request size limits
- Pydantic input validation
- Error handling and logging

---

## 🐛 Troubleshooting

### Issue: UI not loading
**Solution**: Ensure backend is running on `http://localhost:8000`

### Issue: File upload fails
**Solution**: Check file format (PDF/DOCX/TXT) and size (<50MB)

### Issue: Test cases not generating
**Solution**: 
- Verify document was analyzed
- Select at least one test case type
- Check backend logs

### Issue: Export not working
**Solution**: Check browser permissions for downloads

### Issue: API calls failing
**Solution**: Verify CORS is enabled and backend is accessible

---

## 🎓 User Guide

### For QA Managers
1. Upload requirement documents
2. Review extracted analysis
3. Adjust test case configuration
4. Export professional reports
5. Distribute to test team

### For Test Engineers
1. Review generated test cases
2. Customize as needed
3. Add manual tests if required
4. Execute using test management tool
5. Track results

### For Developers
1. Check generated test cases
2. Verify coverage
3. Identify edge cases
4. Implement fixes
5. Re-run test generation

---

## 📊 Example Workflow

### Scenario: E-Commerce Registration Module

**Input**: Requirements document (DOCX)

**Output**: 
- 10 test cases (positive, negative, boundary)
- Professional Word/Excel reports
- Organized by test type and priority

**Typical Time**: 30 seconds - 2 minutes

---

## 🔗 Related Resources

- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Backend Source**: `/app/main.py`
- **Frontend Source**: `/public/`
- **Configuration**: `.env.example`

---

## 📞 Support

### Getting Help
1. Check troubleshooting section
2. Review backend logs: `console output`
3. Verify file format and size
4. Check browser console (F12)

### Common Issues Database
See API_TESTING_GUIDE.md for API error responses

---

## 🚀 Advanced Features (Future)

- 🔄 Batch processing multiple documents
- 📈 Test coverage analytics
- 🤖 AI-powered test case refinement
- 📝 Custom test templates
- 🔗 Integration with test management tools
- 📊 Test execution tracking
- 👥 Multi-user collaboration

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-04-07 | Initial release |

---

## 💡 Tips & Tricks

### Speed Up Workflow
1. Use keyboard shortcuts (Ctrl+S to analyze)
2. Pre-format your requirements document
3. Use consistent document structure
4. Create templates for common scenarios

### Best Practices
1. Review analysis before generation
2. Start with 5 test cases, increase as needed
3. Use all three test case types
4. Export regularly as backup
5. Keep generated files organized

### Quality Improvements
1. Provide detailed requirements
2. Use clear, concise language
3. Include examples in user stories
4. Specify edge cases in constraints
5. Review and refine generated cases

---

**Last Updated**: April 7, 2024
**Status**: ✅ Production Ready
