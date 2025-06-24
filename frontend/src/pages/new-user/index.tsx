import React, { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { setLocalStorageItem } from '@shared/lib/utils/local-storage';
import { SaveUserProfileForm } from '@features/save-user-profile/ui/SaveUserProfileForm';

export const NewUserPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialUserId = searchParams.get('user_id');

  useEffect(() => {
    if (initialUserId) {
      setLocalStorageItem('user_id', initialUserId);
    }
  }, [initialUserId]);

  return (
    <div className="new-user-page">
      <h1>Welcome, New User!</h1>
      <p>Please tell us about your food preferences. User ID: {initialUserId}</p>
      <SaveUserProfileForm />
    </div>
  );
}; 