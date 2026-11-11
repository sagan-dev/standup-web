#!/usr/bin/env python3
"""Generates the static pages (EN + PL) of standup.sagan.dev. Run: python3 tools/build.py"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://standup.sagan.dev"
GITHUB = "https://github.com/sagan-dev/Standup"
MAIL = "michal@sagan.dev"
ASSET_V = "3"
# Mac App Store listing (verified via iTunes Lookup: trackId 6817507284, bundleId dev.sagan.Standup)
APP_STORE = {
    "en": "https://apps.apple.com/us/app/standup-desk-remote-control/id6817507284?mt=12",
    "pl": "https://apps.apple.com/pl/app/standup-desk-remote-control/id6817507284?mt=12",
}

T = {
 "en": {
  "code": "en", "prefix": "", "other": "pl", "otherlabel": "PL",
  "nav": {"features": "Features", "privacy": "Privacy", "support": "Support"},
  "name": "Standup - Desk Remote Control",
  "tagline": "Your sit/stand desk, one click away in the menu bar — and it stands up before your meetings.",
  "appstore": "Download on the Mac App Store",
  "opensrc": "Open-source edition",
  "footer_made": "Made by <a href=\"https://sagan.dev\">Michal Sagan</a> · <a href=\"https://sagan.dev\">sagan.dev</a>",
  "footer_disc": "Standup is an independent app and is not affiliated with, endorsed by or sponsored by IKEA or Linak. Product names are used only to describe compatibility.",
  "meta_home": "Standup - Desk Remote Control: a native macOS menu bar app for Bluetooth sit/stand desks. Raises your desk before online meetings.",
  "meta_privacy": "Privacy policy of Standup - Desk Remote Control. The app collects no personal data.",
  "meta_support": "Support and FAQ for Standup - Desk Remote Control: pairing, calendar access, meetings, AppleScript.",
 },
 "pl": {
  "code": "pl", "prefix": "/pl", "other": "en", "otherlabel": "EN",
  "nav": {"features": "Funkcje", "privacy": "Prywatność", "support": "Wsparcie"},
  "name": "Standup - Desk Remote Control",
  "tagline": "Twoje biurko z regulacją wysokości pod ręką w pasku menu — i samo wstaje przed Twoimi spotkaniami.",
  "appstore": "Pobierz w Mac App Store",
  "opensrc": "Wersja open source",
  "footer_made": "Stworzone przez <a href=\"https://sagan.dev\">Michała Sagana</a> · <a href=\"https://sagan.dev\">sagan.dev</a>",
  "footer_disc": "Standup jest niezależną aplikacją i nie jest powiązany z firmami IKEA ani Linak, ani przez nie wspierany czy sponsorowany. Nazwy produktów służą wyłącznie do opisu zgodności.",
  "meta_home": "Standup - Desk Remote Control: natywna aplikacja macOS w pasku menu do biurek z regulacją wysokości na Bluetooth. Podnosi biurko przed spotkaniami online.",
  "meta_privacy": "Polityka prywatności aplikacji Standup - Desk Remote Control. Aplikacja nie zbiera żadnych danych osobowych.",
  "meta_support": "Wsparcie i FAQ aplikacji Standup - Desk Remote Control: parowanie, dostęp do kalendarza, spotkania, AppleScript.",
 },
}

def url(lang, path):
    p = T[lang]["prefix"] + path
    return p if p else "/"

def layout(lang, path, title, desc, body, page_class=""):
    t = T[lang]
    canon = BASE + url(lang, path)
    alt_lang = t["other"]
    alt = BASE + url(alt_lang, path)
    en_url = BASE + url("en", path)
    pl_url = BASE + url("pl", path)
    nav = t["nav"]
    home = url(lang, "/")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="pl" href="{pl_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/icon.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#1f6bff">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css?v={ASSET_V}">
</head>
<body class="{page_class}">
<header class="site"><div class="wrap">
  <a class="brand" href="{home}"><img src="/assets/icon.png" width="28" height="28" alt=""><span>Standup</span></a>
  <nav class="main" aria-label="Main">
    <a class="hide-sm" href="{url(lang, '/')}#features">{nav['features']}</a>
    <a href="{url(lang, '/privacy')}">{nav['privacy']}</a>
    <a href="{url(lang, '/support')}">{nav['support']}</a>
    <a class="lang" href="{alt}" hreflang="{alt_lang}" lang="{alt_lang}">{t['otherlabel']}</a>
  </nav>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap">
  <div>{t['footer_made']}</div>
  <div><a href="{url(lang, '/privacy')}">{nav['privacy']}</a> · <a href="{url(lang, '/support')}">{nav['support']}</a> · <a href="{GITHUB}">{t['opensrc']}</a></div>
  <div style="flex-basis:100%;font-size:13px">{t['footer_disc']}</div>
</div></footer>
</body>
</html>
"""

# ------------------------------------------------------------------ landing
FEATURES = {
 "en": [
  ("Menu bar popover", "Height, connection status and desk name at a glance. It lives in the menu bar — no Dock icon, no extra windows.", ""),
  ("Hold to move", "Hold the round raise or lower button and the desk keeps moving; let go and it stops. It never runs away.", ""),
  ("Stand and Sit presets", "One click sends the desk to your saved standing or sitting height and stops there. Click again to stop on the way.", ""),
  ("Stands up before meetings", "Standup reads your Apple Calendar — including Outlook, Exchange and Microsoft 365 accounts added to macOS — and raises the desk shortly before an online meeting you accepted. It goes back down when the meeting ends.", "Automation"),
  ("Heads-up nudge", "Before the desk moves on its own it gives two tiny nudges in the direction it is about to travel, then waits a second — it never starts without a warning.", "Automation"),
  ("Knows when a call runs over", "Optionally keeps the desk up while Zoom, Teams, Webex, Slack, FaceTime or your browser is still using the microphone or speaker. It only sees that audio is in use — never the audio itself.", "Optional"),
  ("Unplanned calls", "When a call starts that is not in your calendar, a notification offers to raise the desk. Nothing moves until you click.", "Optional"),
  ("Hourly stand goal", "Set how many minutes per hour you want to stand. Time you already stood — in meetings or by hand — counts, so the desk only rises for what is missing.", "Optional"),
  ("AppleScript and Shortcuts", "Scriptable with simple commands, so you can move the desk from Shortcuts, Alfred or your own scripts.", ""),
 ],
 "pl": [
  ("Popover w pasku menu", "Wysokość, stan połączenia i nazwa biurka od razu widać. Mieszka w pasku menu — bez ikony w Docku i dodatkowych okien.", ""),
  ("Przytrzymaj, żeby jechać", "Przytrzymaj okrągły przycisk w górę lub w dół, a biurko jedzie; puszczasz i staje. Nigdy nie ucieka.", ""),
  ("Presety Stand i Sit", "Jedno kliknięcie wysyła biurko na zapisaną wysokość stania lub siedzenia i zatrzymuje. Kliknij ponownie, żeby zatrzymać po drodze.", ""),
  ("Wstaje przed spotkaniami", "Standup czyta Twój Kalendarz Apple — także konta Outlook, Exchange i Microsoft 365 dodane do macOS — i podnosi biurko tuż przed spotkaniem online, które zaakceptowałeś. Po spotkaniu opuszcza je z powrotem.", "Automatyzacja"),
  ("Ostrzegawcze szturchnięcie", "Zanim biurko ruszy samo, delikatnie szturcha dwa razy w stronę, w którą zaraz pojedzie, i czeka sekundę — nigdy nie rusza bez ostrzeżenia.", "Automatyzacja"),
  ("Wie, kiedy rozmowa się przedłuża", "Opcjonalnie trzyma biurko w górze, dopóki Zoom, Teams, Webex, Slack, FaceTime lub przeglądarka używa mikrofonu albo głośnika. Widzi tylko, że dźwięk jest używany — nigdy samego dźwięku.", "Opcjonalnie"),
  ("Nieplanowane rozmowy", "Gdy zacznie się rozmowa, której nie ma w kalendarzu, powiadomienie proponuje podniesienie biurka. Nic się nie rusza, dopóki nie klikniesz.", "Opcjonalnie"),
  ("Godzinowy cel stania", "Ustaw, ile minut w godzinie chcesz stać. Czas, który już przestałeś — na spotkaniach lub ręcznie — się liczy, więc biurko podnosi się tylko na brakującą resztę.", "Opcjonalnie"),
  ("AppleScript i Skróty", "Sterowanie prostymi poleceniami, więc biurkiem możesz ruszać ze Skrótów, Alfreda lub własnych skryptów.", ""),
 ],
}
REQS = {
 "en": ("Requirements", ["macOS 12 or newer", "A Bluetooth sit/stand desk with a Linak controller, such as the IKEA IDÅSEN", "Bluetooth access (to talk to the desk); Calendar access only if you use the meeting features"], "Standup is not affiliated with IKEA or Linak."),
 "pl": ("Wymagania", ["macOS 12 lub nowszy", "Biurko z regulacją wysokości na Bluetooth z kontrolerem Linak, np. IKEA IDÅSEN", "Dostęp do Bluetooth (do rozmowy z biurkiem); dostęp do Kalendarza tylko jeśli używasz funkcji spotkań"], "Standup nie jest powiązany z firmami IKEA ani Linak."),
}
HOME = {
 "en": {"feat_h": "Everything a desk remote should do", "feat_lead": "Simple by default. The automation is there when you want it and quiet when you don't.",
        "open_h": "Open source", "open_p": "A free open-source edition with the same look and manual control — without the meeting automation — is on GitHub."},
 "pl": {"feat_h": "Wszystko, co powinien robić pilot do biurka", "feat_lead": "Domyślnie prosto. Automatyzacja jest, gdy jej chcesz, i milczy, gdy nie.",
        "open_h": "Open source", "open_p": "Darmowa wersja open source z tym samym wyglądem i ręcznym sterowaniem — bez automatyzacji spotkań — jest na GitHubie."},
}

def landing(lang):
    t = T[lang]; h = HOME[lang]
    cards = "\n".join(
        f'<div class="card">{f"<span class=tag>{tag}</span>" if tag else ""}<h3>{html.escape(ti)}</h3><p>{html.escape(tx)}</p></div>'
        for ti, tx, tag in FEATURES[lang])
    rt, ritems, rnote = REQS[lang]
    reqs = "".join(f"<li>{html.escape(i)}</li>" for i in ritems)
    body = f"""<div class="wrap">
<section class="hero">
  <img class="icon" src="/assets/icon.png" width="120" height="120" alt="Standup icon">
  <h1>{t['name']}</h1>
  <p class="sub">{html.escape(t['tagline'])}</p>
  <div class="btns">
    <a class="btn primary" href="{APP_STORE[lang]}">{t['appstore']}</a>
    <a class="btn" href="{GITHUB}">{t['opensrc']}</a>
  </div>
  <div class="shot"><img src="/assets/popover.png" width="920" height="634" alt="Standup popover: current desk height, raise and lower buttons, stand and sit presets, and the meeting automation card"></div>
</section>
<section id="features">
  <h2>{h['feat_h']}</h2>
  <p class="lead">{h['feat_lead']}</p>
  <div class="grid">
{cards}
  </div>
</section>
<section>
  <div class="two">
    <div class="card"><h3>{rt}</h3><ul class="clean">{reqs}</ul><p style="margin-top:10px;font-size:13px">{rnote}</p></div>
    <div class="card"><h3>{h['open_h']}</h3><p>{h['open_p']}</p><p style="margin-top:10px"><a href="{GITHUB}">github.com/sagan-dev/Standup →</a></p></div>
  </div>
</section>
</div>"""
    return layout(lang, "/", t["name"] + " — macOS", t["meta_home"], body)

# ------------------------------------------------------------------ privacy
PRIVACY = {
 "en": ("Privacy Policy", "Effective 29 September 2026", f"""
<p class="note"><strong>In short:</strong> Standup collects no personal data. It has no accounts, no analytics, no tracking and no servers. Everything the app does stays on your Mac.</p>

<h2>Who is responsible</h2>
<p>Standup - Desk Remote Control is developed by Michal Sagan (sagan.dev). Contact: <a href="mailto:{MAIL}">{MAIL}</a>.</p>

<h2>What the app accesses, and why</h2>
<ul>
<li><strong>Bluetooth.</strong> Used only to find and talk to your desk (read its height, send move commands). Nothing is sent anywhere else.</li>
<li><strong>Calendar (only if you turn on the meeting features).</strong> Standup reads your calendar events locally, through Apple's EventKit, to find online meetings you organise or have accepted. Event data is used on the device to decide when to move the desk. It is never stored outside the system calendar, never uploaded and never shared. This includes accounts such as Outlook, Exchange or Microsoft 365 that you have added to macOS.</li>
<li><strong>Audio activity (only if you turn on call detection).</strong> Standup asks macOS only whether an app is currently using audio input (microphone) or output (speaker), and which app. It does <em>not</em> capture, record, listen to or access any audio or video, and it does not request microphone or camera permission.</li>
<li><strong>Notifications (optional).</strong> Local notifications, for example a suggestion to raise the desk during an unplanned call. They are created on your Mac and are not sent through any server.</li>
<li><strong>Settings.</strong> Your preferences (heights, units, options) are stored locally on your Mac in the app's preferences. They are not synced or uploaded.</li>
</ul>

<h2>What we do not do</h2>
<ul>
<li>No personal data is collected, transmitted, sold or shared.</li>
<li>No analytics, advertising, tracking, profiling or crash-reporting SDKs. The app contains no third-party SDKs; the launch-at-login helper is a small local open-source component.</li>
<li>No user accounts and no servers operated by us for the app. The app works fully offline.</li>
</ul>

<h2>Data retention and your control</h2>
<p>Because nothing leaves your Mac, there is no data held by us to access, correct or delete. Local settings can be removed by resetting the app's preferences or uninstalling it. You can revoke Bluetooth, Calendar or Notifications access at any time in <em>System Settings → Privacy &amp; Security</em>, and switch the meeting, call-detection and suggestion features off in Preferences.</p>

<h2>GDPR</h2>
<p>Standup does not process personal data on any server of ours, so there is no processing on our side that could be subject to access, rectification, erasure or portability requests. If you have a question, write to <a href="mailto:{MAIL}">{MAIL}</a>. You also have the right to lodge a complaint with your data-protection authority (in Poland: UODO).</p>

<h2>This website</h2>
<p>standup.sagan.dev is a static website. It sets no cookies and runs no analytics. Like any web host, the hosting provider (Vercel) may process technical server logs such as IP addresses to deliver and secure the site.</p>

<h2>Children</h2>
<p>Standup is a utility app and is not directed at children. It does not knowingly collect any data from anyone.</p>

<h2>Changes</h2>
<p>If this policy changes, the new version will be published on this page with an updated date.</p>
"""),
 "pl": ("Polityka prywatności", "Obowiązuje od 29 września 2026", f"""
<p class="note"><strong>W skrócie:</strong> Standup nie zbiera żadnych danych osobowych. Nie ma kont, analityki, śledzenia ani serwerów. Wszystko, co robi aplikacja, zostaje na Twoim Macu.</p>

<h2>Kto odpowiada</h2>
<p>Standup - Desk Remote Control tworzy Michał Sagan (sagan.dev). Kontakt: <a href="mailto:{MAIL}">{MAIL}</a>.</p>

<h2>Do czego aplikacja ma dostęp i po co</h2>
<ul>
<li><strong>Bluetooth.</strong> Używany wyłącznie do znalezienia biurka i rozmowy z nim (odczyt wysokości, polecenia ruchu). Nic nie jest wysyłane nigdzie indziej.</li>
<li><strong>Kalendarz (tylko jeśli włączysz funkcje spotkań).</strong> Standup czyta wydarzenia z kalendarza lokalnie, przez EventKit firmy Apple, aby znaleźć spotkania online, które organizujesz lub zaakceptowałeś. Dane wydarzeń służą na urządzeniu do decyzji, kiedy ruszyć biurkiem. Nie są przechowywane poza kalendarzem systemowym, przesyłane ani udostępniane. Dotyczy to także kont Outlook, Exchange i Microsoft 365 dodanych do macOS.</li>
<li><strong>Aktywność audio (tylko jeśli włączysz wykrywanie rozmów).</strong> Standup pyta macOS wyłącznie o to, czy jakaś aplikacja używa teraz wejścia audio (mikrofonu) lub wyjścia (głośnika) i która. <em>Nie</em> przechwytuje, nie nagrywa, nie podsłuchuje ani nie ma dostępu do żadnego dźwięku ani obrazu i nie prosi o dostęp do mikrofonu ani kamery.</li>
<li><strong>Powiadomienia (opcjonalne).</strong> Lokalne powiadomienia, np. propozycja podniesienia biurka podczas nieplanowanej rozmowy. Powstają na Twoim Macu i nie przechodzą przez żaden serwer.</li>
<li><strong>Ustawienia.</strong> Twoje preferencje (wysokości, jednostki, opcje) są zapisane lokalnie na Macu w ustawieniach aplikacji. Nie są synchronizowane ani wysyłane.</li>
</ul>

<h2>Czego nie robimy</h2>
<ul>
<li>Żadne dane osobowe nie są zbierane, przesyłane, sprzedawane ani udostępniane.</li>
<li>Brak analityki, reklam, śledzenia, profilowania i SDK do raportowania awarii. Aplikacja nie zawiera SDK firm trzecich; pomocnik uruchamiania przy logowaniu to mały lokalny komponent open source.</li>
<li>Brak kont użytkowników i serwerów prowadzonych przez nas na potrzeby aplikacji. Aplikacja działa w pełni offline.</li>
</ul>

<h2>Przechowywanie danych i Twoja kontrola</h2>
<p>Ponieważ nic nie opuszcza Twojego Maca, nie mamy żadnych danych, do których dałoby się żądać dostępu, sprostowania czy usunięcia. Lokalne ustawienia usuniesz, resetując preferencje aplikacji lub odinstalowując ją. Dostęp do Bluetooth, Kalendarza i Powiadomień możesz w każdej chwili cofnąć w <em>Ustawieniach systemowych → Prywatność i ochrona</em>, a funkcje spotkań, wykrywania rozmów i propozycji wyłączyć w Preferencjach.</p>

<h2>RODO</h2>
<p>Standup nie przetwarza danych osobowych na żadnym naszym serwerze, więc po naszej stronie nie ma przetwarzania, do którego mogłyby odnosić się żądania dostępu, sprostowania, usunięcia czy przenoszenia. W razie pytań napisz na <a href="mailto:{MAIL}">{MAIL}</a>. Masz też prawo wnieść skargę do organu ochrony danych (w Polsce: UODO).</p>

<h2>Ta strona</h2>
<p>standup.sagan.dev jest stroną statyczną. Nie ustawia plików cookie i nie uruchamia analityki. Jak każdy hosting, dostawca (Vercel) może przetwarzać techniczne logi serwera, np. adresy IP, aby dostarczać i zabezpieczać stronę.</p>

<h2>Dzieci</h2>
<p>Standup jest aplikacją narzędziową i nie jest skierowany do dzieci. Świadomie nie zbiera danych od nikogo.</p>

<h2>Zmiany</h2>
<p>Jeśli ta polityka się zmieni, nowa wersja pojawi się na tej stronie ze zaktualizowaną datą.</p>
"""),
}

# ------------------------------------------------------------------ support
SUPPORT = {
 "en": ("Support", "Answers to common questions. Still stuck? Write to " + f'<a href="mailto:{MAIL}">{MAIL}</a>.', [
  ("Standup can't find my desk", """<p>Try these in order:</p><ol>
<li>Close any other app connected to the desk (a phone app, another Mac). The desk talks to one device at a time.</li>
<li>Allow Bluetooth for Standup in <em>System Settings → Privacy &amp; Security → Bluetooth</em>.</li>
<li>Make sure the desk's name in Bluetooth still contains the word "Desk".</li>
<li>Reset the desk: lower it as far as it goes, hold the lower button until the desk jumps down and up, then hold the Bluetooth button on the controller until the light blinks, and open Standup again.</li></ol>"""),
  ("How do I use Outlook meetings?", """<p>Standup reads the macOS Calendar. Add your Outlook, Exchange or Microsoft 365 account in <em>System Settings → Internet Accounts</em> and make sure Calendars is switched on for it. The account then shows up in the Calendar app and Standup sees its meetings. Allow calendar access when Standup asks.</p>"""),
  ("Which meetings raise the desk?", """<p>Meetings that have other attendees, contain an online meeting link (Teams, Meet, Zoom, Webex, Whereby or GoToMeeting) in the URL, location or notes, and that you organise or have accepted. All-day events, cancelled, declined, tentative or unanswered invitations and events marked as "free" are ignored. The desk starts rising a couple of minutes before the start (you can change the lead time in Preferences).</p>"""),
  ("Why did the desk not move for my meeting?", """<p>Check that the feature is on (<em>Stand during meetings</em>), that the meeting matches the rules above, and that the desk is connected. If you lowered the desk yourself during a meeting, Standup does not raise it again for that meeting.</p>"""),
  ("What is the little nudge before the desk moves?", """<p>Before an automatic move the desk nudges twice in the direction it is about to travel and waits a second, so it never moves without a warning. Turn it off in Preferences with <em>Nudge the desk before it moves</em>. Moves you start yourself are always immediate.</p>"""),
  ("What does call detection do, and is my audio recorded?", """<p>If you turn on <em>Keep raised while on a call</em>, the desk stays up after the scheduled end while a meeting app is still using the microphone or speaker, and goes down shortly after they go quiet. Standup only sees <em>that</em> an app is using audio and which app — it never records or accesses any audio or video, and it does not ask for microphone or camera permission.</p>"""),
  ("The desk stops a little short or a little past my preset height", """<p>Standup learns how far your desk rolls after a stop and corrects itself after a few moves. If it stays off by more than about half a centimetre, write to us with the two heights.</p>"""),
  ("Can I control the desk from a script or Shortcuts?", """<p>Yes. Standup understands these AppleScript commands:</p>
<pre><code>tell application "Standup" to move desk "stand"    -- or "sit", "up", "down"
tell application "Standup" to set desk height "120cm"  -- or "48in", or just "80"</code></pre>
<p>In Shortcuts, add a <em>Run AppleScript</em> action with one of those lines. macOS asks once for permission to control Standup.</p>"""),
  ("How do I start Standup at login, or quit it?", """<p>Open <em>Preferences</em> from the "…" menu in the popover and switch on <em>Open at login</em>. Choose <em>Quit</em> from the same menu to close the app.</p>"""),
 ], "Contact", f'Email: <a href="mailto:{MAIL}">{MAIL}</a>. The free open-source edition (without meeting automation) takes bug reports on <a href="{GITHUB}/issues">GitHub</a>.'),
 "pl": ("Wsparcie", "Odpowiedzi na częste pytania. Nadal nie działa? Napisz na " + f'<a href="mailto:{MAIL}">{MAIL}</a>.', [
  ("Standup nie widzi mojego biurka", """<p>Spróbuj po kolei:</p><ol>
<li>Zamknij każdą inną aplikację połączoną z biurkiem (aplikację na telefonie, inny Mac). Biurko rozmawia z jednym urządzeniem naraz.</li>
<li>Zezwól Standupowi na Bluetooth w <em>Ustawieniach systemowych → Prywatność i ochrona → Bluetooth</em>.</li>
<li>Upewnij się, że nazwa biurka w Bluetooth nadal zawiera słowo „Desk”.</li>
<li>Zresetuj biurko: opuść je do samego dołu, przytrzymaj przycisk w dół, aż biurko podskoczy w dół i w górę, potem przytrzymaj przycisk Bluetooth na sterowniku, aż dioda zacznie migać, i otwórz Standup ponownie.</li></ol>"""),
  ("Jak używać spotkań z Outlooka?", """<p>Standup czyta Kalendarz macOS. Dodaj konto Outlook, Exchange lub Microsoft 365 w <em>Ustawieniach systemowych → Konta internetowe</em> i upewnij się, że Kalendarze są dla niego włączone. Konto pojawi się wtedy w aplikacji Kalendarz, a Standup zobaczy jego spotkania. Zezwól na dostęp do kalendarza, gdy Standup o to poprosi.</p>"""),
  ("Które spotkania podnoszą biurko?", """<p>Takie, które mają innych uczestników, zawierają link do spotkania online (Teams, Meet, Zoom, Webex, Whereby lub GoToMeeting) w adresie URL, lokalizacji lub notatkach i które organizujesz albo zaakceptowałeś. Wydarzenia całodniowe, odwołane, odrzucone, wstępnie zaakceptowane lub bez odpowiedzi oraz oznaczone jako „wolny” są pomijane. Biurko zaczyna się podnosić kilka minut przed startem (czas możesz zmienić w Preferencjach).</p>"""),
  ("Dlaczego biurko nie ruszyło na moje spotkanie?", """<p>Sprawdź, czy funkcja jest włączona (<em>Stand during meetings</em>), czy spotkanie spełnia powyższe zasady i czy biurko jest połączone. Jeśli sam opuściłeś biurko w trakcie spotkania, Standup nie podniesie go ponownie w tym spotkaniu.</p>"""),
  ("Co to za małe szturchnięcie przed ruchem biurka?", """<p>Przed automatycznym ruchem biurko dwa razy delikatnie szturcha w stronę, w którą zaraz pojedzie, i czeka sekundę, więc nigdy nie rusza bez ostrzeżenia. Wyłączysz to w Preferencjach opcją <em>Nudge the desk before it moves</em>. Ruchy, które sam uruchamiasz, są zawsze natychmiastowe.</p>"""),
  ("Co robi wykrywanie rozmów i czy mój dźwięk jest nagrywany?", """<p>Jeśli włączysz <em>Keep raised while on a call</em>, biurko zostaje w górze po zaplanowanym końcu, dopóki aplikacja spotkaniowa używa mikrofonu lub głośnika, i opuszcza się krótko po ich ucichnięciu. Standup widzi tylko, <em>że</em> aplikacja używa dźwięku i która — nigdy niczego nie nagrywa ani nie ma dostępu do dźwięku czy obrazu i nie prosi o dostęp do mikrofonu ani kamery.</p>"""),
  ("Biurko zatrzymuje się trochę przed albo za wysokością presetu", """<p>Standup uczy się, ile Twoje biurko jeszcze jedzie po zatrzymaniu, i koryguje się po kilku ruchach. Jeśli nadal myli się o więcej niż pół centymetra, napisz do nas i podaj obie wysokości.</p>"""),
  ("Czy mogę sterować biurkiem ze skryptu albo Skrótów?", """<p>Tak. Standup rozumie te polecenia AppleScript:</p>
<pre><code>tell application "Standup" to move desk "stand"    -- lub "sit", "up", "down"
tell application "Standup" to set desk height "120cm"  -- lub "48in", albo samo "80"</code></pre>
<p>W Skrótach dodaj akcję <em>Uruchom AppleScript</em> z jedną z tych linii. macOS raz zapyta o zgodę na sterowanie Standupem.</p>"""),
  ("Jak uruchamiać Standup przy logowaniu albo go zamknąć?", """<p>Otwórz <em>Preferencje</em> z menu „…” w popoverze i włącz <em>Open at login</em>. Wybierz <em>Quit</em> z tego samego menu, żeby zamknąć aplikację.</p>"""),
 ], "Kontakt", f'E-mail: <a href="mailto:{MAIL}">{MAIL}</a>. Darmowa wersja open source (bez automatyzacji spotkań) przyjmuje zgłoszenia błędów na <a href="{GITHUB}/issues">GitHubie</a>.'),
}

def doc_page(lang, kind):
    t = T[lang]
    if kind == "privacy":
        title, meta, content = PRIVACY[lang]
        body = f'<div class="wrap"><article class="doc"><h1>{title}</h1><p class="meta">{meta}</p>{content}</article></div>'
        return layout(lang, "/privacy", f"{title} — {t['name']}", t["meta_privacy"], body)
    title, intro, faqs, ch, contact = SUPPORT[lang]
    items = "\n".join(f"<details><summary>{q}</summary>{a}</details>" for q, a in faqs)
    body = f'<div class="wrap"><article class="doc"><h1>{title}</h1><p class="meta">{intro}</p>{items}<h2>{ch}</h2><p>{contact}</p></article></div>'
    return layout(lang, "/support", f"{title} — {t['name']}", t["meta_support"], body)

def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

urls = []
for lang in ("en", "pl"):
    pre = T[lang]["prefix"].lstrip("/")
    write(f"{pre}/index.html" if pre else "index.html", landing(lang))
    write(f"{pre}/privacy/index.html" if pre else "privacy/index.html", doc_page(lang, "privacy"))
    write(f"{pre}/support/index.html" if pre else "support/index.html", doc_page(lang, "support"))
    urls += [url(lang, "/"), url(lang, "/privacy"), url(lang, "/support")]

not_found = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found — Standup</title><link rel="stylesheet" href="/style.css?v={ASSET_V}"><link rel="icon" href="/assets/favicon-32.png"></head><body><div class="wrap"><section class="hero"><img class="icon" src="/assets/icon.png" width="96" height="96" alt=""><h1>404</h1><p class="sub">This page does not exist.</p><div class="btns"><a class="btn primary" href="/">Standup home</a></div></section></div></body></html>"""
write("404.html", not_found)
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
sm = "\n".join(f"  <url><loc>{BASE}{u}</loc></url>" for u in urls)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
write("vercel.json", '{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
print("built", len(urls), "pages")
