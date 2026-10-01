export interface Content {
  homepage: HomePageContent;
  jobspage: JobsPageContent;
  cvpage: CVPageContent;
  matchpage: MatchPageContent;
  errorpage: ErrorPageContent;
  loaderpage: LoaderPageContent;
  header: HeaderContent;
  footer: FooterContent;
  loginpage: LoginPageContent;
  registerpage: RegisterPageContent;
  profilepage: ProfilePageContent;
}

export interface ProfilePageContent {
  loadingText: string;

  profileEyebrow: string;
  welcomeText: string;
  subtitle: string;

  accountEyebrow: string;
  yourDetailsTitle: string;
  nameLabel: string;
  emailLabel: string;

  cvEyebrow: string;
  cvTitle: string;
  updateCVButton: string;
  uploadCVButton: string;
  noCVText: string;

  resultsEyebrow: string;
  matchedJobsTitle: string;
  matchesLabel: string;
  noMatchesTitle: string;
  noMatchesText: string;

  dangerZoneEyebrow: string;
  deleteAccountTitle: string;
  deleteAccountMessage: string;
  deleteAccountButton: string;

  deleteModalTitle: string;
  deleteModalMessage: string;
  deleteModalConfirm: string;
  deleteModalCancel: string;
}

export interface RegisterPageContent {
  title: string;
  nameLabel: string;
  emailLabel: string;
  passwordLabel: string;
  registerButton: string;
  loadingText: string;
  dividerText: string;
  loginPrompt: string;
  loginLink: string;
  registrationError: string;
}

export interface LoginPageContent {
  title: string;
  emailLabel: string;
  passwordLabel: string;
  loginButton: string;
  loadingText: string;
  dividerText: string;
  registerPrompt: string;
  registerLink: string;
  invalidCredentials: string;
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
  chooseFileLabel: string;
  uploadFileTitle: string;
  uploadFileHint: string;
  chooseFileButton: string;
  uploadErrorTitle: string;
  uploadErrorMessage: string;
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
