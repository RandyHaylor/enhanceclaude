# PDF to Text

**Type:** skill | **Version:** 1.0.0 | **OS:** linux, macos

Convert PDF files to clean text. Handles both embedded-text PDFs and scanned/image PDFs via OCR.

## Tags
pdf, text-extraction, ocr, document-processing, conversion

## Overview
This skill converts PDF documents to clean, readable text using a smart extraction workflow. It first checks whether a PDF contains embedded text (using pdftotext) and falls back to OCR (via ocrmypdf or tesseract) for scanned or image-based PDFs. The skill includes a quality evaluation step that compares extraction methods on sample pages before committing to a full conversion, ensuring the best possible output.

## Try These Prompts
- Convert this PDF to text: /path/to/document.pdf
- Extract the text from report.pdf and save it to report.txt
- This PDF looks scanned — can you OCR it and give me the text?
- Pull the text out of contract.pdf so I can edit it

## Use Cases
- Extracting text from scanned or image-based PDFs
- Converting research papers or reports for editing
- Importing PDF content into downstream AI workflows
- Archiving or indexing document libraries as plain text

## Additional Requirements
Requires pdftotext (poppler-utils), and optionally tesseract-ocr and ocrmypdf for scanned PDFs. Install: sudo apt install poppler-utils tesseract-ocr (Linux) or brew install poppler tesseract (macOS).

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
