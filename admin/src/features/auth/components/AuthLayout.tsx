import { Box, Paper, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

interface AuthLayoutProps {
  title: string;
  subtitle: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export default function AuthLayout({ title, subtitle, children, footer }: AuthLayoutProps) {
  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" px={2}>
      <Paper sx={{ p: 4, width: "100%", maxWidth: 480 }}>
        <Typography variant="h5" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          {subtitle}
        </Typography>
        {children}
        {footer}
      </Paper>
    </Box>
  );
}

export function AuthFooterLink({ text, linkText, to }: { text: string; linkText: string; to: string }) {
  return (
    <Typography variant="body2" textAlign="center" sx={{ mt: 2 }}>
      {text}{" "}
      <Typography component={RouterLink} to={to} variant="body2" color="primary" sx={{ textDecoration: "none" }}>
        {linkText}
      </Typography>
    </Typography>
  );
}
