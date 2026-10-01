import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

import { routes } from "@/routes/routes";

const publicRoutes = [
  routes.home,
  routes.login,
  routes.register,
  routes.cv,
  routes.profile,
  routes.jobs,
  routes.error,
];

for (const route of publicRoutes) {
  test(`accessibility: ${route}`, async ({ page }) => {
    await page.goto(`http://localhost:3000${route}`);

    await page.waitForLoadState("networkidle");

    const results = await new AxeBuilder({
      page,
    }).analyze();

    if (results.violations.length > 0) {
      console.log(
        JSON.stringify(
          results.violations.map((violation) => ({
            id: violation.id,
            impact: violation.impact,
            description: violation.description,
            nodes: violation.nodes.map((node) => ({
              html: node.html,
              target: node.target,
              failureSummary: node.failureSummary,
            })),
          })),
          null,
          2,
        ),
      );
    }

    expect(results.violations).toEqual([]);
  });
}
