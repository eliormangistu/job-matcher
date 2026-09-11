export const routes = {
  home: "/",
  cv: "/cv",
  profile: "/profile",
  jobs: "/jobs",
  error: "/error",
  jobDetails: (id: number) => `/jobs/${id}`,
};
