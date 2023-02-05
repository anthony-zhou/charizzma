import Link from "next/link";
// import ProfileImage from './ProfileImage';
import logo from "../../assets/logo.svg";
import Image from "next/image";
import { useAuthState } from "react-firebase-hooks/auth";
import firebase from "@/lib/firebase/clientApp";
import SignedInWidget from "./widgets/SignedInWidget";
import SignedOutWidget from "./widgets/SignedOutWidget";

export default function Header() {
  const [user, loading, error] = useAuthState(firebase.auth);

  return (
    <div className="container mx-auto px-6 z-100">
      <div className="py-6">
        {/* <div className="flex flex-col justify-items-center content-center"> */}
        <div className=" inline-block">
          <Link href="/" className="text-white text-3xl">
            CHARIZZMA
            {/* <Image src={logo} alt="Snapnotes logo" height={35} /> */}
          </Link>
        </div>
        {user ? <SignedInWidget /> : <SignedOutWidget />}
        {/* </div> */}
      </div>
    </div>
  );
}
