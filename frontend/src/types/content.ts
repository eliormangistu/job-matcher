export interface Content {
  homepage: HomePageContent;
  jobspage: JobsPageContent;
  cvpage: CVPageContent;
  matchpage: MatchPageContent;
  errorpage: ErrorPageContent;
  loaderpage: LoaderPageContent;
  header: HeaderContent;
  footer: FooterContent;
}

export interface HomePageContent {
  title: string;
  subtitle: string;
  careerText: string;
  skillsText: string;
  description: string;
  opportunitiesText: string;
}

export interface JobsPageContent {
  title: string;
  onSite: string;
  remote: string;
  ofLabel: string;
  subtitle: string;
  pageLabel: string;
  closeLabel: string;
  fieldLabel: string;
  nextButton: string;
  loadingText: string;
  postedLabel: string;
  skillsTitle: string;
  yearsSuffix: string;
  locationLabel: string;
  viewJobButton: string;
  workModeLabel: string;
  aboutRoleTitle: string;
  containerTitle: string;
  previousButton: string;
  viewOriginalJob: string;
  yearsExperience: string;
  requirementsTitle: string;
  minExperienceLabel: string;
  locationNotSpecified: string;
}

export interface CVPageContent {
  title: string;
  subtitle: string;
  uploadTitle: string;
}

export interface MatchPageContent {
  title: string;
  noneText: string;
  subtitle: string;
  matchLabel: string;
  containerTitle: string;
  matchDescription: string;
  matchedSkillsTitle: string;
  missingSkillsTitle: string;
}

export interface ErrorPageContent {
  title: string;
  message: string;
  retryLabel: string;
}

export interface LoaderPageContent {
  loadingText: string;
  loadingTextJobs: string;
}

export interface ContentContextValue {
  content: Content | null;
  loading: boolean;
  error: boolean;
}

export interface HeaderContent {
  logo: string;
  home: string;
  jobs: string;
  cvMatcher: string;
}

export interface FooterContent {
  copyright: string;
}
