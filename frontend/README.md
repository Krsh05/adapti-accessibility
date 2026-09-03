# ADAPTI — Frontend Documentation & Test Plan (Member 2 Deliverable)

This document specifies the UI layout, browser runtime requirements, interactive flows, DOM hook references, and test cases for **Member 6 (Testing)**.

---

## 1. Environment & Runtime Prerequisites

* **Target File:** `frontend/index.html`
* **Recommended Browsers:** Google Chrome (v110+) or Microsoft Edge (v110+).  
  * *Note:* Safari and Firefox do not fully support the native Web Speech Recognition API out of the box. Chrome or Edge is required for microphone dictation testing.
* **Microphone Access:** Ensure microphone permissions are granted when prompted by the browser.
* **Dependencies:** Zero npm packages. Pure HTML5, CSS3, and ES6 JavaScript.

---

## 2. Integrated Architecture (Member 2 + Member 4)

1. **Member 4 Engine Scripts:**
   * Script path: `../adaptation/friction.js` (`AdaptiEngine` class)
   * Script path: `../adaptation/tracker.js` (`attachAdaptiTracker` function)
2. **State Subscriptions:**
   * Threshold set to `50`.
   * When `score >= 50` or `isHighFriction === true`, `document.body` is dynamically assigned the `.simplify-mode` class, transforming layout target sizes and suppressing visual noise.
3. **AI Action Dispatcher:**
   * `INCREASE_FONT_SIZE`: Increments `--adapti-scale` up to `1.4x` and applies `.font-large`.
   * `RESET_FONT_SIZE`: Resets `--adapti-scale` to `1.0` and removes `.font-large`.
   * `SIMPLIFY_MODE`: Triggers the stepped guided mode directly.
   * `HIGH_CONTRAST`: Toggles high-contrast styling (`.high-contrast`).

---

## 3. Key DOM Elements Reference Table

| DOM Selector / ID | Element Type | Function / Behavior |
| :--- | :--- | :--- |
| `#hud` | `<div>` | Floating Telemetry HUD on the bottom-left showing live friction metrics. |
| `#hudScore` | `<span>` | Displays numerical friction score percentage (0–100%). |
| `#meterFill` | `<div>` | Dynamic meter bar (Green: 0–34%, Yellow: 35–49%, Red: 50%+). |
| `#hudStateMode` | `<span>` | Engine state text (`Normal` vs. `High Friction`). |
| `#toggleModeBtn` | `<button>` | Manual switcher between legacy portal view and ADAPTI guided mode. |
| `#portalView` | `<div>` | The cluttered, unadapted legacy application form. |
| `#testRageBtn` | `<button>` | Disabled submission button used to simulate rage-click events. |
| `#frictionPrompt` | `<div>` | Assistance popup rendered when friction threshold is reached. |
| `#adaptiView` | `<div>` | Simplified, stepped container (Step 1 and Step 2). |
| `#userNameInput` | `<input>` | Candidate name field supporting live dictation and echo typing. |
| `#micBtn` | `<button>` | Speech recognition trigger (changes to `.recording` with pulsing indicator). |
| `#listeningIndicator`| `<span>` | Visual indicator confirming microphone listening state. |
| `#echoBtn` | `<button>` | Toggle button for "Read While Typing" feature. |
| `#stepCounter` | `<span>` | Step progress tracker (`Step 1 of 2` / `Step 2 of 2`). |
| `#userDocInput` | `<input>` | File input field in Step 2. |
| `#successView` | `<div>` | Application completion screen. |

---

## 4. Testing Procedures for Member 6

### Test Case 1: Passive Friction Detection & Modal Trigger
1. Open `frontend/index.html` in Chrome.
2. In the unadapted view, click `#testRageBtn` repeatedly (3+ times).
3. **Expected Result:**
   * `#hudScore` increases.
   * `#meterFill` turns red when the score reaches `50%`.
   * `#frictionPrompt` appears on the bottom-right.
   * The browser reads aloud: *"Difficulty detected. Would you like ADAPTI to simplify this form into easy steps?"*

### Test Case 2: Assistive Mode Transition
1. On the friction popup, click **"Simplify Now"** (or click `#toggleModeBtn`).
2. **Expected Result:**
   * `#portalView` acquires class `.hidden`.
   * `#adaptiView` is displayed.
   * `#step1` is visible; `#step2` is hidden.
   * Audio prompt auto-announces: *"We simplified this page. What is your full name?"*

### Test Case 3: Speech-to-Text Dictation & Echo Back
1. In Step 1, click `#micBtn` (microphone icon).
2. Allow browser microphone access when requested.
3. Speak clearly: *"Niva Patel"*.
4. **Expected Result:**
   * Text renders in `#userNameInput` in real time as words are spoken.
   * `#micBtn` pulses red and displays `#listeningIndicator`.
   * Upon silence, the recording stops, and text-to-speech speaks back: *"You said: Niva Patel"*.

### Test Case 4: "Type & Talk" (Echo Typing)
1. Ensure `#echoBtn` displays `Read While Typing: ON`.
2. Clear `#userNameInput` and type a single word followed by the **Spacebar** (e.g., `Testing `).
   * **Expected Result:** Browser speaks the word *"Testing"*.
3. Type a sentence followed by a period (e.g., `It works.`).
   * **Expected Result:** Browser speaks the full sentence *"It works."*.
4. Click `#echoBtn` to toggle it to `OFF` and type again.
   * **Expected Result:** No audio is emitted.

### Test Case 5: Visual Accessibility Toolbar
1. Click `🌓 Contrast` in the top toolbar.
   * **Expected Result:** `document.body` gains `.high-contrast`. Background turns black (#000000) and text turns high-visibility yellow (#ffff00).
2. Click `📖 Dyslexia Font`.
   * **Expected Result:** `document.body` gains `.dyslexic-mode`. Font changes to a dyslexia-friendly font with wider letter spacing (0.08em) and increased line height (1.8).
3. Click `A+` twice, then `A-` once.
   * **Expected Result:** Text elements smoothly scale up and down across the entire layout without horizontal overflow.

### Test Case 6: Stepped Form Completion & Reset
1. Enter a name in Step 1 and click **"Continue to Document Upload →"**.
   * **Expected Result:** `#step1` hides, `#step2` appears, `#stepCounter` updates to `Step 2 of 2`.
2. Select any local file in `#userDocInput` and click **"Complete Submission ✓"**.
   * **Expected Result:** `#successView` appears with confirmation message, and confirmation audio announces submission.
3. Click **"Start Over"**.
   * **Expected Result:** Form inputs reset, friction score returns to `0%`, and the UI returns to the initial state.