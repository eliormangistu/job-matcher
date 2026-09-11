import { config as devConfig } from "./dev";
import { config as testConfig } from "./test";
import { config as prodConfig } from "./prod";

const configs = {
  dev: devConfig,
  test: testConfig,
  prod: prodConfig,
} as const;

export const CONFIG =
  configs[process.env.APP_ENV as keyof typeof configs] ??
  devConfig;