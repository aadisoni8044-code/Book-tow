/**
 * Design Metadata & Gallery Firestore Query Service
 */
import { db, isFirebaseInitialized } from './firebase.js';

const LOCAL_STORAGE_DESIGNS_KEY = 'loginscreen_community_local_designs';

// Seed Initial Curated Designs
const DEFAULT_DESIGNS = [
  {
    id: 'design-1',
    title: 'Gmail Spatial — VisionOS Modern Glass Login',
    description: 'A futuristic VisionOS-inspired spatial glassmorphism login UI featuring particle canvases, 3D mouse parallax tilt, dynamic ambient audio waves, and smooth Google OAuth sign-in flow.',
    category: 'Glassmorphism',
    tags: ['spatial', 'visionos', 'glass', 'dark', 'gmail'],
    previewImage: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80',
    creatorId: 'creator_1',
    creatorName: 'Elena Rostova',
    creatorAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150',
    status: 'approved',
    createdAt: new Date(Date.now() - 86400000 * 2).toISOString(),
    views: 1240,
    downloads: 380,
    likes: 194
  },
  {
    id: 'design-2',
    title: 'CyberPulse Cybernetic Portal Login',
    description: 'High-tech cybernetic portal authentication dashboard with animated neon grid background, glowing particle shockwaves, interactive password toggle, and biometric scan feedback.',
    category: 'Cyberpunk',
    tags: ['cyberpunk', 'neon', 'futuristic', 'dark-mode'],
    previewImage: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80',
    creatorId: 'creator_2',
    creatorName: 'Marcus Vance',
    creatorAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
    status: 'approved',
    createdAt: new Date(Date.now() - 86400000 * 5).toISOString(),
    views: 2890,
    downloads: 812,
    likes: 420
  },
  {
    id: 'design-3',
    title: 'Liquid Morphing Canvas Login Interface',
    description: 'Minimalist fluid multi-node spring physics surface coupled with neighbor wave propagation, pointer drag stretching, interactive water ripple canvas, and elegant typography.',
    category: 'Minimal',
    tags: ['liquid', 'minimal', 'animation', 'canvas'],
    previewImage: 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=800&auto=format&fit=crop&q=80',
    creatorId: 'creator_3',
    creatorName: 'Sofia Chen',
    creatorAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
    status: 'approved',
    createdAt: new Date(Date.now() - 86400000 * 8).toISOString(),
    views: 950,
    downloads: 240,
    likes: 156
  },
  {
    id: 'design-4',
    title: 'Apex Delivery Express Parcel Login',
    description: 'Charming e-commerce login screen featuring a smooth SVG delivery truck entrance sequence, box scattering canvas physics, unboxing flap transitions, and clear step indicators.',
    category: 'Illustration',
    tags: ['ecommerce', 'parcel', 'truck', 'interactive'],
    previewImage: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&auto=format&fit=crop&q=80',
    creatorId: 'creator_4',
    creatorName: 'Alex Rivera',
    creatorAvatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150',
    status: 'approved',
    createdAt: new Date(Date.now() - 86400000 * 12).toISOString(),
    views: 3120,
    downloads: 1105,
    likes: 680
  }
];

function getStoredDesigns() {
  const stored = localStorage.getItem(LOCAL_STORAGE_DESIGNS_KEY);
  if (!stored) {
    localStorage.setItem(LOCAL_STORAGE_DESIGNS_KEY, JSON.stringify(DEFAULT_DESIGNS));
    return DEFAULT_DESIGNS;
  }
  try {
    return JSON.parse(stored);
  } catch (e) {
    return DEFAULT_DESIGNS;
  }
}

function saveStoredDesigns(designs) {
  localStorage.setItem(LOCAL_STORAGE_DESIGNS_KEY, JSON.stringify(designs));
}

export async function getPublishedDesigns(filters = {}) {
  const { category, search, sortBy = 'newest' } = filters;

  if (isFirebaseInitialized && db) {
    try {
      const { collection, query, where, getDocs, orderBy } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      let q = query(collection(db, 'designs'), where('status', '==', 'approved'));

      const snapshot = await getDocs(q);
      let list = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));

      // Apply client filtering if complex indexes missing
      if (category && category !== 'All') {
        list = list.filter(d => d.category.toLowerCase() === category.toLowerCase());
      }
      if (search) {
        const s = search.toLowerCase();
        list = list.filter(d => d.title.toLowerCase().includes(s) || d.tags?.some(t => t.toLowerCase().includes(s)));
      }
      return list;
    } catch (err) {
      console.warn('Firestore fetch failed, serving local designs:', err.message);
    }
  }

  // Local storage fallback
  let list = getStoredDesigns().filter(d => d.status === 'approved');

  if (category && category !== 'All') {
    list = list.filter(d => d.category.toLowerCase() === category.toLowerCase());
  }
  if (search) {
    const s = search.toLowerCase();
    list = list.filter(d => d.title.toLowerCase().includes(s) || d.tags?.some(t => t.toLowerCase().includes(s)));
  }

  if (sortBy === 'newest') {
    list.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  } else if (sortBy === 'popular') {
    list.sort((a, b) => (b.views || 0) - (a.views || 0));
  }

  return list;
}

export async function getDesignById(id) {
  if (isFirebaseInitialized && db) {
    try {
      const { doc, getDoc } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      const snap = await getDoc(doc(db, 'designs', id));
      if (snap.exists()) return { id: snap.id, ...snap.data() };
    } catch (e) {
      console.warn('Firestore doc read error:', e.message);
    }
  }

  const list = getStoredDesigns();
  return list.find(d => d.id === id) || null;
}

export async function getPendingSubmissions() {
  if (isFirebaseInitialized && db) {
    try {
      const { collection, query, where, getDocs } = await import('https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js');
      const q = query(collection(db, 'designs'), where('status', '==', 'pending'));
      const snap = await getDocs(q);
      return snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    } catch (e) {
      console.warn('Pending fetch error:', e.message);
    }
  }

  return getStoredDesigns().filter(d => d.status === 'pending');
}

export async function getUserUploads(userId) {
  const list = getStoredDesigns();
  return list.filter(d => d.creatorId === userId);
}
