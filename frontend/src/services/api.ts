import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile: UserProfile;
  date_joined: string;
}

export interface UserProfile {
  email_frequency: 'daily' | 'twice_week' | 'thrice_week' | 'weekly' | 'never';
  receive_emails: boolean;
  created_at: string;
  updated_at: string;
}

export interface Interest {
  id: number;
  name: string;
  slug: string;
  description: string;
  created_at: string;
}

export interface Article {
  id: number;
  title: string;
  url: string;
  summary: string;
  content?: string;
  author: string;
  published_date: string;
  source_name: string;
  interest_names: string[];
  image_url: string;
  scraped_at: string;
}

export interface UserArticle {
  id: number;
  article: Article;
  is_read: boolean;
  is_bookmarked: boolean;
  is_recommended: boolean;
  created_at: string;
  updated_at: string;
}

// API Endpoints
export const authAPI = {
  register: (data: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name?: string;
    last_name?: string;
  }) => api.post('/users/', data),

  login: (username: string, password: string) =>
    api.post('/auth/login/', { username, password }),

  logout: () => api.post('/auth/logout/'),

  getCurrentUser: () => api.get<User>('/users/me/'),

  updateProfile: (data: Partial<User>) =>
    api.patch<User>('/users/me/', data),
};

export const profileAPI = {
  getProfile: () => api.get<UserProfile>('/profiles/me/'),

  updateProfile: (data: Partial<UserProfile>) =>
    api.patch<UserProfile>('/profiles/me/', data),
};

export const interestsAPI = {
  getAll: () => api.get<Interest[]>('/interests/'),

  getBySlug: (slug: string) => api.get<Interest>(`/interests/${slug}/`),

  getUserInterests: () => api.get('/user-interests/my_interests/'),

  addUserInterest: (interestId: number) =>
    api.post('/user-interests/', { interest_id: interestId }),

  removeUserInterest: (id: number) =>
    api.delete(`/user-interests/${id}/`),
};

export const articlesAPI = {
  getAll: (params?: {
    interest?: string;
    source?: number;
    search?: string;
    page?: number;
  }) => api.get<{ results: Article[]; count: number }>('/articles/', { params }),

  getById: (id: number) => api.get<Article>(`/articles/${id}/`),

  getRecommended: () => api.get<Article[]>('/articles/recommended/'),
};

export const userArticlesAPI = {
  getAll: () => api.get<UserArticle[]>('/user-articles/'),

  getBookmarked: () => api.get<UserArticle[]>('/user-articles/bookmarked/'),

  getRead: () => api.get<UserArticle[]>('/user-articles/read/'),

  toggleBookmark: (articleId: number, isBookmarked: boolean) =>
    api.post('/user-articles/', {
      article_id: articleId,
      is_bookmarked: isBookmarked,
    }),

  markAsRead: (articleId: number) =>
    api.post('/user-articles/', {
      article_id: articleId,
      is_read: true,
    }),
};

export default api;
