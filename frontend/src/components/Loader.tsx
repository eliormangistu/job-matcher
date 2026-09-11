import "@/styles/shared/loader.scss";

interface LoaderProps {
  text?: string;
}

export default function Loader({ text = "Loading..." }: LoaderProps) {
  return (
    <div className="loader">
      <div className="loader-spinner" />
      <p>{text}</p>
    </div>
  );
}
