// firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getDatabase } from 'firebase/database'; 

const firebaseConfig = {
  apiKey: "AIzaSyBaELhS9_inyH_KEFCam8tl1lfPVZY4eJY",
  authDomain: "healthcare-true.firebaseapp.com",
  projectId: "healthcare-true",
  storageBucket: "healthcare-true.appspot.com",
  messagingSenderId: "566023643216",
  appId: "1:566023643216:web:69b819955cf8724df2b155"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Export Realtime Database instance
export const database = getDatabase(app);