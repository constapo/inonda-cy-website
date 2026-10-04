/* Inonda LTD (inonda.org) — language switching, menu, header, reveal, hero video, cookie notice, forms */
(function () {
  "use strict";
  var STORE = "inondacy_lang";

  function currentLang() {
    var m = location.pathname.match(/^\/(el|en|ru|uk|he|ro)(\/|$)/);
    return m ? m[1] : (document.documentElement.lang || "en");
  }
  function remember(lang) {
    try { localStorage.setItem(STORE, lang); } catch (e) {}
  }
  function go(lang) {
    /* jump to the same page in the chosen language, using the page's own hreflang links */
    remember(lang);
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
    var target = alt ? alt.getAttribute("href").replace(/^https?:\/\/[^\/]+/, "") : "/" + lang + "/";
    if (LOCAL) {
      /* opened straight from disk: resolve against the site folder and name the file explicitly */
      location.href = location.href.replace(/\/(el|en|ru|uk|he|ro)\/.*$/, "") + target + "index.html";
    } else {
      location.href = target;
    }
  }
  /* true when the site is opened by double-clicking a file (no web server) */
  var LOCAL = location.protocol === "file:";
  function localLinks() {
    /* a web host serves "about/" as "about/index.html" by itself; a file preview needs it spelled out */
    Array.prototype.forEach.call(document.querySelectorAll("a[href]"), function (a) {
      var h = a.getAttribute("href");
      if (/^[a-z]+:|^#|^\/\//i.test(h)) return;
      var parts = h.split("#");
      if (/(^|\/)\.?$/.test(parts[0]) || /\/$/.test(parts[0])) {
        parts[0] = parts[0].replace(/\/?\.?$/, "/") + "index.html";
        if (parts[0].charAt(0) === "/") parts[0] = parts[0].slice(1);
        a.setAttribute("href", parts.join("#"));
      }
    });
  }

  /* Language pages never redirect on their own: search engines and ad landing pages
     must always get the page they asked for. Automatic detection lives only on "/". */
  var here = currentLang();

  document.addEventListener("DOMContentLoaded", function () {
    if (LOCAL) localLinks();
    /* 2. manual language switcher (select + mobile list) */
    Array.prototype.forEach.call(document.querySelectorAll("select.langsel"), function (sel) {
      sel.value = here;
      sel.addEventListener("change", function () { go(sel.value); });
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-golang]"), function (el) {
      el.addEventListener("click", function () { remember(el.getAttribute("data-golang")); });
    });

    /* 3. mobile menu */
    var tog = document.getElementById("menuToggle"), panel = document.getElementById("mobilePanel");
    if (tog && panel) {
      tog.addEventListener("click", function () {
        var open = panel.classList.toggle("open");
        tog.setAttribute("aria-expanded", open ? "true" : "false");
      });
      document.addEventListener("click", function (e) {
        if (panel.classList.contains("open") && !panel.contains(e.target) && !tog.contains(e.target)) {
          panel.classList.remove("open"); tog.setAttribute("aria-expanded", "false");
        }
      });
    }

    /* 4. cookie notice */
    var banner = document.getElementById("cookieBanner");
    if (banner) {
      var ok = null;
      try { ok = localStorage.getItem("inondacy_cookies"); } catch (e) {}
      if (!ok) { banner.classList.add("show"); }
      var btn = document.getElementById("cookieAccept");
      if (btn) btn.addEventListener("click", function () {
        try { localStorage.setItem("inondacy_cookies", "1"); } catch (e) {}
        banner.classList.remove("show");
      });
    }

    /* 5. forms — posted to the mail endpoint, inline feedback, no page reload */
    Array.prototype.forEach.call(document.querySelectorAll("form[data-endpoint]"), function (form) {
      var status = form.querySelector(".form-status");
      var submit = form.querySelector("button[type=submit]");
      var labelIdle = submit ? submit.textContent : "";
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }
        if (status) { status.className = "form-status"; status.textContent = ""; }
        if (submit) { submit.disabled = true; submit.textContent = form.getAttribute("data-sending") || "Sending…"; }
        var data = new FormData(form);
        var payload = {};
        data.forEach(function (v, k) { payload[k] = v; });
        var endpoint = form.getAttribute("data-endpoint");
        if (!endpoint) {
          /* No mail relay configured: hand the completed enquiry to WhatsApp,
             with the e-mail link under the form as the fallback. */
          var lines = [];
          data.forEach(function (v, k) { if (v && k !== "Consent") lines.push(k + ": " + v); });
          var text = encodeURIComponent((form.getAttribute("data-subject") || "Inonda LTD") + "\n" + lines.join("\n"));
          var wa = "https://wa.me/" + form.getAttribute("data-whatsapp") + "?text=" + text;
          window.open(wa, "_blank", "noopener");
          if (status) { status.className = "form-status ok"; status.textContent = form.getAttribute("data-wa-note"); status.setAttribute("data-wa-url", wa); }
          if (submit) { submit.disabled = false; submit.textContent = labelIdle; }
          return;
        }
        payload._subject = form.getAttribute("data-subject") || "Website enquiry — Inonda LTD";
        payload._template = "table";
        payload.Page = location.href;
        fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify(payload)
        }).then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
          .then(function (res) {
            var ok = res && (res.success === true || res.success === "true" || res.ok === true);
            if (ok) {
              if (status) { status.className = "form-status ok"; status.textContent = form.getAttribute("data-sent"); }
              form.reset();
            } else {
              throw new Error("endpoint");
            }
          })
          .catch(function () {
            if (status) { status.className = "form-status err"; status.textContent = form.getAttribute("data-error"); }
          })
          .then(function () {
            if (submit) { submit.disabled = false; submit.textContent = labelIdle; }
            if (status) { status.scrollIntoView({ block: "center", behavior: "smooth" }); }
          });
      });
    });

    /* 6. solid header after scrolling past the top of the page */
    var hdr = document.querySelector("header.site");
    function onScroll() { if (hdr) hdr.classList.toggle("solid", window.scrollY > 40); }
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

    /* 7. reveal on scroll */
    var rv = document.querySelectorAll(".rv");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
      }, { rootMargin: "0px 0px -8% 0px" });
      Array.prototype.forEach.call(rv, function (el) { io.observe(el); });
    } else { Array.prototype.forEach.call(rv, function (el) { el.classList.add("in"); }); }

    /* 8. hero video: only on screens and connections that can afford it */
    var vid = document.querySelector(".hero-media video[data-src]");
    if (vid) {
      var slow = navigator.connection && (navigator.connection.saveData || /2g/.test(navigator.connection.effectiveType || ""));
      var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!slow && !still) {
        var small = window.innerWidth < 760 && vid.getAttribute("data-src-sm");
        vid.src = small ? vid.getAttribute("data-src-sm") : vid.getAttribute("data-src");
        vid.addEventListener("playing", function () { vid.parentNode.classList.add("playing"); });
        var p = vid.play(); if (p && p.catch) p.catch(function () {});
      }
    }
  });
})();
