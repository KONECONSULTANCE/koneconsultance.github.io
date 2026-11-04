/* =========================================================
   Sidi Koné — Site vitrine consultant
   JavaScript vanilla — navigation, animations, formulaire
   ========================================================= */
(function () {
  "use strict";

  var LANG = document.documentElement.lang === "en" ? "en" : "fr";
  var STRINGS = {
    fr: {
      navOpen: "Ouvrir le menu de navigation",
      navClose: "Fermer le menu de navigation",
      errorName: "Merci d'indiquer votre nom.",
      errorEmail: "Merci d'indiquer une adresse e-mail valide.",
      errorMessage: "Votre message doit contenir au moins 10 caractères.",
      formInvalid: "Merci de corriger les champs indiqués avant d'envoyer votre message.",
      formNotConfigured: "Le formulaire n'est pas encore connecté à un service d'envoi. Voir README.md pour l'activer.",
      formSuccess: "Merci, votre message a bien été envoyé.",
      formError: "Une erreur est survenue. Merci de réessayer ou d'écrire directement par e-mail.",
    },
    en: {
      navOpen: "Open navigation menu",
      navClose: "Close navigation menu",
      errorName: "Please enter your name.",
      errorEmail: "Please enter a valid e-mail address.",
      errorMessage: "Your message must be at least 10 characters long.",
      formInvalid: "Please correct the highlighted fields before sending your message.",
      formNotConfigured: "The form isn't connected to a delivery service yet. See README.md to enable it.",
      formSuccess: "Thank you, your message has been sent.",
      formError: "Something went wrong. Please try again or e-mail directly.",
    },
  };
  var T = STRINGS[LANG];

  /* ---------- En-tête : fond au scroll + lien actif ---------- */
  var header = document.getElementById("site-header");
  var sections = Array.prototype.slice.call(document.querySelectorAll("main > section[id]"));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".main-nav a[href^='#']"));

  function onScroll() {
    if (window.scrollY > 12) {
      header.classList.add("is-scrolled");
    } else {
      header.classList.remove("is-scrolled");
    }

    var current = sections[0];
    var scrollPos = window.scrollY + 130;
    sections.forEach(function (section) {
      if (section.offsetTop <= scrollPos) {
        current = section;
      }
    });

    navLinks.forEach(function (link) {
      var isActive = link.getAttribute("href") === "#" + current.id;
      link.classList.toggle("is-active", isActive);
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  var navToggle = document.getElementById("nav-toggle");
  var mainNav = document.getElementById("main-nav");

  navToggle.addEventListener("click", function () {
    var isOpen = mainNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navToggle.setAttribute(
      "aria-label",
      isOpen ? T.navClose : T.navOpen
    );
  });

  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      mainNav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });

  /* ---------- Révélation au défilement ---------- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if ("IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* ---------- Compteurs animés (chiffres clés) ---------- */
  var counters = Array.prototype.slice.call(document.querySelectorAll("[data-counter]"));
  function animateCounter(el) {
    var target = parseInt(el.getAttribute("data-target"), 10) || 0;
    var suffix = el.getAttribute("data-suffix") || "";
    var duration = 1200;
    var start = null;

    function step(timestamp) {
      if (!start) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      var value = Math.round(progress * target);
      el.textContent = value + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    }
    window.requestAnimationFrame(step);
  }

  if ("IntersectionObserver" in window && counters.length) {
    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(function (el) {
      counterObserver.observe(el);
    });
  } else {
    counters.forEach(function (el) {
      el.textContent = el.getAttribute("data-target") + (el.getAttribute("data-suffix") || "");
    });
  }

  /* ---------- Accordéon formations complémentaires ---------- */
  var accordionTriggers = Array.prototype.slice.call(document.querySelectorAll(".accordion-trigger"));

  function setPanelState(trigger, isOpen) {
    var panel = document.getElementById(trigger.getAttribute("aria-controls"));
    trigger.setAttribute("aria-expanded", String(isOpen));
    if (isOpen) {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } else {
      panel.style.maxHeight = "0px";
    }
  }

  accordionTriggers.forEach(function (trigger) {
    setPanelState(trigger, trigger.getAttribute("aria-expanded") === "true");
    trigger.addEventListener("click", function () {
      var isOpen = trigger.getAttribute("aria-expanded") === "true";
      setPanelState(trigger, !isOpen);
    });
  });

  /* ---------- Année courante (pied de page) ---------- */
  var yearEl = document.getElementById("current-year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* ---------- Formulaire de contact : validation + envoi ---------- */
  var form = document.getElementById("contact-form");
  var statusEl = document.getElementById("form-status");

  function setError(fieldId, message) {
    var errorEl = document.querySelector("[data-error-for='" + fieldId + "']");
    if (errorEl) errorEl.textContent = message || "";
  }

  function validateForm() {
    var valid = true;
    var name = document.getElementById("f-name");
    var email = document.getElementById("f-email");
    var message = document.getElementById("f-message");

    setError("f-name", "");
    setError("f-email", "");
    setError("f-message", "");

    if (!name.value.trim()) {
      setError("f-name", T.errorName);
      valid = false;
    }

    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.value.trim() || !emailPattern.test(email.value.trim())) {
      setError("f-email", T.errorEmail);
      valid = false;
    }

    if (!message.value.trim() || message.value.trim().length < 10) {
      setError("f-message", T.errorMessage);
      valid = false;
    }

    return valid;
  }

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      statusEl.textContent = "";
      statusEl.removeAttribute("data-state");

      if (!validateForm()) {
        statusEl.textContent = T.formInvalid;
        statusEl.setAttribute("data-state", "error");
        return;
      }

      var actionUrl = form.getAttribute("action");
      var isConfigured = actionUrl && actionUrl.indexOf("example.com") === -1 && actionUrl.trim() !== "";

      if (!isConfigured) {
        /* TODO: à personnaliser — le formulaire n'est pas encore branché à un service d'envoi.
           Voir README.md, section "Brancher le formulaire de contact" (Formspree recommandé). */
        statusEl.textContent = T.formNotConfigured;
        statusEl.setAttribute("data-state", "error");
        return;
      }

      var submitBtn = form.querySelector("button[type='submit']");
      submitBtn.disabled = true;

      fetch(actionUrl, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      })
        .then(function (response) {
          if (response.ok) {
            form.reset();
            statusEl.textContent = T.formSuccess;
            statusEl.setAttribute("data-state", "success");
          } else {
            throw new Error("Erreur d'envoi");
          }
        })
        .catch(function () {
          statusEl.textContent = T.formError;
          statusEl.setAttribute("data-state", "error");
        })
        .finally(function () {
          submitBtn.disabled = false;
        });
    });
  }
})();

/* Bandeau « Partager » (LinkedIn + copier le lien) */
(function () {
  "use strict";
  var p = location.pathname;
  if (/contact\.html$|apercu\.html$|\/partage\//.test(p)) return;
  var main = document.getElementById("main"); if (!main) return;
  var en = (document.documentElement.lang || "fr").indexOf("en") === 0;
  var canon = document.querySelector('link[rel="canonical"]');
  var url = (canon && canon.href) || (location.origin + location.pathname);
  var bar = document.createElement("div"); bar.className = "share-bar";
  var inner = '<div class="container share-bar-inner"><span>' + (en ? "Found this useful? Share it:" : "Cette page vous a intéressé ? Partagez-la :") + '</span>' +
    '<a class="btn btn-outline" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url) + '">' + (en ? "Share on LinkedIn" : "Partager sur LinkedIn") + '</a>' +
    '<button type="button" class="btn btn-outline share-copy">' + (en ? "Copy link" : "Copier le lien") + '</button></div>';
  bar.innerHTML = inner; main.appendChild(bar);
  var b = bar.querySelector(".share-copy");
  b.addEventListener("click", function () {
    function ok() { b.textContent = en ? "Link copied" : "Lien copié"; setTimeout(function () { b.textContent = en ? "Copy link" : "Copier le lien"; }, 2500); }
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(ok, function () { window.prompt("", url); }); }
    else { window.prompt("", url); }
  });
})();
