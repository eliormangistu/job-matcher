import { env as devEnv } from "./dev";
import { env as testEnv } from "./test";
import { env as prodEnv } from "./prod";

const environments = {
  development: devEnv,
  test: testEnv,
  production: prodEnv,
} as const;

export const ENV =
  environments[process.env.NODE_ENV as keyof typeof environments] ?? devEnv;
