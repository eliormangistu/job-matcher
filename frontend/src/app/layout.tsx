import "@/styles/main.scss";

import Header from "./layout/Header";
import Footer from "./layout/Footer";
import Providers from "./providers";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="app-layout">
            <Header />

            <main className="app-content">{children}</main>

            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}
