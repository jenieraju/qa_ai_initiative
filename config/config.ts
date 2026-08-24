import 'dotenv/config';

export type Environment = 'dev';

interface EnvironmentConfig {
  baseUrl: string;
}

const environments: Record<Environment, EnvironmentConfig> = {
  dev: {
    baseUrl: process.env.DEV_BASE_URL || 'https://web.dev.cofee.life',
  },
};

function resolveEnvironment(): Environment {
  const env = (process.env.TEST_ENV ?? 'dev') as Environment;
  if (!(env in environments)) {
    throw new Error(`Unknown TEST_ENV "${env}" — configured environments: ${Object.keys(environments).join(', ')}`);
  }
  return env;
}

export const config = {
  env: resolveEnvironment(),
  baseUrl: environments[resolveEnvironment()].baseUrl,
  timeouts: {
    actionMs: 10_000,
    navigationMs: 15_000,
    expectMs: 10_000,
  },
  auth: {
    testMobileNumberEnvVar: 'TEST_MOBILE_NUMBER',
    testOtpEnvVar: 'TEST_OTP',
  },
};
