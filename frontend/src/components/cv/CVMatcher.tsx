"use client";

import { MatchResultsProps } from "@/types/match";

import MatchResults from "@/components/matches/MatchResults";

export default function CVMatcher({ matches }: MatchResultsProps) {
  return <MatchResults matches={matches} />;
}
