#!/usr/bin/env python
"""
Complete End-to-End Example Script

This script demonstrates the complete workflow of the AI QA Agent:
1. Upload a document
2. Analyze the document
3. Generate test cases
4. Export to Word and Excel

Run this script with: python example_workflow.py
"""

import os
import sys
import json
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.services.document_parser import DocumentParser
from app.services.ai_agent import AIAgent
from app.models.testcase import TestCaseCollection
from app.utils.word_exporter import WordExporter
from app.utils.excel_exporter import ExcelExporter
from datetime import datetime


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def example_workflow():
    """
    Demonstrate the complete AI QA Agent workflow.
    """
    
    print_section("AI QA Agent - End-to-End Workflow Example")
    
    # Configuration
    sample_doc = "sample_requirements.txt"
    output_dir = "exports"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Parse Document
    print_section("STEP 1: Parse Document")
    
    if not os.path.exists(sample_doc):
        print(f"❌ Error: Sample document '{sample_doc}' not found!")
        print(f"   Please ensure '{sample_doc}' exists in the current directory.")
        return
    
    try:
        parser = DocumentParser()
        print(f"✓ Parsing document: {sample_doc}")
        text_content = parser.parse_document(sample_doc)
        print(f"✓ Document parsed successfully")
        print(f"✓ Content length: {len(text_content)} characters")
        print(f"\nFirst 500 characters of document:")
        print("-" * 80)
        print(text_content[:500] + "...")
        print("-" * 80)
    except Exception as e:
        print(f"❌ Error parsing document: {str(e)}")
        return
    
    # Step 2: Analyze Content
    print_section("STEP 2: Analyze Document Content")
    
    try:
        analysis = parser.analyze_content(text_content)
        print("✓ Document analysis completed\n")
        
        print(f"Extracted Information:")
        print(f"  • User Stories: {len(analysis.user_stories)}")
        for i, story in enumerate(analysis.user_stories[:3], 1):
            print(f"    {i}. {story[:70]}...")
        
        print(f"\n  • Acceptance Criteria: {len(analysis.acceptance_criteria)}")
        for i, criteria in enumerate(analysis.acceptance_criteria[:3], 1):
            print(f"    {i}. {criteria[:70]}...")
        
        print(f"\n  • Preconditions: {len(analysis.preconditions)}")
        for i, pre in enumerate(analysis.preconditions[:3], 1):
            print(f"    {i}. {pre[:70]}...")
        
        print(f"\n  • Business Rules: {len(analysis.business_rules)}")
        for i, rule in enumerate(analysis.business_rules[:3], 1):
            print(f"    {i}. {rule[:70]}...")
        
        print(f"\n  • Constraints: {len(analysis.constraints)}")
        for i, constraint in enumerate(analysis.constraints[:3], 1):
            print(f"    {i}. {constraint[:70]}...")
    
    except Exception as e:
        print(f"❌ Error analyzing document: {str(e)}")
        return
    
    # Step 3: Generate Test Cases
    print_section("STEP 3: Generate Test Cases")
    
    try:
        ai_agent = AIAgent()  # Uses mock responses by default
        print(f"✓ Initializing AI Agent (using mock mode)")
        
        num_cases = 10
        print(f"✓ Generating {num_cases} test cases...")
        test_cases = ai_agent.generate_test_cases(
            analysis,
            sample_doc,
            num_cases=num_cases
        )
        
        print(f"✓ Successfully generated {len(test_cases)} test cases\n")
        
        # Display test case summary
        print("Generated Test Cases Summary:")
        print("-" * 80)
        for i, tc in enumerate(test_cases[:5], 1):
            print(f"\n{i}. {tc.test_case_id} - {tc.name}")
            print(f"   Type: {tc.test_type.upper()} | Priority: {tc.priority.upper()}")
            print(f"   Description: {tc.description[:60]}...")
            print(f"   Pre-Condition: {tc.pre_condition[:60]}...")
            print(f"   Steps: {len(tc.test_steps)}")
        
        if len(test_cases) > 5:
            print(f"\n... and {len(test_cases) - 5} more test cases")
        print("-" * 80)
    
    except Exception as e:
        print(f"❌ Error generating test cases: {str(e)}")
        return
    
    # Step 4: Create Test Case Collection
    print_section("STEP 4: Create Test Case Collection")
    
    try:
        collection = TestCaseCollection(
            document_name=os.path.basename(sample_doc),
            test_cases=test_cases,
            total_count=len(test_cases),
            generated_at=datetime.now().isoformat()
        )
        print("✓ Test case collection created successfully")
        print(f"  • Document: {collection.document_name}")
        print(f"  • Total Test Cases: {collection.total_count}")
        print(f"  • Generated At: {collection.generated_at}")
    
    except Exception as e:
        print(f"❌ Error creating collection: {str(e)}")
        return
    
    # Step 5: Export to Word
    print_section("STEP 5: Export to Word Document (.docx)")
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        word_file = os.path.join(output_dir, f"TestCases_{timestamp}.docx")
        
        print(f"✓ Exporting to Word format...")
        WordExporter.export_collection(collection, word_file)
        
        file_size = os.path.getsize(word_file) / 1024  # Convert to KB
        print(f"✓ Word document created successfully")
        print(f"  • File: {word_file}")
        print(f"  • Size: {file_size:.2f} KB")
    
    except Exception as e:
        print(f"❌ Error exporting to Word: {str(e)}")
    
    # Step 6: Export to Excel
    print_section("STEP 6: Export to Excel Spreadsheet (.xlsx)")
    
    try:
        excel_file = os.path.join(output_dir, f"TestCases_{timestamp}.xlsx")
        
        print(f"✓ Exporting to Excel format...")
        ExcelExporter.export_collection(collection, excel_file)
        
        file_size = os.path.getsize(excel_file) / 1024  # Convert to KB
        print(f"✓ Excel document created successfully")
        print(f"  • File: {excel_file}")
        print(f"  • Size: {file_size:.2f} KB")
        print(f"  • Sheets: Test Cases, Test Steps, Metadata")
    
    except Exception as e:
        print(f"❌ Error exporting to Excel: {str(e)}")
    
    # Step 7: Summary
    print_section("WORKFLOW COMPLETE ✓")
    
    print("Summary:")
    print(f"  ✓ Parsed document: {sample_doc}")
    print(f"  ✓ Generated {len(test_cases)} test cases")
    print(f"  ✓ Exported to Word format (.docx)")
    print(f"  ✓ Exported to Excel format (.xlsx)")
    print(f"\nOutput files are located in: {os.path.abspath(output_dir)}/")
    print("\nNext Steps:")
    print("  1. Review the generated test cases in Word or Excel")
    print("  2. Start the FastAPI server: uvicorn app.main:app --reload")
    print("  3. Access the API documentation: http://localhost:8000/docs")
    print("  4. Upload documents via the API endpoints")


def api_integration_example():
    """
    Example of how to integrate with the FastAPI application.
    """
    
    print_section("API Integration Example")
    
    print("To use the AI QA Agent via the REST API:")
    print()
    print("1. Start the server:")
    print("   $ uvicorn app.main:app --reload")
    print()
    print("2. Upload a document:")
    print('   $ curl -X POST "http://localhost:8000/api/upload/document" \\')
    print('     -F "file=@sample_requirements.txt"')
    print()
    print("3. Analyze the document:")
    print('   $ curl -X POST "http://localhost:8000/api/analyze/document" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"file_id": "20240407_123456_sample_requirements.txt"}\'')
    print()
    print("4. Generate test cases:")
    print('   $ curl -X POST "http://localhost:8000/api/generate/test-cases" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"file_id": "20240407_123456_sample_requirements.txt", "num_test_cases": 10}\'')
    print()
    print("5. Export to Word:")
    print('   $ curl -X POST "http://localhost:8000/api/export/test-cases" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"file_id": "20240407_123456_sample_requirements.txt", "format": "docx"}\' \\')
    print('     -o TestCases.docx')
    print()
    print("6. Export to Excel:")
    print('   $ curl -X POST "http://localhost:8000/api/export/test-cases" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"file_id": "20240407_123456_sample_requirements.txt", "format": "xlsx"}\' \\')
    print('     -o TestCases.xlsx')
    print()
    print("Access API Documentation:")
    print("  • Swagger UI: http://localhost:8000/docs")
    print("  • ReDoc: http://localhost:8000/redoc")


if __name__ == "__main__":
    # Run the example workflow
    example_workflow()
    
    # Show API integration example
    print("\n\n")
    api_integration_example()
    
    print("\n\n")
    print_section("Thank you for using AI QA Agent! 🚀")
