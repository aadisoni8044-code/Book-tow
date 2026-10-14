// Firestore Data Service & Mock Store Sync
import { db, isConfigured } from './firebase-config.js';
import {
  collection,
  getDocs,
  getDoc,
  doc,
  addDoc,
  updateDoc,
  query,
  where,
  orderBy,
  limit,
  increment
} from 'https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js';

// Starter Sample Data for Instant Dynamic Rendering
const SAMPLE_DESIGNS = [
  {
    id: 'design_1',
    title: 'CyberPulse Glassmorphism',
    description: 'A futuristic dark glassmorphic login interface with neon cyan accents, real-time input glowing effects, and smooth micro-interactions.',
    category: 'Glassmorphism',
    tags: ['Glassmorphism', 'Futuristic', 'Dark Mode'],
    previewImage: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop',
    downloadUrl: '#sample-zip',
    htmlCode: `
      <div style="min-height:100vh; background:#0b0f19; display:flex; align-items:center; justify-content:center; padding:1rem;">
        <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(0,240,255,0.3); border-radius:16px; padding:2.5rem; width:100%; max-width:380px; backdrop-filter:blur(12px); color:#fff; box-shadow:0 0 30px rgba(0,240,255,0.15);">
          <h2 style="margin-bottom:0.5rem; text-align:center; font-family:sans-serif; color:#00f0ff;">CYBER//PULSE</h2>
          <p style="text-align:center; font-size:0.85rem; color:#8a99ad; margin-bottom:1.5rem;">Access Secure Terminal</p>
          <div style="margin-bottom:1rem;">
            <label style="display:block; font-size:0.8rem; margin-bottom:0.4rem; color:#8a99ad;">User Identity</label>
            <input type="text" placeholder="net_runner" style="width:100%; padding:0.75rem; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:8px; color:#fff; outline:none;" />
          </div>
          <div style="margin-bottom:1.5rem;">
            <label style="display:block; font-size:0.8rem; margin-bottom:0.4rem; color:#8a99ad;">Access Passcode</label>
            <input type="password" placeholder="••••••••" style="width:100%; padding:0.75rem; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:8px; color:#fff; outline:none;" />
          </div>
          <button style="width:100%; padding:0.8rem; background:linear-gradient(135deg, #00f0ff, #7000ff); border:none; border-radius:8px; color:#fff; font-weight:bold; cursor:pointer;">Authenticate</button>
        </div>
      </div>
    `,
    cssCode: '',
    jsCode: '',
    creatorUid: 'creator_1',
    creatorName: 'Alex Rivera',
    creatorAvatar: 'A',
    status: 'approved',
    downloads: 1420,
    createdAt: new Date(Date.now() - 86400000 * 5).toISOString()
  },
  {
    id: 'design_2',
    title: 'Minimalist Clean Slate',
    description: 'An elegant, high-contrast minimal login form with subtle border hover states and accessible keyboard controls.',
    category: 'Minimal',
    tags: ['Minimal', 'Clean', 'Light & Dark'],
    previewImage: 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?q=80&w=800&auto=format&fit=crop',
    downloadUrl: '#sample-zip',
    htmlCode: `
      <div style="min-height:100vh; background:#f8fafc; display:flex; align-items:center; justify-content:center; padding:1rem; font-family:sans-serif;">
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:2rem; width:100%; max-width:360px; box-shadow:0 10px 25px -5px rgba(0,0,0,0.05); color:#0f172a;">
          <h3 style="font-size:1.4rem; font-weight:700; margin-bottom:0.25rem;">Sign In</h3>
          <p style="font-size:0.875rem; color:#64748b; margin-bottom:1.5rem;">Enter your credentials to continue</p>
          <div style="margin-bottom:1rem;">
            <label style="display:block; font-size:0.8rem; font-weight:600; margin-bottom:0.4rem;">Email</label>
            <input type="email" placeholder="name@company.com" style="width:100%; padding:0.65rem 0.85rem; border:1px solid #cbd5e1; border-radius:6px; font-size:0.9rem;" />
          </div>
          <div style="margin-bottom:1.25rem;">
            <label style="display:block; font-size:0.8rem; font-weight:600; margin-bottom:0.4rem;">Password</label>
            <input type="password" placeholder="••••••••" style="width:100%; padding:0.65rem 0.85rem; border:1px solid #cbd5e1; border-radius:6px; font-size:0.9rem;" />
          </div>
          <button style="width:100%; padding:0.75rem; background:#0f172a; color:#fff; border:none; border-radius:6px; font-weight:600; cursor:pointer;">Continue</button>
        </div>
      </div>
    `,
    cssCode: '',
    jsCode: '',
    creatorUid: 'creator_2',
    creatorName: 'Elena Rostova',
    creatorAvatar: 'E',
    status: 'approved',
    downloads: 980,
    createdAt: new Date(Date.now() - 86400000 * 3).toISOString()
  },
  {
    id: 'design_3',
    title: 'Neon Aurora Login Portal',
    description: 'Dynamic gradient backdrop with interactive card tilt physics and social sign-in buttons.',
    category: 'Gradient & Animated',
    tags: ['Gradient', '3D Perspective', 'Animated'],
    previewImage: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=800&auto=format&fit=crop',
    downloadUrl: '#sample-zip',
    htmlCode: `
      <div style="min-height:100vh; background:linear-gradient(135deg, #0f172a, #1e1b4b, #311042); display:flex; align-items:center; justify-content:center; padding:1rem; font-family:sans-serif;">
        <div style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:20px; padding:2.5rem; width:100%; max-width:400px; color:#fff; backdrop-filter:blur(16px);">
          <div style="width:48px; height:48px; background:linear-gradient(135deg, #a855f7, #ec4899); border-radius:12px; margin:0 auto 1rem; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.2rem;">✨</div>
          <h2 style="text-align:center; font-size:1.5rem; margin-bottom:0.25rem;">Aurora Space</h2>
          <p style="text-align:center; color:#cbd5e1; font-size:0.85rem; margin-bottom:1.5rem;">Welcome back to the multiverse</p>
          <button style="width:100%; padding:0.7rem; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); border-radius:8px; color:#fff; font-weight:500; cursor:pointer; margin-bottom:1rem; display:flex; align-items:center; justify-content:center; gap:0.5rem;">Continue with Google</button>
          <div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-bottom:1rem;">OR</div>
          <input type="email" placeholder="Email Address" style="width:100%; padding:0.75rem; background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.15); border-radius:8px; color:#fff; margin-bottom:1rem; outline:none;" />
          <button style="width:100%; padding:0.75rem; background:linear-gradient(135deg, #ec4899, #8b5cf6); border:none; border-radius:8px; color:#fff; font-weight:600; cursor:pointer;">Enter Portal</button>
        </div>
      </div>
    `,
    cssCode: '',
    jsCode: '',
    creatorUid: 'creator_3',
    creatorName: 'Marcus Vance',
    creatorAvatar: 'M',
    status: 'approved',
    downloads: 2150,
    createdAt: new Date(Date.now() - 86400000 * 2).toISOString()
  }
];

class FirestoreService {
  constructor() {
    this.initMockStore();
  }

  initMockStore() {
    if (!localStorage.getItem('lsc_mock_designs')) {
      localStorage.setItem('lsc_mock_designs', JSON.stringify(SAMPLE_DESIGNS));
    }
  }

  getMockDesigns() {
    try {
      return JSON.parse(localStorage.getItem('lsc_mock_designs')) || SAMPLE_DESIGNS;
    } catch (e) {
      return SAMPLE_DESIGNS;
    }
  }

  saveMockDesigns(designs) {
    localStorage.setItem('lsc_mock_designs', JSON.stringify(designs));
  }

  async getApprovedDesigns(filters = {}) {
    if (isConfigured && db) {
      try {
        let q = query(collection(db, 'designs'), where('status', '==', 'approved'));
        const querySnapshot = await getDocs(q);
        let list = [];
        querySnapshot.forEach(doc => {
          list.push({ id: doc.id, ...doc.data() });
        });

        // Apply search & filtering
        return this.filterAndSortDesigns(list, filters);
      } catch (err) {
        console.warn("Firestore fetch error, falling back to mock store:", err);
      }
    }

    const mockList = this.getMockDesigns().filter(d => d.status === 'approved');
    return this.filterAndSortDesigns(mockList, filters);
  }

  filterAndSortDesigns(list, filters) {
    let result = [...list];

    if (filters.category && filters.category !== 'All') {
      result = result.filter(d => d.category?.toLowerCase() === filters.category.toLowerCase());
    }

    if (filters.search) {
      const term = filters.search.toLowerCase();
      result = result.filter(d =>
        d.title?.toLowerCase().includes(term) ||
        d.description?.toLowerCase().includes(term) ||
        d.creatorName?.toLowerCase().includes(term) ||
        (d.tags && d.tags.some(t => t.toLowerCase().includes(term)))
      );
    }

    if (filters.sort === 'popular') {
      result.sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
    } else {
      // Default newest
      result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    return result;
  }

  async getPendingDesigns() {
    if (isConfigured && db) {
      try {
        const q = query(collection(db, 'designs'), where('status', '==', 'pending'));
        const snap = await getDocs(q);
        let list = [];
        snap.forEach(doc => list.push({ id: doc.id, ...doc.data() }));
        return list;
      } catch (e) {
        console.warn("Firestore pending query error:", e);
      }
    }

    return this.getMockDesigns().filter(d => d.status === 'pending');
  }

  async getDesignById(id) {
    if (isConfigured && db) {
      try {
        const docRef = doc(db, 'designs', id);
        const snap = await getDoc(docRef);
        if (snap.exists()) {
          return { id: snap.id, ...snap.data() };
        }
      } catch (e) {
        console.warn("Firestore get item error:", e);
      }
    }

    return this.getMockDesigns().find(d => d.id === id) || null;
  }

  async submitDesign(designData) {
    const newDesign = {
      ...designData,
      status: 'pending',
      downloads: 0,
      createdAt: new Date().toISOString()
    };

    if (isConfigured && db) {
      const docRef = await addDoc(collection(db, 'designs'), newDesign);
      return { id: docRef.id, ...newDesign };
    } else {
      const mockList = this.getMockDesigns();
      const mockId = 'design_' + Date.now();
      const savedDesign = { id: mockId, ...newDesign };
      mockList.unshift(savedDesign);
      this.saveMockDesigns(mockList);
      return savedDesign;
    }
  }

  async updateDesignStatus(id, newStatus) {
    if (isConfigured && db) {
      const docRef = doc(db, 'designs', id);
      await updateDoc(docRef, { status: newStatus });
    } else {
      const mockList = this.getMockDesigns();
      const target = mockList.find(d => d.id === id);
      if (target) {
        target.status = newStatus;
        this.saveMockDesigns(mockList);
      }
    }
  }

  async incrementDownloadCount(id) {
    if (isConfigured && db) {
      const docRef = doc(db, 'designs', id);
      await updateDoc(docRef, { downloads: increment(1) });
    } else {
      const mockList = this.getMockDesigns();
      const target = mockList.find(d => d.id === id);
      if (target) {
        target.downloads = (target.downloads || 0) + 1;
        this.saveMockDesigns(mockList);
      }
    }
  }

  async getCreators() {
    const approved = await this.getApprovedDesigns();
    const creatorsMap = {};

    approved.forEach(d => {
      if (!creatorsMap[d.creatorUid]) {
        creatorsMap[d.creatorUid] = {
          uid: d.creatorUid,
          displayName: d.creatorName || 'Anonymous',
          avatar: d.creatorAvatar || d.creatorName?.charAt(0) || 'C',
          designCount: 0,
          totalDownloads: 0
        };
      }
      creatorsMap[d.creatorUid].designCount += 1;
      creatorsMap[d.creatorUid].totalDownloads += (d.downloads || 0);
    });

    return Object.values(creatorsMap);
  }

  async getUserDesigns(uid) {
    const all = isConfigured && db ? await (async () => {
      try {
        const q = query(collection(db, 'designs'), where('creatorUid', '==', uid));
        const snap = await getDocs(q);
        let list = [];
        snap.forEach(d => list.push({ id: d.id, ...d.data() }));
        return list;
      } catch (e) {
        return [];
      }
    })() : [];

    if (all.length > 0) return all;

    return this.getMockDesigns().filter(d => d.creatorUid === uid);
  }
}

export const firestoreService = new FirestoreService();
