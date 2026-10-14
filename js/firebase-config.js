// Firebase Config and Storage Initialization
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js';
import { getStorage } from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-storage.js';

// Default configuration with environment dynamic fallback options
const firebaseConfig = window.FIREBASE_CONFIG || {
  apiKey: "AIzaSyDemoKeyForTestingAndVerificationOnly",
  authDomain: "loginscreen-community.firebaseapp.com",
  projectId: "loginscreen-community",
  storageBucket: "loginscreen-community.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};

let app, auth, db, storage;
let isConfigured = false;

try {
  // Check if real keys are provided or fallback to local mode
  if (firebaseConfig.apiKey && !firebaseConfig.apiKey.includes("DemoKey")) {
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    db = getFirestore(app);
    storage = getStorage(app);
    isConfigured = true;
    console.log("Firebase initialized successfully with custom project config.");
  } else {
    console.warn("Firebase running in Local Fallback Mock Store mode. Supply window.FIREBASE_CONFIG to connect to live project.");
  }
} catch (error) {
  console.error("Firebase initialization failed:", error);
}

export { app, auth, db, storage, isConfigured };
