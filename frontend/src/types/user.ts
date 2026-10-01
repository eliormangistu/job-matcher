export interface User {
  id: number;
  google_id: string | null;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface UserData {
  user: User;
}
