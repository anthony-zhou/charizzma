import { Menu, Transition } from "@headlessui/react";
import ProfileImage from "../../ProfileImage";
import firebase from "@/lib/firebase/clientApp";
import { useRouter } from "next/router";

export default function SignedInWidget() {
  const router = useRouter();

  const signOut = () => {
    firebase.auth.signOut();
    // redirect to home page
    window.location.href = "/";
  };

  return (
    <div className="inline-block float-right">
      <Menu>
        <Menu.Button className="inline-flex w-full justify-center rounded-md px-4 py-2 text-sm font-medium text-white hover:bg-opacity-30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75">
          <ProfileImage
            src={firebase.auth.currentUser?.photoURL ?? ""}
            alt="Profile image"
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="#dddddd"
            className="ml-2 mt-2.5 h-5 w-5 text-gray-400"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M19.5 8.25l-7.5 7.5-7.5-7.5"
            />
          </svg>
        </Menu.Button>
        <Transition
          enter="transition duration-100 ease-out"
          enterFrom="transform scale-95 opacity-0"
          enterTo="transform scale-100 opacity-100"
          leave="transition duration-75 ease-out"
          leaveFrom="transform scale-100 opacity-100"
          leaveTo="transform scale-95 opacity-0"
        >
          <Menu.Items className="fixed">
            <Menu.Item>
              <button
                onClick={() => signOut()}
                className="whitespace-nowrap border border-t-0 group flex w-full items-center rounded-md px-3 py-2 text-sm bg-white text-black"
              >
                sign out
              </button>
            </Menu.Item>
          </Menu.Items>
        </Transition>
      </Menu>
    </div>
  );
}
