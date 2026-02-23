<h1>pdf-to-text</h1>
<p>AI coding skill for converting PDF files to clean text. Handles both embedded-text PDFs and scanned/image PDFs via OCR.</p>

<h2>setup</h2>
<p>navigate to ai project skills folder</p>
<ul>
  <li>Antigravity &lt;workspace-root&gt;/.agent/skills/</li>
  <li>Claude Code &lt;workspace-root&gt;/.claude/skills/</li>
</ul>
<pre><code>git clone https://github.com/RandyHaylor/pdf-to-text.git</code></pre>

<h2>use</h2>
<ul>
  <li>option 1: tell ai agent to use the pdf-to-text skill for your task</li>
  <li>option 2: update your project or global agent instructions to incorporate the pdf-to-text skill</li>
</ul>

<hr/>

<h2>Workflow Enhancements</h2>

<p>This skill goes beyond basic extraction with several techniques that improve reliability and output quality.</p>

<ul>
  <li>
    <strong>Two-page sample before full extraction</strong>
    <p>Rather than blindly processing the entire PDF, the agent extracts just the first two pages and evaluates quality before committing to a method. This catches encoding issues, column mangling, and layout problems early — before wasting time on a bad full run.</p>
  </li>
  <li>
    <strong>Comparative method selection</strong>
    <p>When embedded text extraction produces poor results, the agent runs OCR on the same sample pages and compares both outputs side by side. The better method wins. No guessing.</p>
  </li>
  <li>
    <strong>Visual inspection via AI vision</strong>
    <p>When neither extraction method produces clean output, the agent renders pages as images and visually inspects them using multimodal vision. It can see what's actually on the page — watermarks, unusual fonts, columns, embedded images of text — and diagnose the specific issue before recommending a strategy.</p>
  </li>
  <li>
    <strong>User checkpoint before full processing</strong>
    <p>The agent reports its sample findings and recommended approach to the user before running full extraction. No surprises, no wasted processing on the wrong method.</p>
  </li>
  <li>
    <strong>Graceful tool fallback chain</strong>
    <p>The skill defines three extraction paths (<code>pdftotext</code> → <code>ocrmypdf</code> → <code>tesseract</code> + <code>pdftoppm</code>) and checks tool availability upfront. If the preferred tool is missing, it falls through to the next option rather than failing.</p>
  </li>
</ul>
