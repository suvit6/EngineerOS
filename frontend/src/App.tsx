import { FormEvent, useState } from "react";
import { API_BASE_URL } from "./config";
import "./App.css";

function App() {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [registerMessage, setRegisterMessage] = useState("");
  const [registerLoading, setRegisterLoading] = useState(false);

  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginMessage, setLoginMessage] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  const onRegisterSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setRegisterLoading(true);
    setRegisterMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
          full_name: fullName,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setRegisterMessage(data.detail ?? "Registration failed");
        return;
      }

      setRegisterMessage(data.message ?? "User registered successfully");
      setEmail("");
      setFullName("");
      setPassword("");
    } catch {
      setRegisterMessage("Could not connect to backend");
    } finally {
      setRegisterLoading(false);
    }
  };

  const onLoginSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoginLoading(true);
    setLoginMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: loginEmail,
          password: loginPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setLoginMessage(data.detail ?? "Login failed");
        return;
      }

      setLoginMessage(data.message ?? "Login successful");
      setLoginEmail("");
      setLoginPassword("");
    } catch {
      setLoginMessage("Could not connect to backend");
    } finally {
      setLoginLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 560, margin: "40px auto", padding: 16 }}>
      <h1>EngineerOS - Auth</h1>
      <p>Sprint 2: Register and Login integration.</p>

      <section style={{ marginTop: 24 }}>
        <h2>Register</h2>
        <form onSubmit={onRegisterSubmit} style={{ display: "grid", gap: 12 }}>
          <input
            type="text"
            placeholder="Full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password (min 8 chars)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            required
          />
          <button type="submit" disabled={registerLoading}>
            {registerLoading ? "Creating..." : "Create account"}
          </button>
        </form>
        {registerMessage && <p style={{ marginTop: 12 }}>{registerMessage}</p>}
      </section>

      <section style={{ marginTop: 32 }}>
        <h2>Login</h2>
        <form onSubmit={onLoginSubmit} style={{ display: "grid", gap: 12 }}>
          <input
            type="email"
            placeholder="Email"
            value={loginEmail}
            onChange={(e) => setLoginEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={loginPassword}
            onChange={(e) => setLoginPassword(e.target.value)}
            minLength={8}
            required
          />
          <button type="submit" disabled={loginLoading}>
            {loginLoading ? "Logging in..." : "Login"}
          </button>
        </form>
        {loginMessage && <p style={{ marginTop: 12 }}>{loginMessage}</p>}
      </section>
    </main>
  );
}

export default App;