// لایهٔ ارتباط با بک‌اند / Backend API layer
const BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function api(path, { method = "GET", body, form = false } = {}) {
  const headers = {};
  const token = localStorage.getItem("token");
  if (token) headers.Authorization = "Bearer " + token;

  let payload;
  if (body !== undefined) {
    if (form) {
      headers["Content-Type"] = "application/x-www-form-urlencoded";
      payload = new URLSearchParams(body);
    } else {
      headers["Content-Type"] = "application/json";
      payload = JSON.stringify(body);
    }
  }

  const res = await fetch(BASE + path, { method, headers, body: payload });

  if (!res.ok) {
    let detail;
    try {
      detail = (await res.json()).detail;
    } catch {
      detail = { fa: "خطای سرور", en: "Server error" };
    }
    throw { status: res.status, detail };
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/pdf")) return res.blob();
  return res.json();
}

// پیام خطا را به زبان فعال برمی‌گرداند / error message in active language
export function errMsg(err, lang) {
  const d = err?.detail;
  if (!d) return lang === "fa" ? "خطای ناشناخته" : "Unknown error";
  if (typeof d === "string") return d;
  if (Array.isArray(d)) return d.map((x) => x.msg).join("; "); // خطای اعتبارسنجی FastAPI
  return d[lang] || d.fa || d.en;
}
