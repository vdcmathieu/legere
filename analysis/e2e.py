"""End-to-end run of the questionnaire in headless Chromium.

Plays one respondent through every screen, checks for console errors,
horizontal overflow and dead ends, and saves screenshots.
Usage: python3 analysis/e2e.py <url> <outdir> [mobile] [dark] [persona=<cid>]
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


def shot(page, name, full=True):
    page.screenshot(path=str(out / f"{tag}-{name}.png"), full_page=full)


def overflow(page, where):
    w = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if w > 1:
        notes.append(f"horizontal overflow {w}px on {where}")


def answer_one(page, n):
    btns = page.locator(".opt[data-v]")
    if persona:
        cp = page.evaluate("(c) => { const id = st.current; const base = SBY[id] ? id : RBY[id].reverses; const k = CANDS.find(x => x.id === c); const p = k.positions[base]; return p && p.p !== null && p.p !== undefined ? (SBY[id] ? p.p : -p.p) : null; }", persona)
        if cp is None:
            page.click("#na")
        else:
            v = max(-2, min(2, cp + (rnd.choice([-1, 1]) if rnd.random() < 0.25 else 0)))
            btns.nth(v + 2).click()
    elif rnd.random() < 0.06:
        page.click("#na")
    else:
        btns.nth(rnd.choice([0, 1, 1, 2, 3, 3, 4])).click()


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 360, "height": 780} if mobile else {"width": 1280, "height": 900},
                        color_scheme="dark" if dark else "light", device_scale_factor=2 if mobile else 1,
                        has_touch=mobile, is_mobile=mobile)
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(url); page.wait_for_timeout(800)
    shot(page, "01-home"); overflow(page, "home")
    page.click("#start"); page.wait_for_timeout(300)
    # statements: one per screen until the checkpoint appears
    n = 0
    while page.locator(".opt[data-v]").count() and n < 90:
        if n == 0:
            shot(page, "02-statement", full=False); overflow(page, "statement")
            if page.locator(".term").count():
                page.locator(".term").first.click(); page.wait_for_timeout(250)
                shot(page, "02b-glossary", full=False); page.keyboard.press("Escape")
            if page.locator("#more").count():
                page.click("#more"); page.wait_for_timeout(250)
                shot(page, "02c-pour-contre", full=False); page.keyboard.press("Escape")
        if n == 3:
            page.click("#back"); page.wait_for_timeout(100)
        if n == 5 and page.locator("#impt").count():
            page.click("#impt")
        if n == 1:
            shot(page, "02d-statement-2", full=False)
        answer_one(page, n)
        n += 1
        page.wait_for_timeout(40)
    notes.append(f"statements answered before checkpoint: {n}")
    shot(page, "03-ready"); overflow(page, "ready")
    notes.append("checkpoint: " + page.locator("h1").first.inner_text())
    page.select_option("#expect", index=7)
    page.click("#on"); page.wait_for_timeout(900)
    shot(page, "04-results"); overflow(page, "results")
    notes.append("lead: " + page.locator(".lead .who").inner_text())
    notes.append("results top rows: " + " | ".join(page.locator(".res-row .who b").all_inner_texts()[:4]))
    # refine: dilemmas
    page.click("[data-go='dilemmas']"); page.wait_for_timeout(200)
    for i in range(8):
        page.locator("[data-k]").nth(rnd.randint(0, 1)).click(); page.wait_for_timeout(60)
        if i == 0:
            shot(page, "05-dilemma", full=False); overflow(page, "dilemma")
        page.locator("[data-s]").nth(rnd.randint(0, 2)).click(); page.wait_for_timeout(60)
    if page.locator(".lead").count() == 0:
        notes.append("BLOCKED: dilemmas did not return to results")
    # refine: priorities
    page.click("[data-go='importance']"); page.wait_for_timeout(200)
    page.locator("[data-a][data-l='2']").nth(2).click()
    page.locator("[data-a][data-l='0']").nth(5).click()
    shot(page, "06-priorities"); overflow(page, "priorities")
    page.click("#on"); page.wait_for_timeout(600)
    # refine: leadership
    page.click("[data-go='leadership']"); page.wait_for_timeout(200)
    steps = 0
    while page.locator(".lead").count() == 0 and steps < 12:
        if page.locator("[data-m]").count():
            page.click("[data-m='g2'][data-s='probity']"); page.wait_for_timeout(80)
            shot(page, "07-leadership-multi", full=False)
            page.click("#on")
        else:
            if steps == 0:
                shot(page, "07-leadership", full=False); overflow(page, "leadership")
            opts = page.locator("[data-l]")
            opts.nth(rnd.randint(1, opts.count() - 1)).click()
        steps += 1
        page.wait_for_timeout(120)
    if page.locator(".lead").count() == 0:
        notes.append("BLOCKED: leadership did not return to results")
    # refine: reflect
    page.click("[data-go='reflect']"); page.wait_for_timeout(200)
    page.fill("#t-o1", "Le pouvoir d'achat et le coût du logement.")
    page.select_option("#o1area", "san")
    shot(page, "08-reflect"); overflow(page, "reflect")
    page.click("#on"); page.wait_for_timeout(600)
    # refine: keep answering (retests appear here), then back to results
    if page.locator("[data-go='more']").count():
        page.click("[data-go='more']"); page.wait_for_timeout(200)
        for i in range(7):
            if not page.locator(".opt[data-v]").count():
                break
            if i == 0:
                shot(page, "09-refining", full=False)
            answer_one(page, 100 + i); page.wait_for_timeout(40)
        if page.locator("#to-results").count():
            page.click("#to-results"); page.wait_for_timeout(900)
    for d in page.locator("details.sec").all():
        d.evaluate("e => e.open = true")
    page.wait_for_timeout(300)
    shot(page, "10-results-full"); overflow(page, "results-full")
    notes.append("refine done flags: " + str(page.locator(".refine .done").count()))
    page.click("#nav-cands"); page.wait_for_timeout(300)
    shot(page, "11-fiche"); overflow(page, "fiche")
    page.click("#nav-method"); page.wait_for_timeout(300)
    shot(page, "12-method"); overflow(page, "method")
    page.reload(); page.wait_for_timeout(600)
    notes.append("after reload screen: " + page.locator("h1, h2").first.inner_text()[:80])
    page.click("#nav-home"); page.wait_for_timeout(200)
    page.click("#start"); page.wait_for_timeout(300)
    notes.append("start from home goes to: " + page.locator("h1, .lead").first.inner_text()[:60])
    b.close()

print(tag, "ERRORS:", errors or "none")
for n_ in notes:
    print(" -", n_)
