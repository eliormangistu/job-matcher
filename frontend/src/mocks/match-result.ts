import { MatchResultsProps } from "@/types/match";

export const mockMatches: MatchResultsProps["matches"] = [
  {
    job_id: 863,
    score: 85.71,
    matched_skills: ["JavaScript", "Node.js", "React", "Vue.js", "PostgreSQL"],
    missing_skills: ["Communication", "Product mindset"],
    job: {
      id: 863,
      title: "Full Stack Software Engineer",
      company: "Unframe",
      location: ["Tel Aviv"],
      remote: false,
      description:
        "Unframe is an AI-first startup helping the world’s largest enterprises bring LLM-powered applications to life in days - not months.",
      url: "https://job-boards.eu.greenhouse.io/unframe/jobs/4955082101",
      field: "Software Engineering",
      company_industry: ["Technology"],
      min_experience: 5,
      requirements:
        "5+ years of hands-on software-engineering experience. Proven record of shipping real user-facing products end-to-end.",
      required_skills: [
        "JavaScript",
        "Node.js",
        "Vue.js",
        "React",
        "PostgreSQL",
        "Communication",
        "Product mindset",
      ],
      language_requirement: [],
      education_requirements: null,
      posted: "2026-08-18T00:00:00.000Z",
    },
  },

  {
    job_id: 1561,
    score: 83.33,
    matched_skills: ["JavaScript", "TypeScript"],
    missing_skills: ["Artificial Intelligence"],
    job: {
      id: 1561,
      title: "Junior Software Engineer",
      company: "Torii",
      location: ["Ra'anana"],
      remote: false,
      description:
        "We are hiring a Junior Software Engineer to join one of our core development teams for a 1-year temporary position.",
      url: "https://www.linkedin.com/jobs/view/4437110787/",
      field: "Software Engineering",
      company_industry: ["SaaS"],
      min_experience: null,
      requirements:
        "Computer Science graduate or related technical degree. Solid understanding and hands-on knowledge of JavaScript and TypeScript.",
      required_skills: ["JavaScript", "TypeScript", "Artificial Intelligence"],
      language_requirement: [],
      education_requirements: null,
      posted: "2026-07-05T00:00:00.000Z",
    },
  },

  {
    job_id: 1842,
    score: 83.33,
    matched_skills: [
      "JavaScript",
      "Node.js",
      "Microservices",
      "React",
      "MongoDB",
      "Distributed Systems",
    ],
    missing_skills: ["Linux", "Database programming", "Cloud computing"],
    job: {
      id: 1842,
      title: "Senior Full Stack Developer",
      company: "NVIDIA",
      location: ["Yokne'am"],
      remote: false,
      description:
        "We are looking for a senior full stack developer to join the manufacturing information systems team and help shape our data analysis solutions.",
      url: "https://nvidia.wd5.myworkdayjobs.com/",
      field: "Software Engineering",
      company_industry: ["Hardware", "Software", "AI", "Cloud"],
      min_experience: 5,
      requirements:
        "BSc in computer science or equivalent work experience. 5+ years of experience with all phases of the software development lifecycle.",
      required_skills: [
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "Linux",
        "Database programming",
        "Cloud computing",
        "Microservices",
        "Distributed systems",
      ],
      language_requirement: [],
      education_requirements: null,
      posted: "2026-07-28T00:00:00.000Z",
    },
  },
];
