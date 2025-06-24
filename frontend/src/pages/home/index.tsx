import React from 'react';
import { getLocalStorageItem } from '@shared/lib/utils/local-storage';
import { useNavigate } from 'react-router-dom';

export const HomePage: React.FC = () => {
  const userId = getLocalStorageItem('user_id');
  const userProfile = getLocalStorageItem('user_profile');
  const navigate = useNavigate();

  const handleGenerate = (period: number) => {
    navigate(`/generate-meal?period=${period}`);
  };

  return (
    <div>
      <h1>Welcome to Mealix!</h1>
      <p>Your User ID: {userId}</p>
      {userProfile && (
        <div>
          <h2>Your Profile:</h2>
          <pre>{JSON.stringify(JSON.parse(userProfile), null, 2)}</pre>
        </div>
      )}
      <p>This is your main dashboard. More features will be added here.</p>
      <button onClick={() => handleGenerate(1)}>Сгенерировать план на 1 день</button>
      <button onClick={() => handleGenerate(3)}>Сгенерировать план на 3 дня</button>
    </div>
  );
}; 