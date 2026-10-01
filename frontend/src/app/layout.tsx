import type { Metadata } from "next";

import "@/styles/main.scss";

import Header from "./layout/Header";
import Footer from "./layout/Footer";
import Providers from "./providers";

export const metadata: Metadata = {
  title: "Job Matcher",
  description: "Find jobs that match your skills and experience.",
};

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

            <div className="app-content">{children}</div>

            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}
