// جزئیات نمونه + چرخهٔ کاری آزمون‌ها (ثبت نتیجه ← بازبینی ← تأیید ← CoA)
import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, errMsg } from "../api";
import { useLang } from "../i18n";
import { useAuth } from "../auth";
import { StatusChip, ConformityChip } from "../components/Chips";

export default function SampleDetail() {
  const { id } = useParams();
  const { t, lang } = useLang();
  const { hasRole } = useAuth();

  const [sample, setSample] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [results, setResults] = useState([]);
  const [methods, setMethods] = useState([]);
  const [error, setError] = useState("");
  const [newMethodId, setNewMethodId] = useState("");
  const [valueInputs, setValueInputs] = useState({});

  const load = useCallback(async () => {
    try {
      const [s, a, r, m] = await Promise.all([
        api(`/samples/${id}`),
        api(`/test-methods/assignments/${id}`),
        api(`/results/by-sample/${id}`),
        api("/test-methods/"),
      ]);
      setSample(s); setAssignments(a); setResults(r); setMethods(m);
    } catch (e) {
      setError(errMsg(e, lang));
    }
  }, [id, lang]);

  useEffect(() => { load(); }, [load]);

  async function act(fn) {
    setError("");
    try { await fn(); await load(); }
    catch (e) { setError(errMsg(e, lang)); }
  }

  const assignTest = () => act(() =>
    api("/test-methods/assignments", {
      method: "POST",
      body: { sample_id: id, test_method_id: newMethodId },
    }));

  const submitResult = (assignmentId) => act(() =>
    api("/results/", {
      method: "POST",
      body: { assignment_id: assignmentId, value: parseFloat(valueInputs[assignmentId]) },
    }));

  const review = (resultId) => act(() => api(`/results/${resultId}/review`, { method: "POST" }));
  const approve = (resultId) => act(() => api(`/results/${resultId}/approve`, { method: "POST" }));

  async function downloadCoA() {
    setError("");
    try {
      const blob = await api(`/samples/${id}/coa`);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `CoA-${sample.sample_code}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(errMsg(e, lang));
    }
  }

  if (error && !sample) return <div className="alert">{error}</div>;
  if (!sample) return <p>{t("loading")}</p>;

  const methodById = Object.fromEntries(methods.map((m) => [m.id, m]));
  const resultByAssignment = Object.fromEntries(results.map((r) => [r.assignment_id, r]));
  const specText = (r) => {
    if (r.applied_spec_min != null && r.applied_spec_max != null)
      return `${r.applied_spec_min} – ${r.applied_spec_max}`;
    if (r.applied_spec_min != null) return `≥ ${r.applied_spec_min}`;
    if (r.applied_spec_max != null) return `≤ ${r.applied_spec_max}`;
    return "—";
  };
  const assignedIds = new Set(assignments.map((a) => a.test_method_id));

  return (
    <div>
      <div className="page-head">
        <h1 dir="ltr">{sample.sample_code}</h1>
        <StatusChip value={sample.status} />
      </div>
      {error && <div className="alert">{error}</div>}

      {/* مشخصات نمونه */}
      <div className="card info-grid">
        <div><span className="muted">{t("product")}:</span> {sample.product_name}</div>
        <div><span className="muted">{t("batch")}:</span> {sample.batch_number || "—"}</div>
        <div><span className="muted">{t("samplingPoint")}:</span> {sample.sampling_point || "—"}</div>
        <div><span className="muted">{t("source")}:</span> {sample.source || "—"}</div>
        <div><span className="muted">{t("customer")}:</span> {sample.customer || "—"}</div>
        <div><span className="muted">{t("receivedDate")}:</span> <span dir="ltr">{sample.received_date?.slice(0, 16).replace("T", " ")}</span></div>
      </div>

      {/* آزمون‌ها */}
      <div className="page-head">
        <h2>{t("tests")}</h2>
        {sample.status === "completed" && (
          <button className="btn primary" onClick={downloadCoA}>⬇ {t("downloadCoA")}</button>
        )}
      </div>
      <div className="card">
        {hasRole("analyst") && (
          <div className="assign-row">
            <select value={newMethodId} onChange={(e) => setNewMethodId(e.target.value)}>
              <option value="">{t("method")}…</option>
              {methods.filter((m) => !assignedIds.has(m.id)).map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name} ({m.standard_ref || m.code})
                </option>
              ))}
            </select>
            <button className="btn" disabled={!newMethodId} onClick={assignTest}>
              ＋ {t("assignTest")}
            </button>
          </div>
        )}

        {assignments.length === 0 ? (
          <p className="muted">{t("noData")}</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>{t("method")}</th>
                <th>{t("status")}</th>
                <th>{t("value")}</th>
                <th>{t("spec")}</th>
                <th>{t("conformity")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {assignments.map((a) => {
                const m = methodById[a.test_method_id];
                const r = resultByAssignment[a.id];
                return (
                  <tr key={a.id}>
                    <td>{m ? `${m.name} (${m.standard_ref || m.code})` : a.test_method_id}</td>
                    <td><StatusChip value={a.status} kind="as" /></td>
                    <td dir="ltr">{r ? `${r.value} ${r.unit || ""}` : "—"}</td>
                    <td dir="ltr">{r ? specText(r) : "—"}</td>
                    <td>{r && <ConformityChip value={r.conformity} />}</td>
                    <td className="row-actions">
                      {!r && hasRole("analyst") && (
                        <span className="result-entry">
                          <input
                            type="number" step="any" dir="ltr"
                            placeholder={t("value")}
                            value={valueInputs[a.id] || ""}
                            onChange={(e) => setValueInputs({ ...valueInputs, [a.id]: e.target.value })}
                          />
                          <button className="btn small" disabled={!valueInputs[a.id]}
                            onClick={() => submitResult(a.id)}>
                            {t("enterResult")}
                          </button>
                        </span>
                      )}
                      {r && a.status === "result_entered" && hasRole("reviewer") && (
                        <button className="btn small" onClick={() => review(r.id)}>{t("review")}</button>
                      )}
                      {r && a.status === "reviewed" && hasRole("approver") && (
                        <button className="btn small primary" onClick={() => approve(r.id)}>{t("approve")}</button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
