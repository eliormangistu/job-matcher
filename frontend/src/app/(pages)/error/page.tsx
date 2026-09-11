// "use client";

// import { useEffect, useState } from "react";

// import ErrorState from "@/components/ErrorState";
// import { ErrorStateProps } from "@/types/base";

// import "@/styles/components/error/error-state.scss";

// export default function ErrorPage() {
//   const [error, setError] = useState<ErrorStateProps | null>(null);

//   useEffect(() => {
//     const storedError = sessionStorage.getItem("error_state");

//     if (!storedError) {
//       return;
//     }

//     setError(JSON.parse(storedError));
//   }, []);

//   if (!error) {
//     return null;
//   }

//   return <ErrorState title={error.title} message={error.message} />;
// }

"use client";

import ErrorState from "@/components/ErrorState";

export default function ErrorPage() {
  return (
    <ErrorState
      title="Could not load jobs"
      message="We couldn't load the jobs right now. Please try again later."
    />
  );
}
