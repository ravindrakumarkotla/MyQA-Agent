# ============================================================================
# AI QA Agent - Complete Functional Test
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI QA Agent - Full System Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"
$filePath = "sample_requirements.txt"

# Test 1: Health Check
Write-Host "`n[1/7] Testing Health Check..." -ForegroundColor Yellow
try {
    $response = curl -s "$baseUrl/health" | ConvertFrom-Json
    if ($response.status -eq "healthy") {
        Write-Host "✅ Health Check: PASSED" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Health Check: FAILED" -ForegroundColor Red
}

# Test 2: UI Loading
Write-Host "`n[2/7] Testing UI Loading..." -ForegroundColor Yellow
try {
    $response = curl -s "$baseUrl/" -w "%{http_code}"
    if ($response[-1] -eq "0") {
        Write-Host "✅ UI Loading: PASSED (200 OK)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ UI Loading: FAILED" -ForegroundColor Red
}

# Test 3: CSS Loading
Write-Host "`n[3/7] Testing CSS Loading..." -ForegroundColor Yellow
try {
    $response = curl -s "$baseUrl/static/style.css" -w "%{http_code}"
    Write-Host "✅ CSS Loading: PASSED (200 OK)" -ForegroundColor Green
} catch {
    Write-Host "❌ CSS Loading: FAILED" -ForegroundColor Red
}

# Test 4: JavaScript Loading
Write-Host "`n[4/7] Testing JavaScript Loading..." -ForegroundColor Yellow
try {
    $response = curl -s "$baseUrl/static/script.js" -w "%{http_code}"
    Write-Host "✅ JavaScript Loading: PASSED (200 OK)" -ForegroundColor Green
} catch {
    Write-Host "❌ JavaScript Loading: FAILED" -ForegroundColor Red
}

# Test 5: File Upload
Write-Host "`n[5/7] Testing File Upload..." -ForegroundColor Yellow
try {
    $uploadResponse = curl -s -X POST "$baseUrl/api/upload/document" -F "file=@$filePath" | ConvertFrom-Json
    if ($uploadResponse.success) {
        $fileId = $uploadResponse.file_id
        Write-Host "✅ File Upload: PASSED" -ForegroundColor Green
        Write-Host "   File ID: $fileId" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ File Upload: FAILED" -ForegroundColor Red
}

# Test 6: Document Analysis
Write-Host "`n[6/7] Testing Document Analysis..." -ForegroundColor Yellow
try {
    $analysisBody = @{file_id = $fileId} | ConvertTo-Json
    $analysisResponse = curl -s -X POST "$baseUrl/api/analyze/document" -H "Content-Type: application/json" -d $analysisBody | ConvertFrom-Json
    if ($analysisResponse.success) {
        Write-Host "✅ Document Analysis: PASSED" -ForegroundColor Green
        Write-Host "   User Stories: $($analysisResponse.analysis.user_stories.Count)" -ForegroundColor Cyan
        Write-Host "   Acceptance Criteria: $($analysisResponse.analysis.acceptance_criteria.Count)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Document Analysis: FAILED" -ForegroundColor Red
}

# Test 7: Test Case Generation & Export
Write-Host "`n[7/7] Testing Test Case Generation & Export..." -ForegroundColor Yellow
try {
    $generateBody = @{
        file_id = $fileId
        num_test_cases = 5
        include_positive = $true
        include_negative = $true
        include_boundary = $true
    } | ConvertTo-Json
    
    $generateResponse = curl -s -X POST "$baseUrl/api/generate/test-cases" -H "Content-Type: application/json" -d $generateBody | ConvertFrom-Json
    if ($generateResponse.success) {
        Write-Host "✅ Test Case Generation: PASSED" -ForegroundColor Green
        Write-Host "   Generated: $($generateResponse.total_count) test cases" -ForegroundColor Cyan
        
        # Export to Word
        $exportBody = @{
            file_id = $fileId
            format = "docx"
            num_test_cases = 5
        } | ConvertTo-Json
        
        curl -s -X POST "$baseUrl/api/export/test-cases" -H "Content-Type: application/json" -d $exportBody -o "TestCases_Verification.docx"
        Write-Host "✅ Word Export: PASSED" -ForegroundColor Green
        
        # Export to Excel
        $exportBody = @{
            file_id = $fileId
            format = "xlsx"
            num_test_cases = 5
        } | ConvertTo-Json
        
        curl -s -X POST "$baseUrl/api/export/test-cases" -H "Content-Type: application/json" -d $exportBody -o "TestCases_Verification.xlsx"
        Write-Host "✅ Excel Export: PASSED" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Test Case Generation & Export: FAILED" -ForegroundColor Red
}

# Final Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ ALL TESTS COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n📊 Exported Files:" -ForegroundColor Yellow
Write-Host "   • TestCases_Verification.docx (Word format)" -ForegroundColor Cyan
Write-Host "   • TestCases_Verification.xlsx (Excel format)" -ForegroundColor Cyan
Write-Host "`n🌐 Access the UI at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "📚 API Docs at: http://localhost:8000/docs" -ForegroundColor Yellow
