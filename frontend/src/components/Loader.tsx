import "@/styles/shared/loader.scss";
import { LoaderProps } from "@/types/loader";

export default function Loader({ text = "Loading..." }: LoaderProps) {
  return (
    <div className="loader">
      <div className="loader-spinner" />
      <p>{text}</p>
    </div>
  );
}
