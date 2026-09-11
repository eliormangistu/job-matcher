"use client";

import { ChangeEvent } from "react";
import { useRouter } from "next/navigation";

import { uploadCV } from "@/api/cv";
import { validateCV } from "@/validations/cv";
import { CVUploadProps } from "@/types/cv";
import { setErrorState } from "@/lib/api-error";
import { routes } from "@/routes/routes";

import "@/styles/components/cv/cv-upload.scss";

export default function CVUpload({
  onUploadComplete,
  onUploadStart,
  onUploadError,
}: CVUploadProps) {
  const router = useRouter();

  const handleUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    onUploadStart();

    try {
      validateCV(file);

      const response = await uploadCV(file);

      onUploadComplete(response.data);
    } catch (error) {
      console.error("CV upload failed:", error);

      onUploadError();

      setErrorState({
        title: "CV upload failed",
        message:
          "We couldn't process your CV right now. Please try again later.",
      });

      router.push(routes.error);
    }
  };

  return (
    <section className="cv-upload">
      <h1>Upload CV</h1>

      <input type="file" accept=".pdf,.doc,.docx" onChange={handleUpload} />
    </section>
  );
}
