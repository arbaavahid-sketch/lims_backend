// صفحهٔ ورود
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLang } from "../i18n";
import { useAuth } from "../auth";
import { errMsg } from "../api";

export default function Login() {
  const { t, lang } = useLang();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(username, password);
      navigate("/");
    } catch (err) {
      setError(errMsg(err, lang));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrap">
      <form className="card login-card" onSubmit={submit}>
        <h1 className="login-title">🧪 {t("appTitle")}</h1>
        <h2>{t("login")}</h2>
        {error && <div className="alert">{error}</div>}
        <label>
          {t("username")}
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus />
        </label>
        <label>
          {t("password")}
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button className="btn primary" disabled={busy}>
          {busy ? "…" : t("signIn")}
        </button>
      </form>
    </div>
  );
}
