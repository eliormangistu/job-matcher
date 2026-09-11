import { ApiError } from "@/lib/api-error";

const AUTH_REQUIRED_ENDPOINTS = [
    "/cv/upload_cv",
  ];
  
  export function requestInterceptor(
    endpoint: string,
    options: RequestInit = {}
  ): RequestInit {
    const headers = new Headers(options.headers);
  
    if (AUTH_REQUIRED_ENDPOINTS.includes(endpoint)) {
      const token = localStorage.getItem("google_id_token");
  
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
    }
  
    return {
      ...options,
      headers,
    };
  }
  

export async function responseInterceptor(
  response: Response
): Promise<Response> {
  if (response.ok) {
    return response;
  }

  const errorResponse = await response.json();

  throw new ApiError(
    errorResponse.status_code,
    errorResponse.message
  );
}