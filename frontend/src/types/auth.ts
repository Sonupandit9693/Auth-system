export interface User {
  user_id: string;
  email: string;
  username: string;
  is_verified: boolean;
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email_or_username: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}