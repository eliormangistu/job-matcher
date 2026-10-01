import { apiClient } from "./api-client";

import { getDeviceId } from "@/lib/device-id";
import { AuthData, LoginRequest, RegisterRequest } from "@/types/auth";
import { BaseResponse } from "@/types/base";

export function register(
  data: RegisterRequest,
): Promise<BaseResponse<AuthData>> {
  return apiClient<BaseResponse<AuthData>>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function login(
  data: Omit<LoginRequest, "device_id">,
): Promise<BaseResponse<AuthData>> {
  return apiClient<BaseResponse<AuthData>>("/auth/login", {
    method: "POST",
    body: JSON.stringify({
      ...data,
      device_id: getDeviceId(),
    }),
  });
}

export function googleLogin(
  credential: string,
): Promise<BaseResponse<AuthData>> {
  return apiClient<BaseResponse<AuthData>>("/auth/google_login", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${credential}`,
    },
  });
}

export function logout(): Promise<BaseResponse<null>> {
  return apiClient<BaseResponse<null>>("/auth/logout", {
    method: "POST",
  });
}
