"use client";

import { useContext } from "react";

import { ContentContext } from "@/context/ContentContext";
import { ContentContextValue } from "@/types/content";

export function useContent(): ContentContextValue {
  return useContext(ContentContext);
}
