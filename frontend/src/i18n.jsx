// دوزبانگی فارسی/انگلیسی با چرخش خودکار RTL/LTR
import { createContext, useContext, useEffect, useState } from "react";

const DICT = {
  fa: {
    appTitle: "سامانه مدیریت اطلاعات آزمایشگاه نفتی",
    appShort: "LIMS نفتی",
    login: "ورود به سامانه",
    username: "نام کاربری",
    password: "رمز عبور",
    signIn: "ورود",
    logout: "خروج",
    samples: "نمونه‌ها",
    newSample: "ثبت نمونهٔ جدید",
    sampleCode: "کد نمونه",
    product: "فرآورده",
    productType: "نوع فرآورده",
    grade: "گرید",
    batch: "شمارهٔ بچ",
    samplingPoint: "نقطهٔ نمونه‌گیری",
    source: "منبع (مخزن/واحد)",
    customer: "مشتری/واحد",
    status: "وضعیت",
    receivedDate: "تاریخ دریافت",
    save: "ذخیره",
    cancel: "انصراف",
    tests: "آزمون‌ها",
    assignTest: "افزودن آزمون",
    method: "روش آزمون",
    value: "مقدار",
    unit: "واحد",
    spec: "حد پذیرش",
    conformity: "حکم انطباق",
    enterResult: "ثبت نتیجه",
    review: "بازبینی",
    approve: "تأیید نهایی",
    downloadCoA: "دانلود گواهی آنالیز (PDF)",
    loading: "در حال بارگذاری…",
    noData: "داده‌ای موجود نیست",
    role: "نقش",
    // وضعیت نمونه
    st_received: "دریافت‌شده",
    st_in_testing: "در حال آزمون",
    st_completed: "تکمیل‌شده",
    st_archived: "بایگانی",
    st_rejected: "مردود",
    // وضعیت آزمون
    as_pending: "در انتظار",
    as_in_progress: "در حال انجام",
    as_result_entered: "نتیجه ثبت شد",
    as_reviewed: "بازبینی شد",
    as_approved: "تأیید شد",
    // حکم انطباق
    cf_conform: "منطبق",
    cf_nonconform: "نامنطبق",
    cf_conditional: "مشروط",
    cf_not_evaluated: "ارزیابی‌نشده",
    // نقش‌ها
    role_admin: "مدیر سیستم",
    role_analyst: "آزمایش‌گر",
    role_reviewer: "بازبین",
    role_approver: "تأییدکننده",
    role_viewer: "بیننده",
  },
  en: {
    appTitle: "Petroleum Laboratory Information Management System",
    appShort: "Petro LIMS",
    login: "Sign in",
    username: "Username",
    password: "Password",
    signIn: "Sign in",
    logout: "Logout",
    samples: "Samples",
    newSample: "New sample",
    sampleCode: "Sample code",
    product: "Product",
    productType: "Product type",
    grade: "Grade",
    batch: "Batch No.",
    samplingPoint: "Sampling point",
    source: "Source (tank/unit)",
    customer: "Customer/unit",
    status: "Status",
    receivedDate: "Received",
    save: "Save",
    cancel: "Cancel",
    tests: "Tests",
    assignTest: "Assign test",
    method: "Test method",
    value: "Value",
    unit: "Unit",
    spec: "Spec.",
    conformity: "Conformity",
    enterResult: "Enter result",
    review: "Review",
    approve: "Approve",
    downloadCoA: "Download CoA (PDF)",
    loading: "Loading…",
    noData: "No data",
    role: "Role",
    st_received: "Received",
    st_in_testing: "In testing",
    st_completed: "Completed",
    st_archived: "Archived",
    st_rejected: "Rejected",
    as_pending: "Pending",
    as_in_progress: "In progress",
    as_result_entered: "Result entered",
    as_reviewed: "Reviewed",
    as_approved: "Approved",
    cf_conform: "Conforms",
    cf_nonconform: "Nonconforming",
    cf_conditional: "Conditional",
    cf_not_evaluated: "Not evaluated",
    role_admin: "Admin",
    role_analyst: "Analyst",
    role_reviewer: "Reviewer",
    role_approver: "Approver",
    role_viewer: "Viewer",
  },
};

const LangContext = createContext(null);

export function LangProvider({ children }) {
  const [lang, setLang] = useState(localStorage.getItem("lang") || "fa");

  useEffect(() => {
    localStorage.setItem("lang", lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "fa" ? "rtl" : "ltr";
  }, [lang]);

  const t = (key) => DICT[lang][key] ?? key;
  return (
    <LangContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LangContext.Provider>
  );
}

export const useLang = () => useContext(LangContext);
