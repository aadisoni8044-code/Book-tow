/**
 * User Profile Service
 */
import { db, isFirebaseInitialized } from './firebase.js';

export async function getCreatorProfile(userId) {
  if (isFirebaseInitialized && db) {
    try {
      const { doc, getDoc } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      const snap = await getDoc(doc(db, 'users', userId));
      if (snap.exists()) return { uid: snap.id, ...snap.data() };
    } catch (e) {
      console.warn('Firestore profile fetch error:', e.message);
    }
  }

  // Fallback profile
  return {
    uid: userId,
    displayName: 'Elena Rostova',
    bio: 'UI/UX Designer & Frontend Engineer creating interactive glassmorphic and web3 login screens.',
    photoURL: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150',
    location: 'San Francisco, CA',
    website: 'https://github.com',
    twitter: '@elena_design',
    joinedAt: '2024-01-15'
  };
}

export async function updateProfile(userId, profileData) {
  if (isFirebaseInitialized && db) {
    try {
      const { doc, setDoc } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      await setDoc(doc(db, 'users', userId), profileData, { merge: true });
    } catch (e) {
      console.warn('Profile update error:', e.message);
    }
  }

  const stored = JSON.parse(localStorage.getItem('loginscreen_community_local_user') || '{}');
  if (stored && stored.uid === userId) {
    Object.assign(stored, profileData);
    localStorage.setItem('loginscreen_community_local_user', JSON.stringify(stored));
  }
}
