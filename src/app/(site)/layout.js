import Footer from "@/components/Footer";

export default function SiteLayout({ children }) {
  return (
    <>
      {children}
      <Footer />
    </>
  );
}
