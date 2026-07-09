import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getApiErrorMessage, registerAdmin } from "../api/authApi";
import AuthLayout, { AuthFooterLink } from "../components/AuthLayout";

export default function SignupPage() {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [communityName, setCommunityName] = useState("");
  const [communityAddress, setCommunityAddress] = useState("");
  const [communityCity, setCommunityCity] = useState("");
  const [communityPincode, setCommunityPincode] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (communityAddress.trim().length < 5) {
      setError("Address must be at least 5 characters");
      return;
    }

    if (communityPincode.trim().length < 5) {
      setError("Pincode must be at least 5 characters");
      return;
    }

    setSubmitting(true);
    try {
      const tokens = await registerAdmin({
        email: email.trim(),
        password,
        full_name: fullName.trim(),
        phone: phone.trim() || undefined,
        community_name: communityName.trim(),
        community_address: communityAddress.trim(),
        community_city: communityCity.trim(),
        community_pincode: communityPincode.trim(),
      });
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      navigate("/");
    } catch (err) {
      setError(getApiErrorMessage(err, "Admin registration failed. Please check your details."));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthLayout
      title="Create Admin Account"
      subtitle="Register as a community administrator and set up your gated community."
      footer={<AuthFooterLink text="Already have an account?" linkText="Sign in" to="/login" />}
    >
      <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
        <Typography variant="subtitle2" color="text.secondary">
          Admin Details
        </Typography>
        <TextField
          label="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
          autoComplete="name"
        />
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
        <TextField
          label="Phone (optional)"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          autoComplete="tel"
        />

        <Divider sx={{ my: 1 }} />

        <Typography variant="subtitle2" color="text.secondary">
          Community Details
        </Typography>
        <TextField
          label="Community Name"
          value={communityName}
          onChange={(e) => setCommunityName(e.target.value)}
          required
          placeholder="e.g. Green Valley Residency"
        />
        <TextField
          label="Address"
          value={communityAddress}
          onChange={(e) => setCommunityAddress(e.target.value)}
          required
          multiline
          minRows={2}
          helperText="Minimum 5 characters"
        />
        <TextField
          label="City"
          value={communityCity}
          onChange={(e) => setCommunityCity(e.target.value)}
          required
        />
        <TextField
          label="Pincode"
          value={communityPincode}
          onChange={(e) => setCommunityPincode(e.target.value)}
          required
          inputProps={{ maxLength: 10, minLength: 5 }}
          helperText="Minimum 5 characters"
        />

        <Divider sx={{ my: 1 }} />

        <Typography variant="subtitle2" color="text.secondary">
          Security
        </Typography>
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="new-password"
          helperText="Minimum 8 characters"
        />
        <TextField
          label="Confirm Password"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          autoComplete="new-password"
        />

        {error && <Alert severity="error">{error}</Alert>}
        <Button type="submit" variant="contained" size="large" disabled={submitting}>
          {submitting ? <CircularProgress size={24} color="inherit" /> : "Create Admin Account"}
        </Button>
      </Box>
    </AuthLayout>
  );
}
