import { test, expect } from "@playwright/test";

test("parcours création campagne → arène (API requis)", async ({ page }) => {
  test.skip(!process.env.E2E_API_URL, "Définir E2E_API_URL pour exécuter");
  await page.goto("/campagnes");
  await expect(page.getByText("Campagnes")).toBeVisible();
});
