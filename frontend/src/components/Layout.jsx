// قالب کلی صفحات: نوار بالا + سوییچر زبان + خروج
import { Link, Outlet, useNavigate } from "react-router-dom";
import { useLang } from "../i18n";
import { useAuth } from "../auth";

export default function Layout() {
  const { lang, setLang, t } = useLang();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand">🧪 {t("appShort")}</Link>
        <div className="topbar-actions">
          {user && (
            <span className="user-chip">
              {user.full_name} · {t("role_" + user.role)}
            </span>
          )}
          <button
            className="btn ghost"
            onClick={() => setLang(lang === "fa" ? "en" : "fa")}
            title="Switch language"
          >
            {lang === "fa" ? "EN" : "فا"}
          </button>
          {user && (
            <button
              className="btn ghost"
              onClick={() => { logout(); navigate("/login"); }}
            >
              {t("logout")}
            </button>
          )}
        </div>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
