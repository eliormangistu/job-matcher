import { apiClient } from "./api-client";

import { BaseResponse } from "@/types/base";
import { UserData } from "@/types/user";

export function getCurrentUser(): Promise<BaseResponse<UserData>> {
  return apiClient<BaseResponse<UserData>>("/users/get_user");
}

export function deleteAccount(): Promise<BaseResponse<null>> {
  return apiClient<BaseResponse<null>>("/users/delete", {
    method: "DELETE",
  });
}
