import { CONFIG } from "@/config";
import { requestInterceptor, responseInterceptor } from "./interceptors";

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const isFormData = options.body instanceof FormData;

  const requestOptions = requestInterceptor(endpoint, {
    ...options,
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...options.headers,
    },
  });

  const response = await fetch(
    `${CONFIG.api.baseUrl}${endpoint}`,
    requestOptions,
  );

  const handledResponse = await responseInterceptor(response);

  return handledResponse.json();
}
