"use client";

import { ChangeEvent } from "react";

import { useRouter } from "next/navigation";

import { uploadCV } from "@/api/cv";

import { validateCV } from "@/validations/cv";

import { CVUploadProps } from "@/types/cv";

import { setErrorState } from "@/lib/api-error";

import { routes } from "@/routes/routes";

import { useContent } from "@/hooks/content";

import "@/styles/components/cv/_cv-upload.scss";

export default function CVUpload({
  onUploadComplete,
  onUploadStart,
  onUploadError,
}: CVUploadProps) {
  const router = useRouter();

  const { content, loading } = useContent();

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
        title: cv.uploadErrorTitle,
        message: cv.uploadErrorMessage,
      });

      router.push(routes.error);
    }
  };

  if (loading || !content) {
    return null;
  }

  const cv = content.cvpage;

  return (
    <main className="cv-upload" aria-labelledby="cv-upload-title">
      <h2 id="cv-upload-title">{cv.uploadTitle}</h2>

      <label htmlFor="cv-file" className="cv-upload-label">
        {cv.chooseFileLabel}
      </label>

      <div className="cv-file-picker">
        <div className="cv-file-picker-content">
          <span className="cv-file-picker-icon">✦</span>

          <div>
            <span className="cv-file-picker-title">{cv.uploadFileTitle}</span>

            <span className="cv-file-picker-hint">{cv.uploadFileHint}</span>
          </div>
        </div>

        <label htmlFor="cv-file" className="cv-file-picker-button">
          {cv.chooseFileButton}
        </label>

        <input
          id="cv-file"
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleUpload}
          className="cv-upload-input"
        />
      </div>
    </main>
  );
}
