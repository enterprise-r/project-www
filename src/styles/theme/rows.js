/* Dark-R dynamic list. Enhances any .r-rows: add and remove rows, keyboard,
   live-region announcements, and data-name="…{i}…" templates. No dependencies.
   <script src="theme/rows.js"></script> */
(function (global) {
  "use strict";

  var TOKEN = /\{i\}|\{n\}/g;
  var ready = new WeakSet();

  function fill(template, i, n) {
    return String(template).replace(TOKEN, function (tok) {
      return tok === "{i}" ? String(i) : String(n);
    });
  }

  function enhance(root) {
    if (!root || ready.has(root)) return;
    var list = root.querySelector(".r-rows-list");
    var addBtn = root.querySelector(".r-row-add");
    var live = root.querySelector(".r-rows-live");
    if (!list || !addBtn) return;
    ready.add(root);

    var addedMsg = root.getAttribute("data-added") || "Row added";
    var removedMsg = root.getAttribute("data-removed") || "Row removed";
    var removeTpl = root.getAttribute("data-remove") || "Remove row {n}";

    function rows() {
      return Array.prototype.slice.call(list.querySelectorAll(":scope > .r-row"));
    }

    function announce(msg) {
      if (!live) return;
      live.textContent = "";
      requestAnimationFrame(function () { live.textContent = msg; });
    }

    function reindex() {
      var all = rows();
      all.forEach(function (row, i) {
        var n = i + 1;
        Array.prototype.forEach.call(row.querySelectorAll("input, select, textarea"), function (inp) {
          var nameTpl = inp.getAttribute("data-name");
          if (nameTpl) inp.name = fill(nameTpl, i, n);
          var idTpl = inp.getAttribute("data-id");
          if (idTpl) inp.id = fill(idTpl, i, n);
          var labelTpl = inp.getAttribute("data-label");
          if (labelTpl) inp.setAttribute("aria-label", fill(labelTpl, i, n));
        });
        var rm = row.querySelector(".r-row-remove");
        if (rm) {
          var label = fill(removeTpl, i, n);
          rm.setAttribute("aria-label", label);
          rm.disabled = all.length === 1;
        }
      });
    }

    function makeRow() {
      var all = rows();
      var src = all[all.length - 1];
      if (!src) return null;
      var row = src.cloneNode(true);
      row.classList.remove("is-new");
      row.classList.add("is-new");
      Array.prototype.forEach.call(row.querySelectorAll("input, select, textarea"), function (inp) {
        if (inp.type === "checkbox" || inp.type === "radio") inp.checked = false;
        else inp.value = "";
      });
      return row;
    }

    function add() {
      var row = makeRow();
      if (!row) return;
      list.appendChild(row);
      reindex();
      announce(addedMsg);
      var first = row.querySelector("input, select, textarea");
      if (first) first.focus();
    }

    function removeRow(row) {
      var all = rows();
      if (all.length === 1) return;
      var i = all.indexOf(row);
      var target = all[i + 1] || all[i - 1];
      row.parentNode.removeChild(row);
      reindex();
      announce(removedMsg);
      if (target) {
        var el = target.querySelector("input, select, textarea");
        if (el) el.focus();
      } else {
        addBtn.focus();
      }
    }

    addBtn.addEventListener("click", add);
    list.addEventListener("click", function (e) {
      var btn = e.target.closest(".r-row-remove");
      if (btn && !btn.disabled) {
        var row = btn.closest(".r-row");
        if (row && list.contains(row)) removeRow(row);
      }
    });
    list.addEventListener("keydown", function (e) {
      var input = e.target.closest("input");
      if (!input || !list.contains(input)) return;
      var row = input.closest(".r-row");
      if (!row) return;
      var all = rows();
      if (e.key === "Enter" && row === all[all.length - 1]) {
        e.preventDefault();
        add();
      }
      if (e.key === "Backspace" && input.selectionStart === 0 && input.selectionEnd === 0
          && all.length > 1) {
        var fields = Array.prototype.slice.call(row.querySelectorAll("input"));
        var empty = fields.every(function (el) { return el.value === ""; });
        if (!empty) return;
        e.preventDefault();
        var i = all.indexOf(row);
        var prev = all[i - 1];
        row.parentNode.removeChild(row);
        reindex();
        announce(removedMsg);
        if (prev) {
          var prevFields = Array.prototype.slice.call(prev.querySelectorAll("input"));
          var last = prevFields[prevFields.length - 1];
          if (last) {
            last.focus();
            if (last.setSelectionRange) {
              var end = last.value.length;
              last.setSelectionRange(end, end);
            }
          }
        } else {
          var first = rows()[0] && rows()[0].querySelector("input");
          if (first) first.focus();
        }
      }
    });
    reindex();
  }

  function enhanceAll(scope) {
    var root = scope && scope.querySelectorAll ? scope : document;
    Array.prototype.forEach.call(root.querySelectorAll(".r-rows"), enhance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { enhanceAll(); });
  } else {
    enhanceAll();
  }

  global.rRows = { enhance: enhance, enhanceAll: enhanceAll };
})(typeof window !== "undefined" ? window : this);
