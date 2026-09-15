import { apiClient } from "@/api/api-client";
import { BaseResponse } from "@/types/base";

import { Content } from "@/types/content";

export function getContent(): Promise<BaseResponse<Content>> {
  return apiClient<BaseResponse<Content>>("/content");
}
