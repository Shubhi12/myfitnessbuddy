import { Alert, Box, Button, CircularProgress, TextField } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getApiErrorMessage, loginAdmin } from "../api/authApi";
import AuthLayout, { AuthFooterLink } from "../components/AuthLayout";

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const tokens = await loginAdmin(email, password);
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      navigate("/");
    } catch (err) {
      setError(getApiErrorMessage(err, "Invalid admin credentials"));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthLayout
      title="My Fitness Buddy Admin"
      subtitle="Sign in with your administrator account."
      footer={<AuthFooterLink text="Need an admin account?" linkText="Sign up" to="/signup" />}
    >
      <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
        <TextField
          label="Admin Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />
        {error && <Alert severity="error">{error}</Alert>}
        <Button type="submit" variant="contained" size="large" disabled={submitting}>
          {submitting ? <CircularProgress size={24} color="inherit" /> : "Sign In"}
        </Button>
      </Box>
    </AuthLayout>
  );
}
