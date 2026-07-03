// داشبورد نمونه‌ها
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, errMsg } from "../api";
import { useLang } from "../i18n";
import { useAuth } from "../auth";
import { StatusChip } from "../components/Chips";

export default function Samples() {
  const { t, lang } = useLang();
  const { hasRole } = useAuth();
  const [samples, setSamples] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/samples/")
      .then(setSamples)
      .catch((e) => setError(errMsg(e, lang)));
  }, [lang]);

  if (error) return <div className="alert">{error}</div>;
  if (!samples) return <p>{t("loading")}</p>;

  return (
    <div>
      <div className="page-head">
        <h1>{t("samples")}</h1>
        {hasRole("analyst") && (
          <Link className="btn primary" to="/samples/new">＋ {t("newSample")}</Link>
        )}
      </div>
      <div className="card">
        {samples.length === 0 ? (
          <p className="muted">{t("noData")}</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>{t("sampleCode")}</th>
                <th>{t("product")}</th>
                <th>{t("batch")}</th>
                <th>{t("status")}</th>
                <th>{t("receivedDate")}</th>
              </tr>
            </thead>
            <tbody>
              {samples.map((s) => (
                <tr key={s.id}>
                  <td><Link to={`/samples/${s.id}`} className="code-link">{s.sample_code}</Link></td>
                  <td>{s.product_name}</td>
                  <td>{s.batch_number || "—"}</td>
                  <td><StatusChip value={s.status} /></td>
                  <td dir="ltr">{s.received_date?.slice(0, 16).replace("T", " ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
