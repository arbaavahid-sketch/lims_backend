import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { LangProvider, useLang } from "./i18n";
import { AuthProvider, useAuth } from "./auth";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Samples from "./pages/Samples";
import NewSample from "./pages/NewSample";
import SampleDetail from "./pages/SampleDetail";

// فقط کاربر واردشده اجازهٔ دیدن صفحات را دارد
function Protected({ children }) {
  const { user, ready } = useAuth();
  const { t } = useLang();
  if (!ready) return <p style={{ padding: 24 }}>{t("loading")}</p>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <LangProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<Layout />}>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<Protected><Samples /></Protected>} />
              <Route path="/samples/new" element={<Protected><NewSample /></Protected>} />
              <Route path="/samples/:id" element={<Protected><SampleDetail /></Protected>} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </LangProvider>
  );
}
