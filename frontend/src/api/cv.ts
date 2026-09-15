import { apiClient } from "./api-client";
import { BaseResponse } from "@/types/base";
import { CVUploadData } from "@/types/cv";

export function uploadCV(file: File): Promise<BaseResponse<CVUploadData>> {
  const token = localStorage.getItem("google_id_token");

  if (!token) {
    throw new Error("Authentication token is required");
  }

  const formData = new FormData();
  formData.append("file", file);

  return apiClient<BaseResponse<CVUploadData>>("/cv/upload_cv", {
    method: "POST",
    body: formData,
  });
}
