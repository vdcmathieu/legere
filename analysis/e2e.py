"""End-to-end run of the questionnaire in headless Chromium.

Plays one respondent through every screen, checks for console errors,
horizontal overflow and dead ends, and saves screenshots.
Usage: python3 analysis/e2e.py <url> <outdir> [mobile] [dark]
"""
import random, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], Path(sys.argv[2])
mobile = "mobile" in sys.argv[3:]
dark = "dark" in sys.argv[3:]
persona = next((a.split("=")[1] for a in sys.argv[3:] if a.startswith("persona=")), None)
out.mkdir(parents=True, exist_ok=True)
tag = ("mobile" if mobile else "desktop") + ("-dark" if dark else "") + (f"-{persona}" if persona else "")
rnd = random.Random(7)
errors, notes = [], []


def shot(page, name):
    page.screenshot(path=str(out / f"{tag}-{name}.png"), full_page=True)


def overflow(page, where):
    w = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if w > 1:
        notes.append(f"horizontal overflow {w}px on {where}")


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1280, "height": 900},
                        color_scheme="dark" if dark else "light", device_scale_factor=1)
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(url); page.wait_for_timeout(600)
    shot(page, "01-home"); overflow(page, "home")
    page.click("#start")
    page.fill("#t-o1", "Le pouvoir d'achat et le coût du logement.")
    page.select_option("#o1area", "san")
    shot(page, "02-open")
    page.click("#next")
    # statements: lean slightly left-liberal-pro-EU persona with noise; test back + toggle
    n = 0
    while page.locator(".scale").count() and n < 90:
        if n == 0:
            shot(page, "03-statement"); overflow(page, "statement")
            page.click("summary") if page.locator("summary").count() else None
            shot(page, "03b-context")
        if n == 3:
            page.click("#back")
        if n == 5 and page.locator("#impt").count():
            page.click("#impt")
        btns = page.locator(".scale button")
        if persona:
            # answer as the persona candidate, with one-step noise 25% of the time
            cp = page.evaluate("(c) => { const id = st.current; const s = SBY[id] || RBY[id]; const base = SBY[id] ? id : RBY[id].reverses; const k = CANDS.find(x => x.id === c); const p = k.positions[base]; return p && p.p !== null && p.p !== undefined ? (SBY[id] ? p.p : -p.p) : null; }", persona)
            if cp is None:
                page.click("#na")
            else:
                v = max(-2, min(2, cp + (rnd.choice([-1, 1]) if rnd.random() < 0.25 else 0)))
                btns.nth(v + 2).click()
        elif rnd.random() < 0.06:
            page.click("#na")
        else:
            btns.nth(rnd.choice([0, 1, 1, 2, 3, 3, 4])).click()
        n += 1
        page.wait_for_timeout(30)
    notes.append(f"statements answered before stop screen: {n}")
    shot(page, "04-stop"); overflow(page, "stop")
    h2 = page.locator("h2").first.inner_text()
    notes.append(f"stop screen: {h2}")
    page.click("#on")
    # dilemmas
    for i in range(8):
        page.locator(".dilemma button").nth(rnd.randint(0, 1)).click()
        if i == 0:
            shot(page, "05-dilemma"); overflow(page, "dilemma")
        page.locator("[data-s]").nth(rnd.randint(0, 2)).click()
    page.click("#on")
    # importance
    page.click("#equal")
    shot(page, "06-importance"); overflow(page, "importance")
    page.click("#on")
    # leadership
    page.click("[data-m='g2'][data-s='probity']")
    for gid in ("g1", "g2w", "g3"):
        page.locator(f"[data-l='{gid}']").nth(rnd.randint(1, 4)).click()
    page.locator("[data-l='g2b']").nth(1).click()
    page.locator("[data-l='g4']").nth(2).click()
    page.locator("[data-l='g5']").nth(1).click()
    page.locator("[data-l='g6']").nth(2).click()
    shot(page, "07-leadership"); overflow(page, "leadership")
    if page.locator("#on").is_disabled():
        notes.append("BLOCKED: leadership continue disabled")
    page.click("#on")
    page.locator("[data-e]").nth(6).click()
    page.click("#on")
    page.wait_for_timeout(800)
    shot(page, "08-results"); overflow(page, "results")
    notes.append("results top rows: " + " | ".join(page.locator(".res-row .who b").all_inner_texts()[:4]))
    page.click("#nav-cands"); page.wait_for_timeout(300)
    shot(page, "09-fiche"); overflow(page, "fiche")
    page.click("#nav-method"); page.wait_for_timeout(300)
    shot(page, "10-method"); overflow(page, "method")
    page.reload(); page.wait_for_timeout(500)
    notes.append("after reload screen: " + page.locator("h1, h2").first.inner_text()[:80])
    b.close()

print(tag, "ERRORS:", errors or "none")
for n_ in notes:
    print(" -", n_)
