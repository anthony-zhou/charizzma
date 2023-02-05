import Header from "../Header/Header";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="fixed top-0 left-0 w-full h-full bg-black z-50">
      <Header />
      <div className="pt-24">{children}</div>
    </div>
  );
}
