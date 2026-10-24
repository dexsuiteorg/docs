// DexSuite docs: clips play only while on screen (as on the project page).
document.addEventListener("DOMContentLoaded", function () {
  var vids = document.querySelectorAll("video.ds-video, .ds-tile video");
  if (!("IntersectionObserver" in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else { v.pause(); }
    });
  }, { threshold: 0.35 });
  vids.forEach(function (v) { v.muted = true; v.playsInline = true; io.observe(v); });
});
