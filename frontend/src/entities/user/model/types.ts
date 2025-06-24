export type UserId = string;

export interface UserPreferences {
  allergies: string[];
  dietaryRestrictions: string[];
  favoriteCuisines: string[];
}

export interface UserProfile {
  userId: UserId;
  name: string;
  preferences: UserPreferences;
} 