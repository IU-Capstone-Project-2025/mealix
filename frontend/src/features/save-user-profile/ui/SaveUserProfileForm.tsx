import React, { useState } from 'react';
import { UserPreferences, UserProfile } from '@entities/user/model/types';
import { setLocalStorageItem } from '@shared/lib/utils/local-storage';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { saveUserProfile } from '@entities/user/api/userApi';

export const SaveUserProfileForm: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialUserId = Number(searchParams.get('user_id'));

  const [name, setName] = useState<string>('');
  const [allergies, setAllergies] = useState<string>('');
  const [dietaryRestrictions, setDietaryRestrictions] = useState<string>('');
  const [favoriteCuisines, setFavoriteCuisines] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setSuccess(false);

    if (!initialUserId || isNaN(initialUserId)) {
      setError("User ID not found in URL. Please open the app from Telegram.");
      return;
    }

    const preferences: UserPreferences = {
      allergies: allergies.split(',').map(item => item.trim()).filter(Boolean),
      dietaryRestrictions: dietaryRestrictions.split(',').map(item => item.trim()).filter(Boolean),
      favoriteCuisines: favoriteCuisines.split(',').map(item => item.trim()).filter(Boolean),
    };

    const userProfile: UserProfile = {
      userId: initialUserId,
      name: name,
      preferences,
    };

    setLoading(true);
    try {
      setLocalStorageItem('user_profile', JSON.stringify(userProfile));
      const result = await saveUserProfile(userProfile);
      console.log(result.data)
      setSuccess(true);
      alert("Profile saved successfully!");
      navigate('/');
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
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
      <button type="submit" disabled={loading}>Save Preferences</button>
      {error && <div style={{ color: 'red', marginTop: 10 }}>{error}</div>}
      {success && <div style={{ color: 'green', marginTop: 10 }}>Profile saved!</div>}
    </form>
  );
}; 