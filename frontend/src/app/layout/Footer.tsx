import Image from "next/image";

import "@/styles/layout/footer.scss";

export default function Footer() {
  return (
    <footer className="site-footer">
      <p>
        © 2026 Job Matcher
        <Image src="/icon.svg" alt="" width={24} height={24} />
      </p>
    </footer>
  );
}
