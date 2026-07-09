import { Navigate, Route, Routes } from "react-router-dom";
import { isAdminAuthenticated } from "../../features/auth/api/authApi";
import LoginPage from "../../features/auth/pages/LoginPage";
import SignupPage from "../../features/auth/pages/SignupPage";
import DashboardPage from "../../features/dashboard/pages/DashboardPage";
import MainLayout from "../../shared/layouts/MainLayout";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!isAdminAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
