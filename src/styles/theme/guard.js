/* Dark-® click guard.
   Movement (or arriving on the control) → HOT immediately, including
   during movement. The hot window --r-guard-gap2 (10s) restarts on each
   movement. After 10s with no movement, OFF until the pointer moves again.
   An accepted press turns clicks off for --r-guard-cool, then stays OFF
   until the pointer moves again.
   Clicks are judged on button press (pointerdown), not on pointerup; a
   discarded press also suppresses the following click.
   A discarded press flashes the waiting cursor for 300ms.
   Touch and keyboard use the cooldown only.
   Applies to button and input type=button/submit/reset, not links.
   Opt out with .r-unguarded on the control or an ancestor.
   <script src="theme/guard.js"></script> */
(function () {
  "use strict";

  var GAP2_MS = 10000;
  var COOL_MS = 400;
  var FLASH_MS = 300;
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
        gap2Timer: 0,
        coolTimer: 0,
        flashTimer: 0,
        suppressClick: false,
        acceptedPress: false,
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
    el.classList.remove(WAIT);
  }

  function showWait(el, s, ms) {
    el.classList.add(WAIT);
    clearTimer(s, "flashTimer");
    s.flashTimer = setTimeout(function () {
      s.flashTimer = 0;
      el.classList.remove(WAIT);
    }, ms);
  }

  function goOff(s) {
    s.hot = false;
    clearTimer(s, "gap2Timer");
  }

  function becomeHot(el, s) {
    if (cooling(s) || !s.hover) return;
    s.hot = true;
    clearTimer(s, "gap2Timer");
    hideWait(el, s);
    s.gap2Timer = setTimeout(function () {
      s.gap2Timer = 0;
      s.hot = false;
    }, GAP2_MS);
  }

  function onMove(el, s) {
    if (s.pointerType === "touch") return;
    if (cooling(s)) return;
    becomeHot(el, s);
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
    showWait(el, s, FLASH_MS);
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
    onMove(btn, s);
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

  document.addEventListener("pointerdown", function (e) {
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
        s.acceptedPress = true;
      }
      return;
    }
    if (cooling(s) || !s.hot) {
      block(e, btn, s);
      s.suppressClick = true;
    } else {
      s.acceptedPress = true;
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
    if (s.acceptedPress) {
      s.acceptedPress = false;
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
