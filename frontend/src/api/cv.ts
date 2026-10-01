import { apiClient } from "./api-client";

import { BaseResponse } from "@/types/base";
import { CVResponse, CVUploadData } from "@/types/cv";
import { MatchResult } from "@/types/match";

export function uploadCV(file: File): Promise<BaseResponse<CVUploadData>> {
  const formData = new FormData();

  formData.append("file", file);

  return apiClient<BaseResponse<CVUploadData>>("/cv/upload_cv", {
    method: "POST",
    body: formData,
  });
}

export function getCV(): Promise<BaseResponse<CVResponse | null>> {
  return apiClient<BaseResponse<CVResponse | null>>("/cv/get_cv");
}

export function getCVMatches(): Promise<BaseResponse<MatchResult[]>> {
  return apiClient<BaseResponse<MatchResult[]>>("/cv/get_matches");
}
