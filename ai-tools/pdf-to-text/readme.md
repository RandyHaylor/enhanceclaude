# PDF to Text

**Type:** skill | **Version:** 1.0.0 | **Platform:** Claude Code

Convert PDF files to clean text. Handles both embedded-text PDFs and scanned/image PDFs via OCR.

## Tags
pdf, text-extraction, ocr, document-processing, conversion

## Overview
This skill converts PDF documents to clean, readable text using a smart extraction workflow. It first checks whether a PDF contains embedded text (using pdftotext) and falls back to OCR (via ocrmypdf or tesseract) for scanned or image-based PDFs. The skill includes a quality evaluation step that compares extraction methods on sample pages before committing to a full conversion, ensuring the best possible output.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
