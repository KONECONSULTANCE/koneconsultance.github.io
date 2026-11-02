(function () {
  "use strict";
  var BASE = "";
  var PHOTOS = [
    { f: "dioila-01-famille-kaladougou", a: "dioila", t: ["famille"], c: "Photo de famille — acteurs de la commune de Kaladougou (atelier de Dioïla)", wide: true },
    { f: "dioila-02-famille-ngaradougou", a: "dioila", t: ["famille"], c: "Photo de famille — acteurs de la commune de N'Garadougou (atelier de Dioïla)", wide: true },
    { f: "dioila-03-banniere", a: "dioila", t: [], c: "Atelier de Dioïla — bannière du projet WPHF · ONU Femmes · ONG KILABO" },
    { f: "dioila-04-salle", a: "dioila", t: [], c: "Atelier de Dioïla — séance de travail en salle" },
    { f: "dioila-05-travaux", a: "dioila", t: [], c: "Atelier de Dioïla — travaux de groupe" },
    { f: "dioila-06-hangar", a: "dioila", t: [], c: "Atelier de Dioïla — échanges en groupe sous le hangar" },
    { f: "dioila-07-restitution", a: "dioila", t: [], c: "Atelier de Dioïla — restitution des travaux de groupe" },
    { f: "dioila-08-projection", a: "dioila", t: [], c: "Atelier de Dioïla — présentation et projection" },
    { f: "degnekoro-01-famille-degnekoro", a: "degnekoro", t: ["famille"], c: "Photo de famille — acteurs de la commune de Dègnékoro (atelier de Dégnékoro)", wide: true },
    { f: "degnekoro-02-famille-kilidougou", a: "degnekoro", t: ["famille"], c: "Photo de famille — acteurs de la commune de Kilidougou (atelier de Dégnékoro)", wide: true },
    { f: "degnekoro-03-groupe-kilidougou", a: "degnekoro", t: [], c: "Atelier de Dégnékoro — groupe de travail de Kilidougou" },
    { f: "degnekoro-04-travaux", a: "degnekoro", t: [], c: "Atelier de Dégnékoro — travaux de groupe" },
    { f: "degnekoro-05-ombre", a: "degnekoro", t: [], c: "Atelier de Dégnékoro — travail de groupe à l'ombre des arbres" },
    { f: "degnekoro-06-pleniere", a: "degnekoro", t: [], c: "Atelier de Dégnékoro — exposé en séance plénière" },
    { f: "degnekoro-07-echanges", a: "degnekoro", t: [], c: "Atelier de Dégnékoro — échanges entre participants" }
  ];

  var list = document.getElementById("gallery");
  var chips = document.querySelectorAll(".pcu-chip");
  var lb = document.getElementById("lightbox");
  var lbImg = document.getElementById("lb-img");
  var lbCap = document.getElementById("lb-cap");
  var current = [];   // photos visibles
  var idx = 0;
  var lastFocus = null;

  function matches(p, flt) { return flt === "all" || p.a === flt || p.t.indexOf(flt) !== -1; }

  function render(flt) {
    current = PHOTOS.filter(function (p) { return matches(p, flt); });
    list.innerHTML = "";
    current.forEach(function (p, i) {
      var li = document.createElement("li");
      if (p.wide && (flt === "all" || flt === "famille")) li.className = "wide";
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Agrandir : " + p.c);
      var img = document.createElement("img");
      img.src = BASE + p.f + "-thumb.webp";
      img.alt = p.c;
      img.loading = "lazy";
      img.width = 640; img.height = 360;
      var cap = document.createElement("span");
      cap.className = "cap";
      cap.textContent = p.c.replace(/ \(atelier de [^)]+\)$/, "");
      b.appendChild(img); b.appendChild(cap);
      b.addEventListener("click", function () { open(i); });
      li.appendChild(b);
      list.appendChild(li);
    });
  }

  function counts() {
    ["all", "dioila", "degnekoro", "famille"].forEach(function (k) {
      var el = document.querySelector('[data-count="' + k + '"]');
      if (el) el.textContent = PHOTOS.filter(function (p) { return matches(p, k); }).length;
    });
  }

  chips.forEach(function (ch) {
    ch.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("is-active"); c.setAttribute("aria-pressed", "false"); });
      ch.classList.add("is-active"); ch.setAttribute("aria-pressed", "true");
      render(ch.getAttribute("data-filter"));
    });
  });

  function show(i) {
    idx = (i + current.length) % current.length;
    var p = current[idx];
    lbImg.src = BASE + p.f + ".webp";
    lbImg.alt = p.c;
    lbCap.textContent = p.c + "  ·  " + (idx + 1) + " / " + current.length + "  ·  © Z. Doumbia_ONG KILABO";
    // précharge la suivante
    var n = new Image(); n.src = BASE + current[(idx + 1) % current.length].f + ".webp";
  }
  function open(i) {
    lastFocus = document.activeElement;
    lb.hidden = false; document.body.style.overflow = "hidden";
    show(i);
    lb.querySelector(".lb-close").focus();
  }
  function close() {
    lb.hidden = true; document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  lb.querySelector(".lb-close").addEventListener("click", close);
  lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
  lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowLeft") show(idx - 1);
    else if (e.key === "ArrowRight") show(idx + 1);
  });
  var x0 = null;
  lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
  });

  counts();
  render("all");
})();
