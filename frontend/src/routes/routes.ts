export const routes = {
  home: "/",
  login: "/login",
  register: "/register",
  cv: "/cv",
  profile: "/profile",
  jobs: "/jobs",
  error: "/error",
  jobDetails: (id: number) => `/jobs/${id}`,
};
