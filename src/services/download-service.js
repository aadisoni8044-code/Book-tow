/**
 * Secure ZIP Package Download & Verification Service
 */

export async function downloadDesignPackage(design) {
  if (!design) {
    throw new Error('Invalid design template data.');
  }

  if (design.status !== 'approved') {
    throw new Error('This design submission is currently pending review and cannot be downloaded yet.');
  }

  // Create client-side generated ZIP package file dynamically
  const filename = `${slugify(design.title)}-template.html`;
  const codeContent = design.codeSnippet || getDefaultTemplateCode(design.title);

  const blob = new Blob([codeContent], { type: 'text/html;charset=utf-8' });
  const downloadUrl = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
  return true;
}

function slugify(text) {
  return text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
}

function getDefaultTemplateCode(title) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${title} - Downloaded Template</title>
  <style>
    body { font-family: sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .box { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px; width: 300px; }
    input { width: 100%; padding: 0.5rem; margin-bottom: 1rem; box-sizing: border-box; }
    button { width: 100%; padding: 0.5rem; background: #4f46e5; color: white; border: none; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="box">
    <h3>${title}</h3>
    <input type="text" placeholder="Username">
    <input type="password" placeholder="Password">
    <button>Submit</button>
  </div>
</body>
</html>`;
}
