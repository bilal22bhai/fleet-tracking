const API = "http://localhost:8000";
const MOVING_KMH = 3;   // is se zyada speed = chal rahi hai

function getToken() { return localStorage.getItem("token"); }
function requireLogin() { if (!getToken()) location.href = "login.html"; }
function logout() { localStorage.removeItem("token"); location.href = "login.html"; }

async function api(path) {
  const res = await fetch(API + path, { headers: { Authorization: "Bearer " + getToken() } });
  if (res.status === 401) { logout(); return; }
  if (!res.ok) throw new Error("Request failed: " + res.status);
  return res.json();
}

async function login(email, password) {
  const res = await fetch(API + "/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Wrong email or password. Check them and try again.");
  localStorage.setItem("token", (await res.json()).access_token);
}

function newMap(elId) {
  const el = document.getElementById(elId);
  if (typeof L === "undefined") {
    el.innerHTML = '<p class="map-msg">Map library did not load. Check your internet connection and reload.</p>';
    throw new Error("Leaflet not loaded");
  }
  const map = L.map(elId, { zoomControl: false }).setView([31.52, 74.35], 12);
  L.control.zoom({ position: "bottomright" }).addTo(map);

  // CARTO ab API key maangta hai, is liye seedha OpenStreetMap use kar rahe hain (free, key nahi chahiye)
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors", maxZoom: 19,
  }).addTo(map);

  setTimeout(() => map.invalidateSize(), 200);
  window.addEventListener("resize", () => map.invalidateSize());
  return map;
}

function isMoving(car) { return (car.last_speed || 0) > MOVING_KMH; }

function plateIcon(car) {
  const cls = isMoving(car) ? "go" : "stop";
  return L.divIcon({
    className: "pin-wrap", iconSize: [0, 0],
    html: `<div class="plate pin ${cls}">${esc(car.plate_number)}</div>`,
  });
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function fmtTime(iso) { return iso ? new Date(iso + "Z").toLocaleString([], { dateStyle: "medium", timeStyle: "short" }) : "No data yet"; }

function timeAgo(iso) {
  if (!iso) return "No data yet";
  const s = Math.max(0, (Date.now() - new Date(iso + "Z")) / 1000);
  if (s < 60) return "Just now";
  if (s < 3600) return Math.floor(s / 60) + " min ago";
  if (s < 86400) return Math.floor(s / 3600) + " h ago";
  return Math.floor(s / 86400) + " d ago";
}

function distanceKm(points) {
  const R = 6371, rad = d => d * Math.PI / 180;
  let total = 0;
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1], b = points[i];
    const dLat = rad(b.lat - a.lat), dLng = rad(b.lng - a.lng);
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
    total += 2 * R * Math.asin(Math.sqrt(h));
  }
  return total;
}
