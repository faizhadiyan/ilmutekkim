import Header from "@/components/Header";
import ChatWidget from "@/components/ChatWidget";
import "./globals.css";
import "./chat.css";

const themeInit = "(function(){try{var t=localStorage.getItem(\"ilm-theme\");if(!t){t=window.matchMedia(\"(prefers-color-scheme: dark)\").matches?\"dark\":\"light\";}document.documentElement.setAttribute(\"data-theme\",t);}catch(e){document.documentElement.setAttribute(\"data-theme\",\"light\");}})();";

export const metadata = {
  title: {
    default: "ilmutekkim | Bikin Teknik Kimia Asik: Pabrik, Proses, Safety",
    template: "%s | ilmutekkim",
  },
  description: "Bedah proses teknik kimia dari pabriknya langsung: distilasi, kilang, sawit, semen, pulp, sampai safety. Ditulis insinyur kimia ITB.",
  alternates: {
    canonical: "https://ilmutekkim.vercel.app/",
  },
  openGraph: {
    type: "website",
    title: "ilmutekkim | Bikin Teknik Kimia Asik: Pabrik, Proses, Safety",
    description: "Bedah proses teknik kimia dari pabriknya langsung: distilasi, kilang, sawit, semen, pulp, sampai safety. Ditulis insinyur kimia ITB.",
    url: "https://ilmutekkim.vercel.app/",
  },
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23131518'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23F4F4F2' font-family='Arial' font-weight='bold'>IT</text></svg>",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="id" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
        <script dangerouslySetInnerHTML={{ __html: "window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments);};" }} />
        <script defer src="/_vercel/insights/script.js" />
      </head>
      <body>
        <Header />
        {children}
        <ChatWidget />
      </body>
    </html>
  );
}
