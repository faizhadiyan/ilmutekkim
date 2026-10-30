import "./kamus.css";

export default function KamusLayout({ children }) {
  return (
    <>
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link
        rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Noto+Sans:wght@400;600;700&display=swap"
        precedence="default"
      />
      {children}
    </>
  );
}
