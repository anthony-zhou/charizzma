// auth.tsx
import React from "react";
import StyledFirebaseAuth from "react-firebaseui/StyledFirebaseAuth";
import firebase from "@/lib/firebase/clientApp";
import { GoogleAuthProvider } from "firebase/auth";
import Link from "next/link";
import { doc, getDoc, setDoc } from "firebase/firestore";
import Head from "next/head";

const uiConfig: firebaseui.auth.Config = {
  signInSuccessUrl: "/",
  signInOptions: [GoogleAuthProvider.PROVIDER_ID],
  callbacks: {
    signInSuccessWithAuthResult: (authResult, redirectURL) => {
      const user = authResult.user;
      const docRef = doc(firebase.db, `users/${user.uid}`);
      getDoc(docRef).then((docSnap) => {
        if (!docSnap.exists()) {
          setDoc(docRef, {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL,
          }).then(() => {
            console.log("Document written with ID: ", docRef.id);
            window.location.href = redirectURL ?? "/";
          });
        } else {
          window.location.href = redirectURL ?? "/";
        }
      });

      return false;
    },
  },
};

function SignInScreen() {
  return (
    <div className="container mx-auto px-4">
      <Head>
        <title>sign in | charisma</title>
      </Head>
      <div className="flex flex-col items-center justify-center">
        <div className="bg-white shadow rounded lg:w-1/3 md:w-1/2 w-full p-10 mt-16">
          <p className="focus:outline-none text-2xl font-extrabold leading-6 text-gray-800">
            Log in to start creating
          </p>
          <p className="focus:outline-none text-sm mt-4 font-medium leading-none text-gray-500">
            Don&apos;t have an account?{" "}
            <Link
              href="/auth/signup"
              className="hover:text-gray-500 focus:text-gray-500 focus:outline-none focus:underline hover:underline text-sm font-medium leading-none  text-gray-800 cursor-pointer"
            >
              Sign up here
            </Link>
          </p>
          <div>
            <StyledFirebaseAuth
              uiConfig={uiConfig}
              firebaseAuth={firebase.auth}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignInScreen;
