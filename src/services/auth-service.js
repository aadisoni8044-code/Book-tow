/**
 * Firebase Authentication & User State Service
 */
import { auth, isFirebaseInitialized } from './firebase.js';

let currentUser = null;
let authListeners = [];

const LOCAL_STORAGE_USER_KEY = 'loginscreen_community_local_user';

export function getCurrentUser() {
  if (currentUser) return currentUser;
  const stored = localStorage.getItem(LOCAL_STORAGE_USER_KEY);
  if (stored) {
    try {
      currentUser = JSON.parse(stored);
      return currentUser;
    } catch (e) {
      localStorage.removeItem(LOCAL_STORAGE_USER_KEY);
    }
  }
  return null;
}

export function initAuthListener(onUserChanged) {
  if (onUserChanged) authListeners.push(onUserChanged);

  if (isFirebaseInitialized && auth) {
    import('https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js').then(({ onAuthStateChanged }) => {
      onAuthStateChanged(auth, (user) => {
        if (user) {
          currentUser = {
            uid: user.uid,
            displayName: user.displayName || 'Community Creator',
            email: user.email,
            photoURL: user.photoURL || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
            isAdmin: user.email?.endsWith('@admin.com') || false
          };
          localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
        } else {
          currentUser = null;
          localStorage.removeItem(LOCAL_STORAGE_USER_KEY);
        }
        notifyListeners();
      });
    }).catch(() => {
      notifyListeners();
    });
  } else {
    notifyListeners();
  }
}

function notifyListeners() {
  const user = getCurrentUser();
  authListeners.forEach(listener => listener(user));
}

export async function signInWithEmail(email, password) {
  if (isFirebaseInitialized && auth) {
    try {
      const { signInWithEmailAndPassword } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js');
      const cred = await signInWithEmailAndPassword(auth, email, password);
      currentUser = {
        uid: cred.user.uid,
        displayName: cred.user.displayName || email.split('@')[0],
        email: cred.user.email,
        photoURL: cred.user.photoURL || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
        isAdmin: email.includes('admin')
      };
      localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
      notifyListeners();
      return currentUser;
    } catch (err) {
      throw err;
    }
  } else {
    // Local fallback sign-in
    currentUser = {
      uid: 'user_' + Date.now(),
      displayName: email.split('@')[0],
      email: email,
      photoURL: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
      isAdmin: email.includes('admin')
    };
    localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
    notifyListeners();
    return currentUser;
  }
}

export async function signUpWithEmail(email, password, displayName) {
  if (isFirebaseInitialized && auth) {
    try {
      const { createUserWithEmailAndPassword, updateProfile } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js');
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(cred.user, { displayName });
      currentUser = {
        uid: cred.user.uid,
        displayName: displayName,
        email: cred.user.email,
        photoURL: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
        isAdmin: email.includes('admin')
      };
      localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
      notifyListeners();
      return currentUser;
    } catch (err) {
      throw err;
    }
  } else {
    currentUser = {
      uid: 'user_' + Date.now(),
      displayName: displayName || email.split('@')[0],
      email: email,
      photoURL: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
      isAdmin: email.includes('admin')
    };
    localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
    notifyListeners();
    return currentUser;
  }
}

export async function signInWithGoogle() {
  if (isFirebaseInitialized && auth) {
    try {
      const { signInWithPopup, GoogleAuthProvider } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js');
      const provider = new GoogleAuthProvider();
      const cred = await signInWithPopup(auth, provider);
      currentUser = {
        uid: cred.user.uid,
        displayName: cred.user.displayName,
        email: cred.user.email,
        photoURL: cred.user.photoURL,
        isAdmin: cred.user.email?.includes('admin')
      };
      localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
      notifyListeners();
      return currentUser;
    } catch (err) {
      throw err;
    }
  } else {
    currentUser = {
      uid: 'google_user_' + Date.now(),
      displayName: 'Google Creator',
      email: 'creator@google.com',
      photoURL: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
      isAdmin: false
    };
    localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(currentUser));
    notifyListeners();
    return currentUser;
  }
}

export async function signOutUser() {
  if (isFirebaseInitialized && auth) {
    const { signOut } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js');
    await signOut(auth);
  }
  currentUser = null;
  localStorage.removeItem(LOCAL_STORAGE_USER_KEY);
  notifyListeners();
}
