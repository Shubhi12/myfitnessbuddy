import { axiosClient } from "../../../core/api/axiosClient";

export interface AdminRegisterPayload {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  community_name: string;
  community_address: string;
  community_city: string;
  community_pincode: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AdminUser {
  id: number;
  email: string;
  full_name: string;
  role: string;
  community_id: number;
}

interface ValidationErrorItem {
  loc: (string | number)[];
  msg: string;
}

export async function registerAdmin(payload: AdminRegisterPayload): Promise<AuthTokens> {
  const body = {
    ...payload,
    phone: payload.phone?.trim() || undefined,
  };
  const { data } = await axiosClient.post<AuthTokens>("/auth/admin/register", body);
  return data;
}

export async function loginAdmin(email: string, password: string): Promise<AuthTokens> {
  const { data } = await axiosClient.post<AuthTokens>("/auth/admin/login", { email, password });
  return data;
}

export async function getCurrentUser(): Promise<AdminUser> {
  const { data } = await axiosClient.get<AdminUser>("/users/me");
  return data;
}

function formatFieldName(field: string): string {
  return field
    .replace(/^community_/, "community ")
    .replace(/^full_name$/, "full name")
    .replace(/_/g, " ");
}

export function getApiErrorMessage(error: unknown, fallback: string): string {
  if (typeof error === "object" && error !== null && "response" in error) {
    const response = (error as {
      response?: { data?: { error?: string; detail?: string | ValidationErrorItem[] } };
    }).response;
    const detail = response?.data?.detail;

    if (response?.data?.error) return response.data.error;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((item) => {
          const field = item.loc[item.loc.length - 1];
          const label = typeof field === "string" ? formatFieldName(field) : "field";
          return `${label}: ${item.msg}`;
        })
        .join("; ");
    }
  }
  return fallback;
}

export function isAdminAuthenticated(): boolean {
  const token = localStorage.getItem("access_token");
  if (!token) return false;

  try {
    const payload = JSON.parse(atob(token.split(".")[1])) as { role?: string };
    return payload.role === "admin";
  } catch {
    return false;
  }
}

export function clearAuthTokens(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}
