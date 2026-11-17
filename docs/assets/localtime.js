// Shows the next Saturday 10 am Toronto class in the visitor's own time zone.
try {
  (function () {
    var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (!tz || tz === "America/Toronto") return;
    function off(d) {
      var v = new Intl.DateTimeFormat("en-US", { timeZone: "America/Toronto", timeZoneName: "shortOffset" })
        .formatToParts(d).find(function (p) { return p.type === "timeZoneName"; }).value;
      var m = v.match(/GMT([+-]\d+)(?::(\d+))?/);
      if (!m) return -300;
      var h = parseInt(m[1], 10);
      return h * 60 + (m[2] ? (h < 0 ? -1 : 1) * parseInt(m[2], 10) : 0);
    }
    var now = new Date();
    var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/Toronto", year: "numeric", month: "numeric", day: "numeric", weekday: "short", hour: "numeric", hourCycle: "h23" }).formatToParts(now);
    var g = function (t) { return parts.find(function (x) { return x.type === t; }).value; };
    var wd = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(g("weekday").slice(0, 3));
    var add = (6 - wd + 7) % 7;
    if (add === 0 && parseInt(g("hour"), 10) >= 11) add = 7;
    var base = new Date(Date.UTC(+g("year"), +g("month") - 1, +g("day") + add, 10, 0));
    var start = new Date(base.getTime() - off(base) * 60000);
    var s = new Intl.DateTimeFormat(undefined, { weekday: "long", hour: "numeric", minute: "2-digit", timeZoneName: "short" }).format(start);
    var el = document.getElementById("localtime");
    if (!el) return;
    el.textContent = "Joining online? The next class is " + s + " your time.";
    el.hidden = false;
  })();
} catch (e) {}
