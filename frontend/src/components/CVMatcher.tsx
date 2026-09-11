"use client";

import { MatchResultsProps } from "@/types/match";

import MatchResults from "./MatchResults";

import "@/styles/components/cv/cv-matcher.scss";

export default function CVMatcher({ matches }: MatchResultsProps) {
  return <MatchResults matches={matches} />;
}
