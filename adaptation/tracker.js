/**
 * File Name: tracker.js
 * Role: Member 4 - Automated DOM Tracker
 */

function attachAdaptiTracker(engineInstance) {
  let clickCount = 0;
  let lastClickTarget = null;
  let clickTimer = null;

  // 1. Detect Repeated Clicks on the same element within 1.5s
  document.addEventListener("click", (e) => {
    const target = e.target;

    if (target === lastClickTarget) {
      clickCount++;
    } else {
      lastClickTarget = target;
      clickCount = 1;
    }

    clearTimeout(clickTimer);
    clickTimer = setTimeout(() => {
      clickCount = 0;
      lastClickTarget = null;
    }, 1500);

    if (clickCount >= 3) {
      engineInstance.repeatedClick();
      clickCount = 0;
    }
  });

  // 2. Detect Form Validation Errors
  document.addEventListener("invalid", () => {
    engineInstance.formError();
  }, true);

  // 3. Detect Inactivity (30s)
  let inactivityTimer;
  const resetInactivity = () => {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
      engineInstance.longInactivity();
    }, 30000);
  };

  ["mousemove", "keydown", "scroll", "touchstart"].forEach((event) => {
    document.addEventListener(event, resetInactivity, { passive: true });
  });

  resetInactivity();
}