import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { getLocalStorageItem, setLocalStorageItem } from '@shared/lib/utils/local-storage';
import { HomePage } from '@pages/home';
import { NewUserPage } from '@pages/new-user';

const AuthWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const userId = getLocalStorageItem('user_id');

  useEffect(() => {

    switch (location.pathname) {
      case '/':
        if (!userId) { 
          navigate('/notfound') 
        }
        break;
      case '/newuser':
        if (userId) {
          navigate('/');
          break;
        }

        const queryParams = new URLSearchParams(location.search);
        const userIdFromUrl = queryParams.get('user_id');

        if (userIdFromUrl) {
          setLocalStorageItem('user_id', userIdFromUrl);
        };
        if (!userIdFromUrl) navigate('/notfound');
        break;
    }
  }, [location.pathname, location.search, navigate]);

  return <>{children}</>;
};

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthWrapper>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/newuser" element={<NewUserPage />} />
          <Route path="*" element={<h1>404: Not Found<br />Пожалуйста, переходите на сайт через Telegram-бота</h1>} />
        </Routes>
      </AuthWrapper>
    </BrowserRouter>
  );
}; 