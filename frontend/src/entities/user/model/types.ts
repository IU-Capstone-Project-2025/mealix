export type UserId = string;

export interface UserPreferences {
  name: string;
  allergies: string[];
  dietaryRestrictions: string[];
  favoriteCuisines: string[];
  cookingTime: string;
  period: string;
}

export interface UserProfile {
  userId: UserId;
  preferences: UserPreferences;
} 