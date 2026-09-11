import { apiClient } from "@/api/api-client";
import { BaseResponse } from "@/types/base";
import { Job, JobsResponse } from "@/types/job";

export function getJobs(
  limit: number = 20,
  offset: number = 0,
): Promise<BaseResponse<JobsResponse>> {
  return apiClient<BaseResponse<JobsResponse>>(
    `/jobs?limit=${limit}&offset=${offset}`,
  );
}

export function getJobById(id: number): Promise<BaseResponse<Job>> {
  return apiClient<BaseResponse<Job>>(`/jobs/${id}`);
}
