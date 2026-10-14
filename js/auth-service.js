// Authentication Service Module
import { auth, db, isConfigured } from './firebase-config.js';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  updateProfile
} from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js';
import { doc, setDoc, getDoc, updateDoc } from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js';

// Local Storage Fallback Key
const LOCAL_USER_KEY = 'lsc_user_session';

class AuthService {
  constructor() {
    this.currentUser = null;
    this.listeners = [];
    this.init();
  }

  init() {
    if (isConfigured && auth) {
      onAuthStateChanged(auth, async (user) => {
        if (user) {
          const profile = await this.getUserProfile(user.uid);
          this.currentUser = {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName || profile?.displayName || user.email.split('@')[0],
            photoURL: user.photoURL || profile?.photoURL || '',
            bio: profile?.bio || 'Passionate designer & developer',
            isAdmin: profile?.isAdmin || false,
            createdAt: profile?.createdAt || new Date().toISOString()
          };
        } else {
          this.currentUser = null;
        }
        this.notifyListeners();
      });
    } else {
      // Local fallback session check
      const savedUser = localStorage.getItem(LOCAL_USER_KEY);
      if (savedUser) {
        try {
          this.currentUser = JSON.parse(savedUser);
        } catch (e) {
          this.currentUser = null;
        }
      } else {
        // Create default local guest / demo user
        this.currentUser = null;
      }
      setTimeout(() => this.notifyListeners(), 50);
    }
  }

  onAuthChange(callback) {
    this.listeners.push(callback);
    callback(this.currentUser);
  }

  notifyListeners() {
    this.listeners.forEach(cb => cb(this.currentUser));
  }

  async signUp(email, password, displayName) {
    if (isConfigured && auth) {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      await updateProfile(user, { displayName });

      const userDocData = {
        uid: user.uid,
        email: user.email,
        displayName: displayName,
        photoURL: '',
        bio: 'Passionate UI/UX designer & frontend engineer.',
        isAdmin: email.includes('admin'),
        createdAt: new Date().toISOString(),
        designCount: 0
      };

      if (db) {
        await setDoc(doc(db, 'users', user.uid), userDocData);
      }

      this.currentUser = userDocData;
      return userDocData;
    } else {
      // Fallback local sign up
      const mockUser = {
        uid: 'user_' + Date.now(),
        email,
        displayName: displayName || email.split('@')[0],
        photoURL: '',
        bio: 'Passionate UI/UX designer & frontend engineer.',
        isAdmin: email.toLowerCase().includes('admin'),
        createdAt: new Date().toISOString(),
        designCount: 0
      };

      localStorage.setItem(LOCAL_USER_KEY, JSON.stringify(mockUser));
      this.currentUser = mockUser;
      this.notifyListeners();
      return mockUser;
    }
  }

  async signIn(email, password) {
    if (isConfigured && auth) {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      const profile = await this.getUserProfile(user.uid);

      this.currentUser = {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName || profile?.displayName || email.split('@')[0],
        photoURL: user.photoURL || profile?.photoURL || '',
        bio: profile?.bio || 'Passionate designer & developer',
        isAdmin: profile?.isAdmin || false
      };
      return this.currentUser;
    } else {
      // Fallback local sign in
      const mockUser = {
        uid: 'user_demo_' + Math.floor(Math.random() * 1000),
        email,
        displayName: email.split('@')[0],
        photoURL: '',
        bio: 'Community design enthusiast',
        isAdmin: email.toLowerCase().includes('admin'),
        createdAt: new Date().toISOString()
      };

      localStorage.setItem(LOCAL_USER_KEY, JSON.stringify(mockUser));
      this.currentUser = mockUser;
      this.notifyListeners();
      return mockUser;
    }
  }

  async signOut() {
    if (isConfigured && auth) {
      await firebaseSignOut(auth);
    } else {
      localStorage.removeItem(LOCAL_USER_KEY);
    }
    this.currentUser = null;
    this.notifyListeners();
  }

  async getUserProfile(uid) {
    if (isConfigured && db) {
      try {
        const userDoc = await getDoc(doc(db, 'users', uid));
        if (userDoc.exists()) {
          return userDoc.data();
        }
      } catch (e) {
        console.error("Error fetching user profile:", e);
      }
    }
    return null;
  }

  async updateProfileData(data) {
    if (!this.currentUser) throw new Error("User not authenticated");

    this.currentUser = { ...this.currentUser, ...data };

    if (isConfigured && db && auth?.currentUser) {
      await updateDoc(doc(db, 'users', this.currentUser.uid), data);
      if (data.displayName) {
        await updateProfile(auth.currentUser, { displayName: data.displayName });
      }
    } else {
      localStorage.setItem(LOCAL_USER_KEY, JSON.stringify(this.currentUser));
    }
    this.notifyListeners();
    return this.currentUser;
  }
}

export const authService = new AuthService();
