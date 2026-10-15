/**
 * Upload & Submission Handling Service
 */
import { db, storage, isFirebaseInitialized } from './firebase.js';

const LOCAL_STORAGE_DESIGNS_KEY = 'loginscreen_community_local_designs';

export async function submitDesignPackage(designData, user) {
  if (!user) {
    throw new Error('You must be signed in to submit a design.');
  }

  const submissionId = 'design_' + Date.now();
  let previewUrl = 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80';
  let zipDownloadUrl = '#';

  // Read preview file as Base64/DataURL if provided locally
  if (designData.previewImageFile) {
    previewUrl = await readFileAsDataURL(designData.previewImageFile);
  }

  const newSubmission = {
    id: submissionId,
    title: designData.title,
    description: designData.description,
    category: designData.category,
    tags: designData.tags || [],
    previewImage: previewUrl,
    downloadUrl: zipDownloadUrl,
    codeSnippet: designData.codeSnippet || getSampleHTMLCode(designData.title),
    creatorId: user.uid,
    creatorName: user.displayName || user.email.split('@')[0],
    creatorAvatar: user.photoURL || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
    status: 'pending', // Set initial submission status to pending moderation
    createdAt: new Date().toISOString(),
    views: 0,
    downloads: 0,
    likes: 0
  };

  // Save to Firestore if connected
  if (isFirebaseInitialized && db) {
    try {
      const { doc, setDoc } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      await setDoc(doc(db, 'designs', submissionId), newSubmission);
    } catch (err) {
      console.warn('Firestore submission failed, using local storage backup:', err.message);
    }
  }

  // Update Local Storage
  const stored = JSON.parse(localStorage.getItem(LOCAL_STORAGE_DESIGNS_KEY) || '[]');
  stored.unshift(newSubmission);
  localStorage.setItem(LOCAL_STORAGE_DESIGNS_KEY, JSON.stringify(stored));

  return newSubmission;
}

export async function updateSubmissionStatus(designId, status, reviewNotes = '') {
  if (isFirebaseInitialized && db) {
    try {
      const { doc, updateDoc } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      await updateDoc(doc(db, 'designs', designId), {
        status,
        reviewNotes,
        reviewedAt: new Date().toISOString()
      });
    } catch (err) {
      console.warn('Firestore status update error:', err.message);
    }
  }

  const stored = JSON.parse(localStorage.getItem(LOCAL_STORAGE_DESIGNS_KEY) || '[]');
  const idx = stored.findIndex(d => d.id === designId);
  if (idx !== -1) {
    stored[idx].status = status;
    stored[idx].reviewNotes = reviewNotes;
    localStorage.setItem(LOCAL_STORAGE_DESIGNS_KEY, JSON.stringify(stored));
  }
}

function readFileAsDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function getSampleHTMLCode(title) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #0f172a; color: #fff; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
    .card { background: rgba(255,255,255,0.08); padding: 2rem; border-radius: 16px; width: 320px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
    h2 { margin-top: 0; font-size: 1.25rem; text-align: center; }
    input { width: 100%; padding: 0.75rem; margin-bottom: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.2); color: #fff; box-sizing: border-box; }
    button { width: 100%; padding: 0.75rem; background: #4f46e5; color: #fff; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Welcome Back</h2>
    <input type="email" placeholder="Email Address">
    <input type="password" placeholder="Password">
    <button>Sign In</button>
  </div>
</body>
</html>`;
}
