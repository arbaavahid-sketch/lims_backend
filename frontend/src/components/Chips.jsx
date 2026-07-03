// چیپ‌های رنگی وضعیت و حکم انطباق
import { useLang } from "../i18n";

const STATUS_COLORS = {
  received: "#5c6bc0",
  in_testing: "#f9a825",
  completed: "#2e7d32",
  archived: "#757575",
  rejected: "#c62828",
  pending: "#90a4ae",
  in_progress: "#f9a825",
  result_entered: "#0288d1",
  reviewed: "#7b1fa2",
  approved: "#2e7d32",
};

export function StatusChip({ value, kind = "st" }) {
  const { t } = useLang();
  return (
    <span className="chip" style={{ background: STATUS_COLORS[value] || "#607d8b" }}>
      {t(`${kind}_${value}`)}
    </span>
  );
}

const CONF_COLORS = {
  conform: "#2e7d32",
  nonconform: "#c62828",
  conditional: "#b26a00",
  not_evaluated: "#757575",
};

export function ConformityChip({ value }) {
  const { t } = useLang();
  if (!value) return null;
  return (
    <span className="chip" style={{ background: CONF_COLORS[value] || "#607d8b" }}>
      {t("cf_" + value)}
    </span>
  );
}
