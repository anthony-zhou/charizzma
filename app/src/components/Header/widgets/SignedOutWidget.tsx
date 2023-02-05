import Link from "next/link";

export default function SignedOutWidget() {
  return (
    <div className="inline-block float-right">
      <Link
        href="/auth/signup"
        className="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Sign in
      </Link>
    </div>
  );
}
