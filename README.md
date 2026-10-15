# LoginScreen Community Platform

LoginScreen Community is a production-oriented login screen design-sharing gallery platform built with standard HTML5, CSS3, Vanilla JavaScript (ES modules), Express/Netlify serverless endpoints, and Firebase (Auth, Firestore, Storage).

## Features
- **Design Marketplace Gallery**: Responsive 4/2/1 column card grid showcasing curated login screen designs.
- **Search & Filters**: Real-time title/tag search, category filtering, and sorting.
- **Firebase Authentication**: Email/Password and Google OAuth authentication with user profiles.
- **Submission Workflow**: Upload design metadata, preview screenshot, and downloadable ZIP package (`pending` moderation queue).
- **Admin Moderation Portal**: Dynamic approval/rejection pipeline backed by serverless functions and Firebase Security Rules.
- **Safe Live Preview**: Sandboxed isolated `iframe` viewer preventing untrusted code from accessing application credentials or storage.
- **Direct ZIP Package Downloads**: Secure client download generator for login template files.

## Local Development & Testing

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your Firebase configuration keys:
   ```bash
   cp .env.example .env
   ```

3. **Start Development Server**:
   ```bash
   npm start
   ```
   Open `http://localhost:8080` in your browser.

4. **Run Automated Tests**:
   ```bash
   npm test
   ```

## Firebase & Netlify Setup Instructions

1. **Firebase Project**:
   - Create a project in [Firebase Console](https://console.firebase.google.com/).
   - Enable **Authentication** (Email/Password & Google Sign-In).
   - Enable **Cloud Firestore** and deploy rules from `firebase/firestore.rules`.
   - Enable **Firebase Storage** and deploy rules from `firebase/storage.rules`.

2. **Netlify Deployment**:
   - Connect repository to Netlify.
   - Configure Environment Variables in Netlify Settings matching `.env.example`.
   - Netlify will automatically discover `netlify.toml` and compile functions under `netlify/functions/`.
