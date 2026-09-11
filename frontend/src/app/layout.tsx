import "@/styles/main.scss";

import Header from "./layout/Header";
import Footer from "./layout/Footer";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Job Matcher | AI Jobs",
  description: "Find your next AI opportunity.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="app-layout">
          <Header />

          <main className="app-content">{children}</main>

          <Footer />
        </div>
      </body>
    </html>
  );
}
