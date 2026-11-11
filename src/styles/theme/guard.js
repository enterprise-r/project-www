/* Dark-® click guard.
   Movement ends → start timer → --r-guard-gap1 → HOT (clicks accepted)
   for --r-guard-gap2 → OFF until the pointer moves and stops again.
   Each pointermove resets the gap-1 timer (movement end is the last move).
   An accepted click turns clicks off for --r-guard-cool, then stays OFF
   until the pointer moves and stops again.
   Clicks are judged on button up (pointerup), not on pointerdown; a
   discarded up also suppresses the following click.
   A discarded click flashes the waiting cursor until the button is HOT,
   or briefly if it cannot become clickable without further movement.
   Touch and keyboard use the cooldown only.
   Applies to button and input type=button/submit/reset, not links.
   Opt out with .r-unguarded on the control or an ancestor.
   <script src="theme/guard.js"></script> */
(function () {
  "use strict";

  var GAP1_MS = 300;
  var GAP2_MS = 10000;
  var COOL_MS = 400;
  var MOVE_PX = 3;
  var SELECTOR = "button, input[type=button], input[type=submit], input[type=reset]";
  var WAIT = "r-guard-wait";
  var state = new WeakMap();
  var timed = false;

  function msVar(name, fallback) {
    try {
      var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      if (!v) return fallback;
      var n = parseFloat(v);
      if (isNaN(n)) return fallback;
      if (v.slice(-2) === "ms") return n;
      if (v.slice(-1) === "s") return n * 1000;
      return n;
    } catch (err) {
      return fallback;
    }
  }

  function timings() {
    if (timed) return;
    timed = true;
    GAP1_MS = msVar("--r-guard-gap1", 300);
    GAP2_MS = msVar("--r-guard-gap2", 10000);
    COOL_MS = msVar("--r-guard-cool", 400);
  }

  function target(el) {
    if (!el || !el.closest) return null;
    var btn = el.closest(SELECTOR);
    if (!btn || btn.closest(".r-unguarded")) return null;
    return btn;
  }

  function get(el) {
    var s = state.get(el);
    if (!s) {
      s = {
        hot: false,
        hover: false,
        fromKey: false,
        pointerType: "",
        coolUntil: 0,
        gap1Timer: 0,
        gap2Timer: 0,
        coolTimer: 0,
        flashTimer: 0,
        flashUntilHot: false,
        suppressClick: false,
        acceptedUp: false,
        lastX: null,
        lastY: null
      };
      state.set(el, s);
    }
    return s;
  }

  function cooling(s) {
    return s.coolUntil > Date.now();
  }

  function clearTimer(s, name) {
    if (s[name]) {
      clearTimeout(s[name]);
      s[name] = 0;
    }
  }

  function hideWait(el, s) {
    clearTimer(s, "flashTimer");
    s.flashUntilHot = false;
    el.classList.remove(WAIT);
  }

  function showWait(el, s, ms) {
    el.classList.add(WAIT);
    clearTimer(s, "flashTimer");
    s.flashUntilHot = false;
    s.flashTimer = setTimeout(function () {
      s.flashTimer = 0;
      el.classList.remove(WAIT);
    }, ms);
  }

  function showWaitUntilHot(el, s) {
    el.classList.add(WAIT);
    clearTimer(s, "flashTimer");
    s.flashUntilHot = true;
  }

  function goOff(s) {
    s.hot = false;
    clearTimer(s, "gap1Timer");
    clearTimer(s, "gap2Timer");
  }

  function becomeHot(el, s) {
    if (cooling(s) || !s.hover) return;
    s.hot = true;
    clearTimer(s, "gap1Timer");
    clearTimer(s, "gap2Timer");
    if (s.flashUntilHot) hideWait(el, s);
    s.gap2Timer = setTimeout(function () {
      s.gap2Timer = 0;
      s.hot = false;
    }, GAP2_MS);
  }

  function startGap1(el, s) {
    clearTimer(s, "gap1Timer");
    s.gap1Timer = setTimeout(function () {
      s.gap1Timer = 0;
      becomeHot(el, s);
    }, GAP1_MS);
  }

  function onMove(el, s) {
    if (s.pointerType === "touch") return;
    goOff(s);
    if (cooling(s)) return;
    startGap1(el, s);
  }

  function movedEnough(s, e) {
    if (s.lastX == null || s.lastY == null) {
      s.lastX = e.clientX;
      s.lastY = e.clientY;
      return false;
    }
    var dx = e.clientX - s.lastX;
    var dy = e.clientY - s.lastY;
    if ((dx * dx + dy * dy) < MOVE_PX * MOVE_PX) return false;
    s.lastX = e.clientX;
    s.lastY = e.clientY;
    return true;
  }

  function startCool(el, s) {
    goOff(s);
    hideWait(el, s);
    clearTimer(s, "coolTimer");
    s.coolUntil = Date.now() + COOL_MS;
    s.coolTimer = setTimeout(function () {
      s.coolTimer = 0;
      s.coolUntil = 0;
    }, COOL_MS);
  }

  function block(e, el, s) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var untilCool = cooling(s) && (s.pointerType === "touch" || e.type === "keydown" || s.fromKey);
    if (untilCool) showWait(el, s, Math.max(1, s.coolUntil - Date.now()));
    else if (s.gap1Timer && !cooling(s)) showWaitUntilHot(el, s);
    else showWait(el, s, GAP1_MS);
  }

  function sameButton(btn, related) {
    return related && btn.contains(related);
  }

  document.addEventListener("pointermove", function (e) {
    var btn = target(e.target);
    if (!btn) return;
    timings();
    var s = get(btn);
    s.hover = true;
    s.pointerType = e.pointerType;
    if (e.buttons & 1) return;
    if (!movedEnough(s, e)) return;
    onMove(btn, s);
  }, true);

  document.addEventListener("pointerover", function (e) {
    var btn = target(e.target);
    if (!btn || sameButton(btn, e.relatedTarget)) return;
    timings();
    var s = get(btn);
    s.hover = true;
    s.pointerType = e.pointerType;
    s.lastX = e.clientX;
    s.lastY = e.clientY;
  }, true);

  document.addEventListener("pointerout", function (e) {
    var btn = target(e.target);
    if (!btn || sameButton(btn, e.relatedTarget)) return;
    var s = get(btn);
    s.hover = false;
    s.lastX = null;
    s.lastY = null;
    goOff(s);
    hideWait(btn, s);
  }, true);

  document.addEventListener("pointerup", function (e) {
    if (e.button !== 0) return;
    var btn = target(e.target);
    if (!btn) return;
    timings();
    var s = get(btn);
    s.pointerType = e.pointerType;
    if (e.pointerType === "touch") {
      if (cooling(s)) {
        block(e, btn, s);
        s.suppressClick = true;
      } else {
        s.acceptedUp = true;
      }
      return;
    }
    if (cooling(s) || !s.hot) {
      block(e, btn, s);
      s.suppressClick = true;
    } else {
      s.acceptedUp = true;
    }
  }, true);

  document.addEventListener("click", function (e) {
    var btn = target(e.target);
    if (!btn) return;
    timings();
    var s = get(btn);
    if (s.suppressClick) {
      s.suppressClick = false;
      e.preventDefault();
      e.stopImmediatePropagation();
      return;
    }
    if (s.acceptedUp) {
      s.acceptedUp = false;
      s.fromKey = false;
      startCool(btn, s);
      return;
    }
    if (s.fromKey) {
      s.fromKey = false;
      if (cooling(s)) {
        block(e, btn, s);
        return;
      }
      startCool(btn, s);
      return;
    }
    if (cooling(s) || !s.hot) {
      block(e, btn, s);
      return;
    }
    startCool(btn, s);
  }, true);

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var btn = target(e.target);
    if (!btn || (e.target !== btn && !btn.contains(e.target))) return;
    timings();
    var s = get(btn);
    if (cooling(s)) {
      block(e, btn, s);
      return;
    }
    s.fromKey = true;
  }, true);
})();
