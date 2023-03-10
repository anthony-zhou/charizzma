import Head from "next/head";
import Image from "next/image";
import { useAuthState } from "react-firebase-hooks/auth";
import firebase from "@/lib/firebase/clientApp";
import Link from "next/link";
import { useEffect, useState } from "react";
import {
  addDoc,
  collection,
  doc,
  DocumentData,
  DocumentReference,
  getFirestore,
  onSnapshot,
  serverTimestamp,
  updateDoc,
} from "firebase/firestore";
import Layout from "@/components/Layout";

const sampleTranscript = `
Isn’t this incredible that we are both vegan?  I can’t believe we have actually gone vegan.
Babe, please.  I’m starving.
Oh, come on.  Just have some more salad.
Charizzma: I’m not hungry.
Salad?
Yeah, you need to eat more plant foods, vegetables and fruits.
I’m starving babe, alright?  I feel like I’ve been eating leaves all day.
Charizzma: That's fantastic that you're eating more plant foods.
Frances, stop it.  It’s only been three days.
Three days? That’s all?
Yep.
Hasn’t it been a week already?  I feel like I’m breaking some sort of record.
Well, I’m proud of you.  You are going to live a longer life.
(under his breath)  In misery…
What?
I gotta tell ya, I’m ready to grab my bow and arrow and shoot down birds in the backyard.
That’s horrible.  Tell me you’re joking.
I’m hungry!  Been eating salad that don’t even look like salad.  It’s leaves.
It’s baby spinach!
`;

export default function Home() {
  const [user, loading] = useAuthState(firebase.auth);

  const [conversationState, setConversationState] = useState<
    "initial" | "ongoing" | "finished"
  >("initial");

  const [transcript, setTranscript] = useState("");

  const [conversationRef, setConversationRef] =
    useState<DocumentReference<DocumentData> | null>(null);

  useEffect(() => {
    if (!conversationRef) return;
    const unsubscribe = onSnapshot(conversationRef, (querySnapshot) => {
      const docData = querySnapshot.data();
      if (docData) setTranscript(docData["full_transcript"]);
    });
    return unsubscribe;
  }, [conversationRef]);

  if (loading) {
    return <></>;
  } else if (!user) {
    return (
      <Layout>
        <Head>
          <title>home | charizzma</title>
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <div className="container mx-auto pt-6 pb-28 md:px-36 px-6 text-center">
          <h1 className="text-5xl">up your conversation game</h1>
          <div className="pt-10 text-white">
            Please{" "}
            <Link href="/auth/signin" className="underline text-pink-400">
              sign in
            </Link>{" "}
            to start using Charisma.{" "}
          </div>
        </div>
      </Layout>
    );
  }

  const startConversation = async () => {
    // TODO: start conversation in firebase
    const conversations = collection(getFirestore(), "conversations");
    const conversationRef = await addDoc(conversations, {
      active: true,
      start_time: serverTimestamp(),
      created_by: user.uid,
    });
    setConversationState("ongoing");
    setConversationRef(conversationRef);
  };

  const highlightCharizzma = (text: string[]) => {
    for (let i = 0; i < text.length; i++) {
      if (text[i].startsWith("Charizzma: ")) {
        text[i] = '<span class="text-pink-400">' + text[i] + "</span>";
      }
    }

    return { __html: text.join("\n") };
  };

  return (
    <Layout>
      <Head>
        <title>home | charizzma</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="container mx-auto pt-6 pb-28 md:px-36 px-6 text-center">
        <h1 className="text-5xl">up your conversation game</h1>
        <div className="pt-10">
          {conversationState === "initial" && (
            <button
              className="button primary text-2xl text-white-700 bg-pink-400 rounded-xl px-10 py-4 hover:bg-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-600 focus:ring-opacity-50"
              onClick={startConversation}
            >
              Start conversation
            </button>
          )}
          {conversationState === "ongoing" && transcript && (
            <div className="text-left">
              <p
                className="whitespace-pre-line"
                dangerouslySetInnerHTML={highlightCharizzma(
                  transcript.split("\n")
                )}
              ></p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
