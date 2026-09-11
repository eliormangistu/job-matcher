import { CONFIG } from "@/config/index";

export function validateCV(file: File): void {
  if (!file) {
    throw new Error("CV file is required");
  }

  if (!CONFIG.cv.allowedFileTypes.includes(file.type as never)) {
    throw new Error("Unsupported CV file type");
  }

  if (file.size > CONFIG.cv.maxFileSize) {
    throw new Error("CV file is too large");
  }
}
