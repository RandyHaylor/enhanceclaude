---
name: pdf-to-text
description: "Convert PDF files to clean text. Handles both embedded-text PDFs and scanned/image PDFs via OCR. Use when the user wants to import, extract, or convert a PDF to text."
allowed-tools: Bash, Read, Write
argument-hint: [pdf-path] [output-path]
---

# PDF to Text Import

## Workflow

1. **Check if PDF has embedded text**
   ```bash
   pdftotext <input.pdf> - | head -20
   ```
   - If output contains readable text → use `pdftotext` (fast, accurate)
   - If output is empty or garbled → fall back to OCR

2. **Test scan first two pages and evaluate quality**
   ```bash
   pdftotext -f 1 -l 2 <input.pdf> -
   ```
   Read the output and check for:
   - Garbled characters, mojibake, or encoding issues
   - Missing words, merged lines, or broken paragraphs
   - Headers/footers bleeding into body text
   - Table or column data mangled into single lines

   If quality is poor with `pdftotext`, try OCR on the same two pages:
   ```bash
   pdftoppm -f 1 -l 2 -png <input.pdf> /tmp/test-scan
   tesseract /tmp/test-scan-1.png - 2>/dev/null
   rm /tmp/test-scan-*.png
   ```

   Compare both outputs. Report findings to user before proceeding with full extraction.

   If neither produces clean output, visually inspect the pages:
   ```bash
   pdftoppm -f 1 -l 2 -png -r 200 <input.pdf> /tmp/visual-check
   ```
   Use the Read tool to view `/tmp/visual-check-1.png` and `/tmp/visual-check-2.png` (Claude vision will render them). Compare what you see on the page to what the text extraction produced. Identify the specific issue (columns, watermarks, unusual fonts, embedded images of text, etc.) and recommend an extraction strategy before proceeding.
   ```bash
   rm /tmp/visual-check-*.png
   ```

3. **Extract text**

   Embedded text (preferred):
   ```bash
   pdftotext <input.pdf> <output.txt>
   ```

   Scanned/image PDF (OCR fallback):
   ```bash
   ocrmypdf --force-ocr <input.pdf> /tmp/ocr-temp.pdf
   pdftotext /tmp/ocr-temp.pdf <output.txt>
   rm /tmp/ocr-temp.pdf
   ```

   If `ocrmypdf` is not installed:
   ```bash
   # Convert pages to images, then OCR
   pdftoppm <input.pdf> /tmp/pdf-page -png
   tesseract /tmp/pdf-page-*.png <output> txt
   rm /tmp/pdf-page-*.png
   ```

3. **Report results**
   ```bash
   wc -l <output.txt>
   pdfinfo <input.pdf> | grep Pages
   ```
   - Report page count and line count to user

## Arguments

- `$ARGUMENTS[0]` — path to input PDF (required)
- `$ARGUMENTS[1]` — path to output txt file (optional, defaults to same name with .txt extension)

## Tool Requirements

Requires at least one of:
- `pdftotext` (from poppler-utils) — for embedded text PDFs
- `ocrmypdf` + `pdftotext` — for scanned PDFs
- `tesseract` + `pdftoppm` — OCR fallback if ocrmypdf unavailable

Check availability before starting:
```bash
which pdftotext ocrmypdf tesseract pdftoppm 2>/dev/null
```

If missing tools, tell the user what to install:
- `sudo apt install poppler-utils` — pdftotext and pdftoppm
- `sudo apt install tesseract-ocr` — tesseract
- `pip install ocrmypdf` — ocrmypdf
