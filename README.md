# LoginScreen Community 🚀

An open-source, community-driven platform where developers and UI/UX designers can share, explore, preview in isolated sandboxes, and download custom login screen designs.

---

## 🌟 Key Features

1. **Modern Responsive Design**: Premium dark glassmorphic interface with CSS variables, mobile drawer navigation, smooth transitions, and layout accessibility.
2. **Interactive Explore Gallery**: Search designs by keywords, filter by category pills (*Glassmorphism*, *Minimal*, *Gradient & Animated*, *Cyberpunk*, *3D & Spatial*), and sort by *Newest* or *Popularity*.
3. **Sandboxed Live Preview System**:
   - Executes untrusted user HTML/CSS/JS inside a sandboxed iframe (`sandbox="allow-scripts"` without `allow-same-origin`).
   - Content Security Policy (CSP) headers restrict frame permissions to prevent token theft or unauthorized cross-origin requests.
   - Device frame switchers (*Desktop*, *Tablet*, *Mobile*).
4. **Creator Profiles & Submissions Dashboard**:
   - Public creator profile showcasing bio, total published designs, and download stats.
   - Personal dashboard with real-time submission approval badges (*Pending Review*, *Approved*, *Rejected*).
   - Profile bio editing.
5. **Client & Storage File Validation**:
   - Drag-and-drop file upload dropzone.
   - Validates package types (`.zip` max 10MB) and screenshots (`.png`, `.jpg`, `.webp` max 5MB).
6. **Admin Moderation Console**:
   - Inspect pending queue in real time.
   - Test sandboxed preview before approving or rejecting submissions.
   - Updating status immediately reflects across the live public gallery without requiring website redeployments.

---

## 🛠️ Technology Stack

- **Frontend**: Vanilla HTML5, CSS3 (Modern Glassmorphism Design System), JavaScript (ES Modules).
- **Backend Services**: Firebase v10 SDK (ESM).
- **Authentication**: Firebase Authentication (Email/Password).
- **Database**: Cloud Firestore.
- **Storage**: Firebase Storage.
- **Hosting**: Netlify / Static Web Server.

---

## 📁 File & Folder Structure

```
.
├── css/
│   └── main.css            # Dark glassmorphic design system & layout styles
├── js/
│   ├── firebase-config.js  # Firebase v10 ESM SDK initialization & fallback handler
│   ├── auth-service.js     # User authentication & Firestore user sync
│   ├── firestore-service.js# CRUD for designs, creators, & pending queues
│   ├── preview-sandbox.js # Secure iframe sandbox renderer & file validator
│   └── app-ui.js           # Navigation bar, auth modal & toast notification UI
├── index.html              # Landing home page with featured gallery & creators
├── explore.html            # Searchable & filterable design gallery
├── preview.html            # Live preview page with device switcher & sandbox iframe
├── upload.html             # User upload form with drag & drop validation
├── creators.html           # Public creators directory
├── profile.html            # Creator profile & submissions dashboard
├── admin.html              # Moderation console for approving/rejecting designs
├── env.example.js          # Example Firebase configuration template
└── README.md               # Project setup and deployment guide
```

---

## 🚀 Setup & Firebase Configuration

### 1. Firebase Console Setup
1. Go to [Firebase Console](https://console.firebase.google.com/) and create a new project.
2. Enable **Authentication** with Email/Password provider under `Build -> Authentication -> Sign-in method`.
3. Create a **Cloud Firestore Database** under `Build -> Firestore Database`.

#### Firestore Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
    match /designs/{designId} {
      allow read: if resource.data.status == 'approved' || request.auth != null;
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null;
    }
  }
}
```

4. Create a **Firebase Storage Bucket** under `Build -> Storage`.

#### Storage Security Rules
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /previews/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null && request.resource.size < 5 * 1024 * 1024;
    }
    match /packages/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null && request.resource.size < 10 * 1024 * 1024;
    }
  }
}
```

### 2. Local Environment Configuration
Create or update `env.js` or define `window.FIREBASE_CONFIG` in your web root:

```javascript
window.FIREBASE_CONFIG = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

---

## 🌐 Netlify Deployment

1. Connect your repository to [Netlify](https://www.netlify.com/).
2. Set Build Command to: `(Leave blank - static site)`
3. Set Publish Directory to: `.`
4. Click **Deploy Site**.

---

## 🛡️ Security Guidelines

- All uploaded preview HTML/CSS/JS is rendered inside an iframe configured with `sandbox="allow-scripts"` without `allow-same-origin`.
- Uploaded code cannot access parent window context, `localStorage`, `cookies`, or Firebase tokens.
- Server/Executable file types (`.exe`, `.sh`, `.php`, `.py`) are rejected on submission.
