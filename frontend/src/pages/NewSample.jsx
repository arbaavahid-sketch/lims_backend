// فرم ثبت نمونهٔ جدید
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, errMsg } from "../api";
import { useLang } from "../i18n";

const PRODUCT_TYPES = [
  "crude_oil", "gasoline", "gasoil", "kerosene", "jet_fuel",
  "fuel_oil", "naphtha", "lpg", "bitumen", "lube_oil", "other",
];

export default function NewSample() {
  const { t, lang } = useLang();
  const navigate = useNavigate();
  const [grades, setGrades] = useState([]);
  const [error, setError] = useState("");
  const [f, setF] = useState({
    sample_code: "", product_name: "", product_type: "gasoil",
    product_grade_id: "", batch_number: "", sampling_point: "",
    source: "", customer: "",
  });

  useEffect(() => {
    api("/grades/").then(setGrades).catch(() => {});
  }, []);

  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      const body = { ...f };
      if (!body.product_grade_id) delete body.product_grade_id;
      const s = await api("/samples/", { method: "POST", body });
      navigate(`/samples/${s.id}`);
    } catch (err) {
      setError(errMsg(err, lang));
    }
  }

  return (
    <div>
      <div className="page-head"><h1>{t("newSample")}</h1></div>
      <form className="card form-grid" onSubmit={submit}>
        {error && <div className="alert span2">{error}</div>}
        <label>{t("sampleCode")} *
          <input required value={f.sample_code} onChange={set("sample_code")} placeholder="GO-1404-001" />
        </label>
        <label>{t("product")} *
          <input required value={f.product_name} onChange={set("product_name")} />
        </label>
        <label>{t("productType")}
          <select value={f.product_type} onChange={set("product_type")}>
            {PRODUCT_TYPES.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
        </label>
        <label>{t("grade")}
          <select value={f.product_grade_id} onChange={set("product_grade_id")}>
            <option value="">—</option>
            {grades.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}
          </select>
        </label>
        <label>{t("batch")}
          <input value={f.batch_number} onChange={set("batch_number")} />
        </label>
        <label>{t("samplingPoint")}
          <input value={f.sampling_point} onChange={set("sampling_point")} />
        </label>
        <label>{t("source")}
          <input value={f.source} onChange={set("source")} />
        </label>
        <label>{t("customer")}
          <input value={f.customer} onChange={set("customer")} />
        </label>
        <div className="span2 form-actions">
          <button type="button" className="btn ghost" onClick={() => navigate(-1)}>{t("cancel")}</button>
          <button className="btn primary">{t("save")}</button>
        </div>
      </form>
    </div>
  );
}
