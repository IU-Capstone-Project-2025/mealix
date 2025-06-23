import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { setLocalStorageItem } from '@shared/lib/utils/local-storage';
import { UserId, UserPreferences, UserProfile } from '@entities/user/model/types';

export const NewUserPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialUserId = searchParams.get('user_id') as UserId;

  const [name, setName] = useState<string>('');
  const [allergies, setAllergies] = useState<string>('');
  const [dietaryRestrictions, setDietaryRestrictions] = useState<string>('');
  const [favoriteCuisines, setFavoriteCuisines] = useState<string>('');
  const [cookingTime, setCookingTime] = useState<string>('');
  const [period, setPeriod] = useState<string>('');

  useEffect(() => {
    if (initialUserId) {
      setLocalStorageItem('user_id', initialUserId);
    }
  }, [initialUserId]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    if (!initialUserId) {
      alert("User ID not found in URL. Please open the app from Telegram.");
      return;
    }

    const preferences: UserPreferences = {
      name,
      allergies: allergies.split(',').map(item => item.trim()).filter(Boolean),
      dietaryRestrictions: dietaryRestrictions.split(',').map(item => item.trim()).filter(Boolean),
      favoriteCuisines: favoriteCuisines.split(',').map(item => item.trim()).filter(Boolean),
      cookingTime,
      period,
    };

    const userProfile: UserProfile = {
      userId: initialUserId,
      preferences,
    };

    setLocalStorageItem('user_profile', JSON.stringify(userProfile));
    alert("Profile saved successfully!");
    navigate('/'); // Redirect to home page
  };

  return (
    <div className="new-user-page">
      <h1>Welcome, New User!</h1>
      <p>Please tell us about your food preferences. User ID: {initialUserId}</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Your Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="allergies">Allergies (comma-separated):</label>
          <input
            type="text"
            id="allergies"
            value={allergies}
            onChange={(e) => setAllergies(e.target.value)}
            placeholder="e.g., peanuts, dairy"
          />
        </div>

        <div className="form-group">
          <label htmlFor="dietaryRestrictions">Dietary Restrictions (comma-separated):</label>
          <input
            type="text"
            id="dietaryRestrictions"
            value={dietaryRestrictions}
            onChange={(e) => setDietaryRestrictions(e.target.value)}
            placeholder="e.g., vegetarian, vegan, gluten-free"
          />
        </div>

        <div className="form-group">
          <label htmlFor="favoriteCuisines">Favorite Cuisines (comma-separated):</label>
          <input
            type="text"
            id="favoriteCuisines"
            value={favoriteCuisines}
            onChange={(e) => setFavoriteCuisines(e.target.value)}
            placeholder="e.g., Italian, Mexican, Asian"
          />
        </div>

        <div className="form-group">
          <label htmlFor="cookingTime">Preferred Cooking Time (e.g., 30-60 min):</label>
          <input
            type="text"
            id="cookingTime"
            value={cookingTime}
            onChange={(e) => setCookingTime(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="period">Meal Plan Period (e.g., day, 3 days, week):</label>
          <input
            type="text"
            id="period"
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            required
          />
        </div>

        <button type="submit">Save Preferences</button>
      </form>
    </div>
  );
}; 