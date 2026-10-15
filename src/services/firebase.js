/**
 * Firebase Client Initialization & Fallback Configuration
 */

// Default fallback configuration placeholder
const firebaseConfig = {
  apiKey: import.meta?.env?.VITE_FIREBASE_API_KEY || "AIzaSyDemoKeyPlaceholderForTestingModeOnly",
  authDomain: "loginscreen-community.firebaseapp.com",
  projectId: "loginscreen-community",
  storageBucket: "loginscreen-community.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};

export let firebaseApp = null;
export let auth = null;
export let db = null;
export let storage = null;
export let isFirebaseInitialized = false;

// Initialize Firebase dynamically via CDN module loading with Local Storage Fallback
export async function initFirebase() {
  if (isFirebaseInitialized) return { auth, db, storage };

  try {
    const { initializeApp } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js');
    const { getAuth, GoogleAuthProvider } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js');
    const { getFirestore } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
    const { getStorage } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js');

    firebaseApp = initializeApp(firebaseConfig);
    auth = getAuth(firebaseApp);
    db = getFirestore(firebaseApp);
    storage = getStorage(firebaseApp);
    isFirebaseInitialized = true;

    console.log('Firebase initialized successfully.');
  } catch (err) {
    console.warn('Firebase CDN initialization unavailable or offline. Falling back to local offline storage provider mode:', err.message);
    isFirebaseInitialized = false;
  }

  return { auth, db, storage, isFirebaseInitialized };
}

// Initial auto-boot init
initFirebase();
