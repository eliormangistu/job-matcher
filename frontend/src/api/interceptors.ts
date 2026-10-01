import { ApiError } from "@/lib/api-error";

export function requestInterceptor(
  endpoint: string,
  options: RequestInit = {},
): RequestInit {
  const headers = new Headers(options.headers);
  const method = (options.method ?? "GET").toUpperCase();

  const csrfToken = document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("csrf_token="))
    ?.split("=")[1];

  if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
    if (csrfToken) {
      headers.set("X-CSRF-Token", decodeURIComponent(csrfToken));
    }
  }

  return {
    ...options,
    credentials: "include",
    headers,
  };
}

export async function responseInterceptor(
  response: Response,
): Promise<Response> {
  if (response.ok) {
    return response;
  }

  let errorMessage = "Request failed";

  try {
    const errorResponse = await response.json();

    errorMessage = errorResponse.message ?? errorMessage;

    throw new ApiError(
      errorResponse.status_code ?? response.status,
      errorMessage,
    );
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(response.status, errorMessage);
  }
}
