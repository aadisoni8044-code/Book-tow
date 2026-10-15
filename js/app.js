/**
 * AUTHVAULT — DRIBBBLE-INSPIRED LOGIN SCREEN GALLERY & SANDBOX
 * Main Application Logic, Sandboxed Live Preview, Download & Firebase Integration
 */

class AuthVaultApp {
  constructor() {
    this.designs = [];
    this.filteredDesigns = [];
    this.activeCategory = 'all';
    this.activeTech = 'all';
    this.activeSort = 'popular';
    this.searchQuery = '';
    this.currentPreviewDesign = null;
    this.userLikes = new Set(JSON.parse(localStorage.getItem('authvault_likes') || '[]'));
    this.isFirebaseAvailable = false;

    // Initialize Application
    this.initFirebase();
    this.loadInitialDataset();
    this.bindEvents();
    this.renderGallery();
    this.renderCreators();
  }

  /* --------------------------------------------------------------------------
     1. FIREBASE INITIALIZATION & FALLBACK
     -------------------------------------------------------------------------- */
  initFirebase() {
    try {
      // Firebase configuration (uses standard demo/public config or local fallback)
      const firebaseConfig = {
        apiKey: "AIzaSyAuthVaultPublicDemoConfigKey12345",
        authDomain: "authvault-gallery.firebaseapp.com",
        projectId: "authvault-gallery",
        storageBucket: "authvault-gallery.appspot.com",
        messagingSenderId: "1234567890",
        appId: "1:1234567890:web:abcdef123456"
      };

      if (typeof firebase !== 'undefined' && !firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
        this.db = firebase.firestore();
        this.isFirebaseAvailable = true;
        console.log("Firebase initialized successfully.");
      }
    } catch (e) {
      console.warn("Firebase running in offline/localStorage mode:", e);
      this.isFirebaseAvailable = false;
    }
  }

  /* --------------------------------------------------------------------------
     2. RICH DATASET GENERATOR
     -------------------------------------------------------------------------- */
  loadInitialDataset() {
    const baseDesigns = [
      {
        id: "design-1",
        title: "CyberPulse Cybernetic Portal Login",
        category: "dark",
        tech: "canvas",
        views: 14200,
        likes: 1280,
        publishedDate: "2 days ago",
        creator: {
          name: "Elena Rostova",
          avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "elena_ui"
        },
        tags: ["cyberpunk", "canvas", "dark-mode", "glowing", "futuristic"],
        description: "A dark cyberpunk authentication portal featuring animated grid lines, ambient plasma particle bursts, glowing cyan input borders, and smooth perspective tilt physics.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#0A0C16"/>
            <circle cx="200" cy="150" r="120" fill="url(#p1)" opacity="0.3"/>
            <rect x="100" y="50" width="200" height="200" rx="16" fill="#131728" stroke="#00F0FF" stroke-width="1.5" stroke-opacity="0.5"/>
            <rect x="120" y="110" width="160" height="32" rx="8" fill="#1C233D" stroke="#00F0FF" stroke-width="1"/>
            <rect x="120" y="152" width="160" height="32" rx="8" fill="#1C233D" stroke="#334155" stroke-width="1"/>
            <rect x="120" y="196" width="160" height="32" rx="16" fill="url(#p2)"/>
            <circle cx="200" cy="80" r="16" fill="#00F0FF" opacity="0.8"/>
            <defs>
              <radialGradient id="p1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(200 150) rotate(90) scale(120)">
                <stop stop-color="#00F0FF"/>
                <stop offset="1" stop-color="#0A0C16" stop-opacity="0"/>
              </radialGradient>
              <linearGradient id="p2" x1="120" y1="196" x2="280" y2="228" gradientUnits="userSpaceOnUse">
                <stop stop-color="#00F0FF"/>
                <stop offset="1" stop-color="#7000FF"/>
              </linearGradient>
            </defs>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #080B10;
      color: #FFF;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .card {
      background: rgba(16, 23, 42, 0.8);
      border: 1px solid rgba(0, 240, 255, 0.3);
      box-shadow: 0 0 30px rgba(0, 240, 255, 0.2);
      border-radius: 20px;
      padding: 40px;
      width: 360px;
      backdrop-filter: blur(10px);
      text-align: center;
      position: relative;
      z-index: 2;
    }
    .title { font-size: 22px; font-weight: 700; color: #00F0FF; margin-bottom: 6px; letter-spacing: 1px; }
    .sub { font-size: 13px; color: #94A3B8; margin-bottom: 24px; }
    .input-group { margin-bottom: 16px; text-align: left; }
    .input-group label { display: block; font-size: 11px; text-transform: uppercase; color: #64748B; margin-bottom: 6px; font-weight: 700; }
    .input-group input {
      width: 100%; padding: 12px 16px; background: #0F172A; border: 1px solid #334155; border-radius: 10px; color: #FFF; outline: none; transition: 0.3s;
    }
    .input-group input:focus { border-color: #00F0FF; box-shadow: 0 0 10px rgba(0, 240, 255, 0.4); }
    .btn {
      width: 100%; padding: 14px; background: linear-gradient(90deg, #00F0FF, #7000FF); border: none; border-radius: 10px; color: #FFF; font-weight: 700; cursor: pointer; margin-top: 10px; transition: transform 0.2s;
    }
    .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 240, 255, 0.4); }
  </style>
</head>
<body>
  <div class="card">
    <div class="title">CYBERVAULT</div>
    <div class="sub">Enter your security credentials to access system core</div>
    <form onsubmit="event.preventDefault(); alert('Access Granted to CyberVault!');">
      <div class="input-group">
        <label>Operator Identifier</label>
        <input type="text" placeholder="agent_007" required>
      </div>
      <div class="input-group">
        <label>Passcode Sequence</label>
        <input type="password" placeholder="••••••••••••" required>
      </div>
      <button class="btn">AUTHENTICATE</button>
    </form>
  </div>
</body>
</html>`
      },
      {
        id: "design-2",
        title: "Apex Glassmorphism Spatial Auth",
        category: "glassmorphic",
        tech: "html",
        views: 18900,
        likes: 2150,
        publishedDate: "1 day ago",
        creator: {
          name: "Marcus Vance",
          avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "marcus_design"
        },
        tags: ["glassmorphism", "blur", "spatial", "modern", "apple-inspired"],
        description: "VisionOS-inspired frosted glass login card with dynamic blurred light spots, floating input fields, and smooth gradient buttons.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#111827"/>
            <circle cx="120" cy="90" r="80" fill="#EA4C89" opacity="0.6"/>
            <circle cx="280" cy="210" r="90" fill="#3B82F6" opacity="0.5"/>
            <rect x="90" y="45" width="220" height="210" rx="20" fill="white" fill-opacity="0.1" stroke="white" stroke-opacity="0.3" style="backdrop-filter:blur(10px)"/>
            <rect x="115" y="110" width="170" height="30" rx="8" fill="white" fill-opacity="0.15"/>
            <rect x="115" y="150" width="170" height="30" rx="8" fill="white" fill-opacity="0.15"/>
            <rect x="115" y="195" width="170" height="32" rx="16" fill="#EA4C89"/>
            <circle cx="200" cy="80" r="14" fill="white" fill-opacity="0.8"/>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0F172A;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }
    .bg-glow-1 { position: absolute; width: 300px; height: 300px; background: #EA4C89; border-radius: 50%; filter: blur(90px); top: 10%; left: 20%; opacity: 0.6; }
    .bg-glow-2 { position: absolute; width: 350px; height: 350px; background: #3B82F6; border-radius: 50%; filter: blur(100px); bottom: 10%; right: 20%; opacity: 0.5; }
    .glass-card {
      position: relative;
      z-index: 10;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(20px);
      border-radius: 24px;
      padding: 40px 32px;
      width: 360px;
      color: white;
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    h2 { font-size: 24px; font-weight: 700; margin-bottom: 6px; }
    p { font-size: 13px; color: rgba(255,255,255,0.7); margin-bottom: 24px; }
    .input-box { margin-bottom: 16px; }
    .input-box input {
      width: 100%; padding: 12px 16px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; color: white; outline: none; font-size: 14px;
    }
    .input-box input::placeholder { color: rgba(255,255,255,0.5); }
    .input-box input:focus { border-color: #EA4C89; background: rgba(255, 255, 255, 0.15); }
    .submit-btn {
      width: 100%; padding: 14px; background: #EA4C89; border: none; border-radius: 12px; color: white; font-size: 15px; font-weight: 600; cursor: pointer; margin-top: 10px; transition: 0.2s;
    }
    .submit-btn:hover { background: #F06292; transform: translateY(-2px); }
  </style>
</head>
<body>
  <div class="bg-glow-1"></div>
  <div class="bg-glow-2"></div>
  <div class="glass-card">
    <h2>Welcome Back</h2>
    <p>Sign in to continue your spatial workspace session</p>
    <form onsubmit="event.preventDefault(); alert('Signed in successfully!');">
      <div class="input-box">
        <input type="email" placeholder="Email address" required>
      </div>
      <div class="input-box">
        <input type="password" placeholder="Password" required>
      </div>
      <button class="submit-btn">Sign In</button>
    </form>
  </div>
</body>
</html>`
      },
      {
        id: "design-3",
        title: "SaaS Dashboard Split Authentication",
        category: "saas",
        tech: "tailwind",
        views: 9800,
        likes: 890,
        publishedDate: "3 days ago",
        creator: {
          name: "Sophia Chen",
          avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "sophiachen"
        },
        tags: ["saas", "split-screen", "clean", "minimal", "enterprise"],
        description: "Professional 2-column SaaS authentication screen with customer review testimonial carousel, SSO Google login button, and high conversion form layout.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#F8F9FA"/>
            <rect width="200" height="300" fill="#0D0C22"/>
            <circle cx="100" cy="120" r="40" fill="#EA4C89" opacity="0.8"/>
            <rect x="230" y="60" width="140" height="24" rx="6" fill="#E5E7EB"/>
            <rect x="230" y="100" width="140" height="28" rx="6" fill="#FFFFFF" stroke="#D1D5DB"/>
            <rect x="230" y="140" width="140" height="28" rx="6" fill="#FFFFFF" stroke="#D1D5DB"/>
            <rect x="230" y="180" width="140" height="32" rx="6" fill="#0D0C22"/>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-4">
  <div class="max-w-4xl w-full bg-white rounded-2xl shadow-xl overflow-hidden grid grid-cols-1 md:grid-cols-2">
    <!-- Left Column (Branding & Testimonial) -->
    <div class="bg-slate-900 p-8 text-white flex flex-col justify-between relative overflow-hidden">
      <div class="absolute -bottom-10 -left-10 w-40 h-40 bg-pink-500 rounded-full blur-3xl opacity-30"></div>
      <div>
        <div class="text-xl font-bold tracking-tight text-pink-500 mb-2">AuthVault Cloud</div>
        <p class="text-slate-400 text-sm">Join over 40,000 teams building secure web applications.</p>
      </div>
      <div class="my-12">
        <blockquote class="text-lg font-medium text-slate-200">
          "This authentication UI cut our user onboarding drop-off rate by over 38% in the first month."
        </blockquote>
        <div class="mt-4 flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-pink-500 flex items-center justify-center font-bold">SC</div>
          <div>
            <div class="font-semibold text-sm">Sarah Connor</div>
            <div class="text-xs text-slate-400">Head of Product at Cyberdyne</div>
          </div>
        </div>
      </div>
      <div class="text-xs text-slate-500">&copy; 2026 AuthVault SaaS Inc.</div>
    </div>
    <!-- Right Column (Form) -->
    <div class="p-8 flex flex-col justify-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-1">Get Started Now</h2>
      <p class="text-sm text-gray-500 mb-6">Enter your email to sign in or create an account</p>
      <form onsubmit="event.preventDefault(); alert('Signed in!');" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Work Email</label>
          <input type="email" required placeholder="alex@company.com" class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-500 focus:border-pink-500 outline-none text-sm">
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-700 uppercase mb-1">Password</label>
          <input type="password" required placeholder="••••••••" class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-pink-500 focus:border-pink-500 outline-none text-sm">
        </div>
        <button class="w-full py-3 bg-slate-900 hover:bg-pink-600 text-white font-semibold rounded-lg text-sm transition">Sign In with Email</button>
      </form>
    </div>
  </div>
</body>
</html>`
      },
      {
        id: "design-4",
        title: "Liquid Morphing Organic Login",
        category: "animated",
        tech: "canvas",
        views: 12300,
        likes: 1540,
        publishedDate: "4 days ago",
        creator: {
          name: "Alex Rivera",
          avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "arivera"
        },
        tags: ["liquid", "canvas", "physics", "animation", "interactive"],
        description: "An interactive login screen featuring a physics-driven multi-node fluid spring canvas background with jelly deformation animations.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#0A0F1D"/>
            <path d="M0 180C100 140 200 220 300 160C350 130 380 180 400 170V300H0V180Z" fill="url(#liqGrad)" opacity="0.8"/>
            <rect x="110" y="60" width="180" height="180" rx="20" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.2)"/>
            <rect x="130" y="110" width="140" height="28" rx="8" fill="rgba(255,255,255,0.1)"/>
            <rect x="130" y="150" width="140" height="28" rx="8" fill="rgba(255,255,255,0.1)"/>
            <rect x="130" y="190" width="140" height="30" rx="15" fill="#00F0FF"/>
            <defs>
              <linearGradient id="liqGrad" x1="0" y1="140" x2="400" y2="300">
                <stop stop-color="#00F0FF"/>
                <stop offset="1" stop-color="#7000FF"/>
              </linearGradient>
            </defs>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #080C14; color: white; font-family: sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    canvas { position: absolute; inset: 0; pointer-events: none; }
    .card { position: relative; z-index: 10; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0,240,255,0.3); padding: 36px; border-radius: 20px; width: 340px; text-align: center; backdrop-filter: blur(12px); }
    h2 { font-size: 20px; color: #00F0FF; margin-bottom: 20px; }
    input { width: 100%; padding: 12px; margin-bottom: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: white; outline: none; }
    button { width: 100%; padding: 12px; background: #00F0FF; color: #080C14; border: none; font-weight: bold; border-radius: 10px; cursor: pointer; }
  </style>
</head>
<body>
  <canvas id="liquidCanvas"></canvas>
  <div class="card">
    <h2>LIQUID AUTH</h2>
    <input type="text" placeholder="Username">
    <input type="password" placeholder="Password">
    <button onclick="alert('Fluid Login Verified!')">LOG IN</button>
  </div>
  <script>
    const canvas = document.getElementById('liquidCanvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    resize(); window.onresize = resize;
    let t = 0;
    function draw() {
      ctx.clearRect(0,0,canvas.width,canvas.height);
      ctx.beginPath();
      ctx.moveTo(0, canvas.height/2);
      for(let x=0; x<=canvas.width; x+=10) {
        let y = canvas.height/2 + Math.sin(x*0.01 + t)*40 + Math.cos(x*0.005 + t*1.5)*30;
        ctx.lineTo(x, y);
      }
      ctx.lineTo(canvas.width, canvas.height);
      ctx.lineTo(0, canvas.height);
      ctx.fillStyle = 'rgba(0, 240, 255, 0.15)';
      ctx.fill();
      t += 0.03;
      requestAnimationFrame(draw);
    }
    draw();
  </script>
</body>
</html>`
      },
      {
        id: "design-5",
        title: "Minimalist Pastel OAuth Login",
        category: "minimal",
        tech: "html",
        views: 8200,
        likes: 710,
        publishedDate: "5 days ago",
        creator: {
          name: "Jessica Wu",
          avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "jessicawu"
        },
        tags: ["minimal", "pastel", "clean", "typography", "social-login"],
        description: "A soft minimalist login card featuring elegant typography, rounded input pills, and Google / Apple OAuth sign in buttons.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#FAF5FF"/>
            <rect x="110" y="50" width="180" height="200" rx="24" fill="#FFFFFF" box-shadow="0 10px 25px rgba(0,0,0,0.05)"/>
            <circle cx="200" cy="85" r="16" fill="#DDD6FE"/>
            <rect x="135" y="115" width="130" height="24" rx="12" fill="#F3E8FF"/>
            <rect x="135" y="145" width="130" height="24" rx="12" fill="#F3E8FF"/>
            <rect x="135" y="180" width="130" height="28" rx="14" fill="#7C3AED"/>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #FAF5FF; font-family: -apple-system, sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; }
    .card { background: white; padding: 40px 32px; border-radius: 28px; width: 340px; box-shadow: 0 10px 30px rgba(124, 58, 237, 0.08); text-align: center; }
    h1 { font-size: 22px; color: #2E1065; margin-bottom: 6px; font-weight: 800; }
    p { font-size: 13px; color: #7E22CE; margin-bottom: 24px; opacity: 0.8; }
    input { width: 100%; padding: 12px 18px; background: #F3E8FF; border: none; border-radius: 99px; margin-bottom: 12px; font-size: 13px; color: #2E1065; outline: none; }
    button { width: 100%; padding: 12px; background: #7C3AED; color: white; border: none; border-radius: 99px; font-weight: 700; cursor: pointer; transition: 0.2s; }
    button:hover { background: #6D28D9; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Hello Beautiful</h1>
    <p>Sign in to your design creative workspace</p>
    <form onsubmit="event.preventDefault(); alert('Logged in!');">
      <input type="email" placeholder="Your Email" required>
      <input type="password" placeholder="Your Password" required>
      <button>Continue</button>
    </form>
  </div>
</body>
</html>`
      },
      {
        id: "design-6",
        title: "Enterprise SSO Multi-Tenant Login",
        category: "enterprise",
        tech: "html",
        views: 11400,
        likes: 920,
        publishedDate: "6 days ago",
        creator: {
          name: "David K.",
          avatar: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "davidk_dev"
        },
        tags: ["enterprise", "sso", "saml", "okta", "security"],
        description: "Enterprise SAML/SSO multi-tenant authentication portal with domain auto-detection and security badge status indicators.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#0F172A"/>
            <rect x="100" y="50" width="200" height="200" rx="12" fill="#1E293B" stroke="#334155"/>
            <rect x="120" y="80" width="160" height="20" rx="4" fill="#334155"/>
            <rect x="120" y="115" width="160" height="30" rx="6" fill="#0F172A" stroke="#475569"/>
            <rect x="120" y="160" width="160" height="32" rx="6" fill="#2563EB"/>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0F172A; color: white; font-family: system-ui, sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; }
    .card { background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 36px; width: 360px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .badge { font-size: 11px; font-weight: 700; color: #38BDF8; background: rgba(56,189,248,0.1); padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 12px; }
    h2 { font-size: 20px; font-weight: 700; margin-bottom: 20px; }
    input { width: 100%; padding: 12px; background: #0F172A; border: 1px solid #475569; border-radius: 6px; color: white; margin-bottom: 16px; outline: none; }
    button { width: 100%; padding: 12px; background: #2563EB; border: none; border-radius: 6px; color: white; font-weight: 600; cursor: pointer; }
    button:hover { background: #1D4ED8; }
  </style>
</head>
<body>
  <div class="card">
    <span class="badge">SSO ENTERPRISE</span>
    <h2>Sign in with SSO</h2>
    <form onsubmit="event.preventDefault(); alert('Redirecting to SAML Provider...');">
      <input type="email" placeholder="name@company.com" required>
      <button>Continue with SSO</button>
    </form>
  </div>
</body>
</html>`
      },
      {
        id: "design-7",
        title: "Neon Cyberpunk Auth HUD",
        category: "gradient",
        tech: "html",
        views: 16500,
        likes: 1890,
        publishedDate: "1 week ago",
        creator: {
          name: "Elena Rostova",
          avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "elena_ui"
        },
        tags: ["neon", "cyberpunk", "gradient", "glowing", "hud"],
        description: "Electric neon gradient login HUD screen with glowing input outlines, laser grid effects, and futuristic status indicators.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#05050A"/>
            <rect x="90" y="45" width="220" height="210" rx="16" fill="#0D0D1A" stroke="url(#neonG)" stroke-width="2"/>
            <rect x="115" y="105" width="170" height="30" rx="6" fill="#14142B" stroke="#FF007A"/>
            <rect x="115" y="145" width="170" height="30" rx="6" fill="#14142B" stroke="#00F0FF"/>
            <rect x="115" y="190" width="170" height="32" rx="16" fill="url(#neonG)"/>
            <defs>
              <linearGradient id="neonG" x1="0" y1="0" x2="1" y2="1">
                <stop stop-color="#FF007A"/>
                <stop offset="1" stop-color="#00F0FF"/>
              </linearGradient>
            </defs>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #05050A; color: white; font-family: monospace; height: 100vh; display: flex; align-items: center; justify-content: center; }
    .card { background: #0D0D1A; border: 2px solid; border-image: linear-gradient(135deg, #FF007A, #00F0FF) 1; padding: 36px; width: 340px; text-align: center; box-shadow: 0 0 30px rgba(255, 0, 122, 0.3); }
    h2 { font-size: 20px; background: linear-gradient(90deg, #FF007A, #00F0FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
    input { width: 100%; padding: 12px; margin-bottom: 12px; background: #14142B; border: 1px solid #FF007A; color: white; outline: none; font-family: monospace; }
    button { width: 100%; padding: 12px; background: linear-gradient(90deg, #FF007A, #00F0FF); border: none; color: white; font-weight: bold; cursor: pointer; font-family: monospace; }
  </style>
</head>
<body>
  <div class="card">
    <h2>[ SYSTEM LOGIN ]</h2>
    <input type="text" placeholder="USER_ID">
    <input type="password" placeholder="PASSKEY">
    <button onclick="alert('ACCESS GRANTED')">INITIALIZE</button>
  </div>
</body>
</html>`
      },
      {
        id: "design-8",
        title: "Mobile Native Bio-Auth Screen",
        category: "mobile",
        tech: "html",
        views: 7400,
        likes: 680,
        publishedDate: "1 week ago",
        creator: {
          name: "Marcus Vance",
          avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
          badge: "PRO",
          username: "marcus_design"
        },
        tags: ["mobile", "face-id", "biometric", "app", "clean"],
        description: "Mobile app biometric Face ID login screen with animated scanner ring and numerical passcode fallback keyboard.",
        thumbnailSvg: `
          <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#F1F5F9"/>
            <rect x="140" y="30" width="120" height="240" rx="20" fill="#0F172A"/>
            <circle cx="200" cy="110" r="24" stroke="#38BDF8" stroke-width="2" stroke-dasharray="4 4"/>
            <rect x="160" y="160" width="80" height="10" rx="5" fill="#334155"/>
            <rect x="160" y="180" width="80" height="10" rx="5" fill="#334155"/>
            <rect x="160" y="200" width="80" height="20" rx="10" fill="#38BDF8"/>
          </svg>
        `,
        code: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #F1F5F9; font-family: -apple-system, sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; }
    .phone { background: #0F172A; border-radius: 36px; padding: 28px 20px; width: 280px; height: 500px; color: white; display: flex; flex-direction: column; align-items: center; justify-content: space-between; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
    .face-icon { width: 70px; height: 70px; border: 2px stroke #38BDF8; border-radius: 50%; border: 2px dashed #38BDF8; display: flex; align-items: center; justify-content: center; font-size: 28px; margin-top: 40px; }
    .btn { width: 100%; padding: 14px; background: #38BDF8; color: #0F172A; border: none; border-radius: 99px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>
  <div class="phone">
    <div style="text-align: center; margin-top: 20px;">
      <h3 style="font-size: 18px;">Face ID</h3>
      <p style="font-size: 12px; color: #94A3B8;">Scan face to authenticate</p>
    </div>
    <div class="face-icon">👤</div>
    <button class="btn" onclick="alert('Face ID Authenticated!')">Log In with Passcode</button>
  </div>
</body>
</html>`
      }
    ];

    // Read stored community uploads from localStorage to prepend dynamically
    const communityUploads = JSON.parse(localStorage.getItem('authvault_uploads') || '[]');

    this.designs = [...communityUploads, ...baseDesigns];
    this.filteredDesigns = [...this.designs];
  }

  /* --------------------------------------------------------------------------
     3. EVENT BINDINGS
     -------------------------------------------------------------------------- */
  bindEvents() {
    // Search bindings
    const globalSearch = document.getElementById('global-search-input');
    const mobileSearch = document.getElementById('mobile-search-input');
    const clearSearch = document.getElementById('clear-search-btn');

    if (globalSearch) {
      globalSearch.addEventListener('input', (e) => {
        this.searchQuery = e.target.value;
        if (clearSearch) clearSearch.classList.toggle('hidden', !this.searchQuery);
        this.applyFilters();
      });
    }

    if (mobileSearch) {
      mobileSearch.addEventListener('input', (e) => {
        this.searchQuery = e.target.value;
        this.applyFilters();
      });
    }

    if (clearSearch) {
      clearSearch.addEventListener('click', () => {
        this.searchQuery = '';
        if (globalSearch) globalSearch.value = '';
        clearSearch.classList.add('hidden');
        this.applyFilters();
      });
    }

    // Keyboard Shortcut (Cmd+K / Ctrl+K)
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (globalSearch) globalSearch.focus();
      } else if (e.key === 'Escape') {
        this.closeAllModals();
      }
    });

    // Category Pills Scroll
    const catContainer = document.getElementById('category-pills');
    const scrollLeft = document.getElementById('cat-scroll-left');
    const scrollRight = document.getElementById('cat-scroll-right');

    if (catContainer) {
      catContainer.addEventListener('click', (e) => {
        const pill = e.target.closest('.pill-btn');
        if (pill) {
          document.querySelectorAll('.pill-btn').forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          this.activeCategory = pill.dataset.category || 'all';
          this.applyFilters();
        }
      });
    }

    if (scrollLeft && catContainer) {
      scrollLeft.addEventListener('click', () => catContainer.scrollBy({ left: -200, behavior: 'smooth' }));
    }
    if (scrollRight && catContainer) {
      scrollRight.addEventListener('click', () => catContainer.scrollBy({ left: 200, behavior: 'smooth' }));
    }

    // Dropdown Select Filters
    const sortSelect = document.getElementById('sort-select');
    const techSelect = document.getElementById('tech-select');

    if (sortSelect) {
      sortSelect.addEventListener('change', (e) => {
        this.activeSort = e.target.value;
        this.applyFilters();
      });
    }

    if (techSelect) {
      techSelect.addEventListener('change', (e) => {
        this.activeTech = e.target.value;
        this.applyFilters();
      });
    }

    // Grid View Toggle
    const btnLarge = document.getElementById('view-grid-large');
    const btnCompact = document.getElementById('view-grid-compact');
    const galleryGrid = document.getElementById('gallery-grid');

    if (btnLarge && btnCompact && galleryGrid) {
      btnLarge.addEventListener('click', () => {
        btnLarge.classList.add('active');
        btnCompact.classList.remove('active');
        galleryGrid.classList.remove('compact-view');
      });
      btnCompact.addEventListener('click', () => {
        btnCompact.classList.add('active');
        btnLarge.classList.remove('active');
        galleryGrid.classList.add('compact-view');
      });
    }

    // Reset Filters button in Empty State
    const resetBtn = document.getElementById('reset-filters-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        this.searchQuery = '';
        this.activeCategory = 'all';
        this.activeTech = 'all';
        this.activeSort = 'popular';
        if (globalSearch) globalSearch.value = '';
        if (sortSelect) sortSelect.value = 'popular';
        if (techSelect) techSelect.value = 'all';
        document.querySelectorAll('.pill-btn').forEach(p => p.classList.toggle('active', p.dataset.category === 'all'));
        this.applyFilters();
      });
    }

    // Modal Triggers & Controls
    this.bindModalEvents();
  }

  /* --------------------------------------------------------------------------
     4. MODAL CONTROLLERS & SANDBOX ENGINE
     -------------------------------------------------------------------------- */
  bindModalEvents() {
    // Open Upload Modal
    const openUploadBtn = document.getElementById('open-upload-btn');
    const mUploadBtn = document.getElementById('m-upload-btn');
    const footerUploadLink = document.getElementById('footer-upload-link');
    const uploadModal = document.getElementById('upload-modal');
    const closeUploadBtn = document.getElementById('close-upload-modal-btn');
    const cancelUploadBtn = document.getElementById('cancel-upload-btn');

    const triggerUpload = () => {
      this.closeAllModals();
      if (uploadModal) uploadModal.classList.remove('hidden');
    };

    if (openUploadBtn) openUploadBtn.addEventListener('click', triggerUpload);
    if (mUploadBtn) mUploadBtn.addEventListener('click', triggerUpload);
    if (footerUploadLink) footerUploadLink.addEventListener('click', (e) => { e.preventDefault(); triggerUpload(); });
    if (closeUploadBtn) closeUploadBtn.addEventListener('click', () => uploadModal.classList.add('hidden'));
    if (cancelUploadBtn) cancelUploadBtn.addEventListener('click', () => uploadModal.classList.add('hidden'));

    // Upload Form Submit
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
      uploadForm.addEventListener('submit', (e) => this.handleUploadSubmit(e));
    }

    // Test Code Button in Upload Modal
    const testCodeBtn = document.getElementById('test-code-btn');
    if (testCodeBtn) {
      testCodeBtn.addEventListener('click', () => {
        const code = document.getElementById('upload-code').value;
        const title = document.getElementById('upload-design-title').value || "Test Upload Preview";
        if (!code) {
          this.showToast("Please enter HTML code before testing.", "info");
          return;
        }
        this.openPreviewModal({
          id: "temp-test",
          title: title,
          category: "saas",
          tech: "html",
          views: 1,
          likes: 0,
          publishedDate: "Just now",
          creator: { name: "You", avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80", badge: "MEMBER" },
          description: "Live test preview of your custom uploaded code snippet.",
          tags: ["test", "upload"],
          code: code
        });
      });
    }

    // Preview Modal Viewport Switches
    document.querySelectorAll('.vp-btn[data-viewport]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.vp-btn[data-viewport]').forEach(b => b.classList.remove('active'));
        const targetBtn = e.currentTarget;
        targetBtn.classList.add('active');
        const frame = document.getElementById('preview-device-frame');
        if (frame) {
          frame.style.width = targetBtn.dataset.viewport;
        }
      });
    });

    // Close Preview Modal
    const closePreviewBtn = document.getElementById('close-preview-modal-btn');
    const previewModal = document.getElementById('preview-modal');
    if (closePreviewBtn && previewModal) {
      closePreviewBtn.addEventListener('click', () => {
        previewModal.classList.add('hidden');
        // Clear iframe to halt scripts
        const iframe = document.getElementById('sandbox-iframe');
        if (iframe) iframe.srcdoc = '';
      });
    }

    // Modal Download Button
    const modalDownloadBtn = document.getElementById('modal-download-btn');
    if (modalDownloadBtn) {
      modalDownloadBtn.addEventListener('click', () => {
        if (this.currentPreviewDesign) {
          this.downloadDesignCode(this.currentPreviewDesign);
        }
      });
    }

    // Modal Like Button
    const modalLikeBtn = document.getElementById('modal-like-btn');
    if (modalLikeBtn) {
      modalLikeBtn.addEventListener('click', () => {
        if (this.currentPreviewDesign) {
          this.toggleLike(this.currentPreviewDesign.id);
        }
      });
    }

    // Open Creators Modal
    const navCreatorsBtn = document.getElementById('nav-creators-btn');
    const mCreatorsBtn = document.getElementById('m-creators-btn');
    const footerCreatorsLink = document.getElementById('footer-creators-link');
    const creatorsModal = document.getElementById('creators-modal');
    const closeCreatorsBtn = document.getElementById('close-creators-modal-btn');

    const triggerCreators = () => {
      this.closeAllModals();
      if (creatorsModal) creatorsModal.classList.remove('hidden');
    };

    if (navCreatorsBtn) navCreatorsBtn.addEventListener('click', triggerCreators);
    if (mCreatorsBtn) mCreatorsBtn.addEventListener('click', triggerCreators);
    if (footerCreatorsLink) footerCreatorsLink.addEventListener('click', (e) => { e.preventDefault(); triggerCreators(); });
    if (closeCreatorsBtn) closeCreatorsBtn.addEventListener('click', () => creatorsModal.classList.add('hidden'));

    // Auth Modal
    const authBtn = document.getElementById('auth-btn');
    const mAuthBtn = document.getElementById('m-auth-btn');
    const authModal = document.getElementById('auth-modal');
    const closeAuthBtn = document.getElementById('close-auth-modal-btn');

    const triggerAuth = () => {
      this.closeAllModals();
      if (authModal) authModal.classList.remove('hidden');
    };

    if (authBtn) authBtn.addEventListener('click', triggerAuth);
    if (mAuthBtn) mAuthBtn.addEventListener('click', triggerAuth);
    if (closeAuthBtn) closeAuthBtn.addEventListener('click', () => authModal.classList.add('hidden'));

    // Mobile Hamburger Toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileDrawer = document.getElementById('mobile-drawer');
    if (mobileMenuToggle && mobileDrawer) {
      mobileMenuToggle.addEventListener('click', () => {
        mobileDrawer.classList.toggle('hidden');
      });
    }
  }

  closeAllModals() {
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.add('hidden'));
    const mobileDrawer = document.getElementById('mobile-drawer');
    if (mobileDrawer) mobileDrawer.classList.add('hidden');
  }

  /* --------------------------------------------------------------------------
     5. FILTERING & SORTING ENGINE
     -------------------------------------------------------------------------- */
  applyFilters() {
    let result = [...this.designs];

    // Category Filter
    if (this.activeCategory !== 'all') {
      result = result.filter(d => d.category === this.activeCategory);
    }

    // Tech Filter
    if (this.activeTech !== 'all') {
      result = result.filter(d => d.tech === this.activeTech);
    }

    // Search Query Filter
    if (this.searchQuery.trim()) {
      const q = this.searchQuery.toLowerCase().trim();
      result = result.filter(d =>
        d.title.toLowerCase().includes(q) ||
        d.creator.name.toLowerCase().includes(q) ||
        d.description.toLowerCase().includes(q) ||
        d.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    // Sorting
    if (this.activeSort === 'popular') {
      result.sort((a, b) => (b.views + b.likes * 5) - (a.views + a.likes * 5));
    } else if (this.activeSort === 'latest') {
      result.sort((a, b) => b.id.localeCompare(a.id));
    } else if (this.activeSort === 'likes') {
      result.sort((a, b) => b.likes - a.likes);
    } else if (this.activeSort === 'title') {
      result.sort((a, b) => a.title.localeCompare(b.title));
    }

    this.filteredDesigns = result;
    this.renderGallery();
  }

  /* --------------------------------------------------------------------------
     6. RENDER GALLERY GRID & CARDS
     -------------------------------------------------------------------------- */
  renderGallery() {
    const grid = document.getElementById('gallery-grid');
    const emptyState = document.getElementById('empty-state');
    const resultsCount = document.getElementById('results-count');

    if (!grid) return;

    if (resultsCount) {
      resultsCount.textContent = `Showing ${this.filteredDesigns.length} design${this.filteredDesigns.length === 1 ? '' : 's'}`;
    }

    if (this.filteredDesigns.length === 0) {
      grid.innerHTML = '';
      if (emptyState) emptyState.classList.remove('hidden');
      return;
    }

    if (emptyState) emptyState.classList.add('hidden');

    grid.innerHTML = this.filteredDesigns.map(design => {
      const isLiked = this.userLikes.has(design.id);
      return `
        <article class="design-card" data-id="${design.id}">

          <!-- Thumbnail & Overlay -->
          <div class="card-thumbnail-wrapper" onclick="window.appInstance.openPreviewModalById('${design.id}')">
            ${design.thumbnailSvg ? design.thumbnailSvg : '<div class="card-thumbnail-preview"><i class="fa-solid fa-code"></i></div>'}

            <div class="card-overlay">
              <div class="overlay-top">
                <span class="card-category-badge">${design.category}</span>
                <div class="overlay-actions">
                  <button class="overlay-btn ${isLiked ? 'liked' : ''}" title="Like Design" onclick="event.stopPropagation(); window.appInstance.toggleLike('${design.id}')">
                    <i class="${isLiked ? 'fa-solid' : 'fa-regular'} fa-heart" style="${isLiked ? 'color: var(--primary-pink);' : ''}"></i>
                  </button>
                  <button class="overlay-btn" title="Download Code" onclick="event.stopPropagation(); window.appInstance.downloadDesignCodeById('${design.id}')">
                    <i class="fa-solid fa-download"></i>
                  </button>
                </div>
              </div>
              <div class="overlay-bottom">
                <h3 class="overlay-title">${this.escapeHtml(design.title)}</h3>
                <button class="overlay-live-btn">
                  <i class="fa-solid fa-play"></i> Live Run
                </button>
              </div>
            </div>
          </div>

          <!-- Card Metadata Footer -->
          <div class="card-info">
            <div class="card-creator">
              <img src="${design.creator.avatar}" alt="${design.creator.name}" class="creator-avatar" loading="lazy">
              <span class="creator-name">${this.escapeHtml(design.creator.name)}</span>
              ${design.creator.badge ? `<span class="creator-badge"><i class="fa-solid fa-circle-check"></i></span>` : ''}
            </div>

            <div class="card-stats">
              <div class="stat-group ${isLiked ? 'liked' : ''}" id="like-stat-${design.id}">
                <i class="${isLiked ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
                <span id="like-count-${design.id}">${design.likes}</span>
              </div>
              <div class="stat-group">
                <i class="fa-regular fa-eye"></i>
                <span>${this.formatNumber(design.views)}</span>
              </div>
            </div>
          </div>

        </article>
      `;
    }).join('');
  }

  /* --------------------------------------------------------------------------
     7. PREVIEW MODAL RENDERING & LIVE ISOLATED SANDBOX
     -------------------------------------------------------------------------- */
  openPreviewModalById(id) {
    const design = this.designs.find(d => d.id === id);
    if (design) {
      design.views += 1;
      this.openPreviewModal(design);
    }
  }

  openPreviewModal(design) {
    this.currentPreviewDesign = design;
    const modal = document.getElementById('preview-modal');
    if (!modal) return;

    // Set Meta
    document.getElementById('modal-creator-avatar').src = design.creator.avatar;
    document.getElementById('modal-creator-name').textContent = design.creator.name;
    document.getElementById('preview-title').textContent = design.title;
    document.getElementById('preview-description').textContent = design.description;
    document.getElementById('preview-tech').textContent = design.tech === 'canvas' ? 'HTML5 Canvas' : (design.tech === 'tailwind' ? 'Tailwind CSS' : 'Vanilla HTML/CSS/JS');
    document.getElementById('preview-category').textContent = design.category.toUpperCase();
    document.getElementById('preview-date').textContent = design.publishedDate;
    document.getElementById('preview-views').textContent = this.formatNumber(design.views);

    // Like State
    const isLiked = this.userLikes.has(design.id);
    const modalLikeBtn = document.getElementById('modal-like-btn');
    const modalLikeCount = document.getElementById('modal-like-count');
    if (modalLikeBtn && modalLikeCount) {
      modalLikeBtn.classList.toggle('liked', isLiked);
      modalLikeCount.textContent = design.likes;
    }

    // Render Tags
    const tagsContainer = document.getElementById('preview-tags');
    if (tagsContainer) {
      tagsContainer.innerHTML = design.tags.map(t => `<span class="tag-badge">#${t}</span>`).join('');
    }

    // Render Related Designs
    const relatedContainer = document.getElementById('related-designs-grid');
    if (relatedContainer) {
      const related = this.designs.filter(d => d.id !== design.id && (d.category === design.category || d.creator.name === design.creator.name)).slice(0, 4);
      relatedContainer.innerHTML = related.map(rel => `
        <div class="related-card" onclick="window.appInstance.openPreviewModalById('${rel.id}')">
          ${rel.thumbnailSvg}
        </div>
      `).join('');
    }

    // Inject Executable Code safely into Sandboxed Iframe
    const iframe = document.getElementById('sandbox-iframe');
    const loader = document.getElementById('sandbox-loader');

    if (loader) loader.style.opacity = '1';
    if (iframe) {
      // Use srcdoc for isolated safe execution
      iframe.srcdoc = design.code;
      iframe.onload = () => {
        if (loader) loader.style.opacity = '0';
      };
    }

    // Show Modal
    modal.classList.remove('hidden');
  }

  /* --------------------------------------------------------------------------
     8. LIKE SYSTEM & LOCALSTORAGE PERSISTENCE
     -------------------------------------------------------------------------- */
  toggleLike(id) {
    const design = this.designs.find(d => d.id === id);
    if (!design) return;

    if (this.userLikes.has(id)) {
      this.userLikes.delete(id);
      design.likes = Math.max(0, design.likes - 1);
      this.showToast(`Removed like from "${design.title}"`, "info");
    } else {
      this.userLikes.add(id);
      design.likes += 1;
      this.showToast(`Added like to "${design.title}"!`, "success");
    }

    // Sync localStorage
    localStorage.setItem('authvault_likes', JSON.stringify([...this.userLikes]));

    // Update UI elements dynamically
    const cardCount = document.getElementById(`like-count-${id}`);
    const cardGroup = document.getElementById(`like-stat-${id}`);
    if (cardCount) cardCount.textContent = design.likes;
    if (cardGroup) cardGroup.classList.toggle('liked', this.userLikes.has(id));

    if (this.currentPreviewDesign && this.currentPreviewDesign.id === id) {
      const modalLikeBtn = document.getElementById('modal-like-btn');
      const modalLikeCount = document.getElementById('modal-like-count');
      if (modalLikeBtn) modalLikeBtn.classList.toggle('liked', this.userLikes.has(id));
      if (modalLikeCount) modalLikeCount.textContent = design.likes;
    }

    // Sync to Firebase if available
    if (this.isFirebaseAvailable && this.db) {
      this.db.collection('designs').doc(id).update({
        likes: firebase.firestore.FieldValue.increment(this.userLikes.has(id) ? 1 : -1)
      }).catch(err => console.log("Firebase sync silent error:", err));
    }
  }

  /* --------------------------------------------------------------------------
     9. DOWNLOAD ACTION ENGINE
     -------------------------------------------------------------------------- */
  downloadDesignCodeById(id) {
    const design = this.designs.find(d => d.id === id);
    if (design) this.downloadDesignCode(design);
  }

  downloadDesignCode(design) {
    const blob = new Blob([design.code], { type: 'text/html;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const cleanFilename = design.title.toLowerCase().replace(/[^a-z0-0]/g, '-').replace(/-+/g, '-') + '-auth.html';

    link.setAttribute('href', url);
    link.setAttribute('download', cleanFilename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    this.showToast(`Downloaded "${cleanFilename}" successfully!`, "success");
  }

  /* --------------------------------------------------------------------------
     10. UPLOAD FORM SUBMISSION & FIREBASE PUBLISHING
     -------------------------------------------------------------------------- */
  handleUploadSubmit(e) {
    e.preventDefault();

    const title = document.getElementById('upload-design-title').value.trim();
    const creatorName = document.getElementById('upload-creator-name').value.trim();
    const category = document.getElementById('upload-category').value;
    const description = document.getElementById('upload-description').value.trim();
    const tagsInput = document.getElementById('upload-tags').value.trim();
    const code = document.getElementById('upload-code').value.trim();

    if (!title || !creatorName || !code) {
      this.showToast("Please fill in all required fields.", "info");
      return;
    }

    const tags = tagsInput ? tagsInput.split(',').map(t => t.trim()) : ['community', 'upload'];

    const newDesign = {
      id: "upload-" + Date.now(),
      title: title,
      category: category,
      tech: code.includes('tailwindcss') ? 'tailwind' : (code.includes('<canvas') ? 'canvas' : 'html'),
      views: 1,
      likes: 0,
      publishedDate: "Just now",
      creator: {
        name: creatorName,
        avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80",
        badge: "CREATOR",
        username: creatorName.toLowerCase().replace(/\s+/g, '')
      },
      tags: tags,
      description: description || "Community submitted login screen design.",
      thumbnailSvg: `
        <svg width="100%" height="100%" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="400" height="300" fill="#0D0C22"/>
          <rect x="90" y="50" width="220" height="200" rx="16" fill="#18181D" stroke="#EA4C89" stroke-width="1.5"/>
          <rect x="120" y="100" width="160" height="30" rx="6" fill="#272730"/>
          <rect x="120" y="140" width="160" height="30" rx="6" fill="#272730"/>
          <rect x="120" y="185" width="160" height="32" rx="16" fill="#EA4C89"/>
        </svg>
      `,
      code: code
    };

    // Save locally
    const existingUploads = JSON.parse(localStorage.getItem('authvault_uploads') || '[]');
    existingUploads.unshift(newDesign);
    localStorage.setItem('authvault_uploads', JSON.stringify(existingUploads));

    // Firebase publish if available
    if (this.isFirebaseAvailable && this.db) {
      this.db.collection('designs').doc(newDesign.id).set(newDesign)
        .then(() => console.log("Published to Firebase Firestore!"))
        .catch(err => console.log("Firebase publish error:", err));
    }

    // Prepend to current in-memory dataset
    this.designs.unshift(newDesign);
    this.applyFilters();

    // Reset Form & Close Modal
    document.getElementById('upload-form').reset();
    document.getElementById('upload-modal').classList.add('hidden');

    this.showToast(`Success! "${title}" has been published to the gallery!`, "success");
  }

  /* --------------------------------------------------------------------------
     11. CREATORS DIRECTORY RENDERER
     -------------------------------------------------------------------------- */
  renderCreators() {
    const grid = document.getElementById('creators-grid');
    if (!grid) return;

    // Aggregate creators from designs
    const creatorMap = new Map();
    this.designs.forEach(d => {
      if (!creatorMap.has(d.creator.name)) {
        creatorMap.set(d.creator.name, {
          ...d.creator,
          designsCount: 1,
          totalLikes: d.likes
        });
      } else {
        const item = creatorMap.get(d.creator.name);
        item.designsCount += 1;
        item.totalLikes += d.likes;
      }
    });

    const creators = Array.from(creatorMap.values());

    grid.innerHTML = creators.map(c => `
      <div class="creator-card-item" onclick="window.appInstance.filterByCreator('${this.escapeHtml(c.name)}')">
        <img src="${c.avatar}" alt="${c.name}" class="creator-avatar" style="width: 48px; height: 48px;">
        <div>
          <h4 style="font-size: 0.95rem; font-weight: 700;">${this.escapeHtml(c.name)} ${c.badge ? '<i class="fa-solid fa-circle-check text-accent" style="font-size:0.75rem;"></i>' : ''}</h4>
          <p style="font-size: 0.8rem; color: var(--text-secondary);">${c.designsCount} Designs • ${c.totalLikes} Likes</p>
        </div>
      </div>
    `).join('');
  }

  filterByCreator(creatorName) {
    this.closeAllModals();
    this.searchQuery = creatorName;
    const globalSearch = document.getElementById('global-search-input');
    if (globalSearch) globalSearch.value = creatorName;
    this.applyFilters();
  }

  /* --------------------------------------------------------------------------
     12. AUTHENTICATION & TOAST UTILITIES
     -------------------------------------------------------------------------- */
  handleSignIn() {
    this.closeAllModals();
    this.showToast("Signed in successfully! Welcome back.", "success");
  }

  showToast(message, type = "info") {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <i class="${type === 'success' ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-info'}"></i>
      <span>${this.escapeHtml(message)}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  formatNumber(num) {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k';
    }
    return num;
  }

  escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

// Global App Initialization
document.addEventListener('DOMContentLoaded', () => {
  window.appInstance = new AuthVaultApp();
});
