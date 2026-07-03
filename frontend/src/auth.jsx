// مدیریت ورود/خروج و کاربر جاری
import { createContext, useContext, useEffect, useState } from "react";
import { api } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // اگر توکن معتبری در localStorage باشد، کاربر را بازیابی کن
    if (!localStorage.getItem("token")) {
      setReady(true);
      return;
    }
    api("/me")
      .then(setUser)
      .catch(() => localStorage.removeItem("token"))
      .finally(() => setReady(true));
  }, []);

  async function login(username, password) {
    const data = await api("/login", {
      method: "POST",
      body: { username, password },
      form: true,
    });
    localStorage.setItem("token", data.access_token);
    const me = await api("/me");
    setUser(me);
    return me;
  }

  function logout() {
    localStorage.removeItem("token");
    setUser(null);
  }

  // آیا کاربر یکی از این نقش‌ها را دارد؟
  const hasRole = (...roles) => user && (roles.includes(user.role) || user.role === "admin");

  return (
    <AuthContext.Provider value={{ user, ready, login, logout, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
