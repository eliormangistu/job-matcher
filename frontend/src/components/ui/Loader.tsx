import "@/styles/shared/_loader.scss";
import { LoaderProps } from "@/types/loader";

export default function Loader({ text = "Loading..." }: LoaderProps) {
  return (
    <div className="loader" role="status" aria-live="polite" aria-label={text}>
      <div className="loader-spinner" aria-hidden="true" />

      <p>{text}</p>
    </div>
  );
}
