import { ENV } from "@/env";

export const config = {
  api: {
    baseUrl: ENV.apiUrl,
  },

  cv: {
    maxFileSize: 5 * 1024 * 1024,

    allowedFileTypes: [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ],
    clientId: "",
  },
} as const;
