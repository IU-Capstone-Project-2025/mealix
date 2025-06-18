import React from 'react';
import { getLocalStorageItem } from '@shared/lib/utils/local-storage';

export const HomePage: React.FC = () => {
  const userId = getLocalStorageItem('user_id');
  const userProfile = getLocalStorageItem('user_profile');

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
    </div>
  );
}; 