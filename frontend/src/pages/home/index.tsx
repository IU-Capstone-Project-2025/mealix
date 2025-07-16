import React, { useState } from 'react';
import { getLocalStorageItem } from '@shared/lib/utils/local-storage';
import { useGenerateMealPlan } from '@features/generate-meal-plan/model/useGenerateMealPlan';

export const HomePage: React.FC = () => {
  const userId = getLocalStorageItem('user_id');
  const userProfile = getLocalStorageItem('user_profile');
  const { generate, loading, data, error } = useGenerateMealPlan();
  const [text, setText] = useState('');
  const [budget, setBudget] = useState('');
  const [nutritionGoals, setNutritionGoals] = useState('');
  const [submitted, setSubmitted] = useState(false);

  if (!userId) {
    return (
      <div>
        <h1>Welcome to Mealix!</h1>
        <p>Пожалуйста, войдите через Telegram-бота для доступа к функционалу.</p>
      </div>
    );
  }

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    generate({
      userId: Number(userId),
      period: 1,
      text,
      budget,
      nutrition_goals: nutritionGoals,
    });
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
      <form onSubmit={handleGenerate} style={{ marginBottom: 24 }}>
        <label htmlFor="prefs">Ваши пожелания (опционально):</label>
        <textarea
          id="prefs"
          value={text}
          onChange={e => setText(e.target.value)}
          rows={3}
          style={{ width: '100%', marginBottom: 12 }}
          placeholder="Например: Хочу что-то легкое, без мяса, люблю итальянскую кухню..."
        />
        <label htmlFor="budget">Бюджет (опционально):</label>
        <input
          id="budget"
          type="text"
          value={budget}
          onChange={e => setBudget(e.target.value)}
          style={{ width: '100%', marginBottom: 12 }}
          placeholder="Например: до 1000 рублей на день"
        />
        <label htmlFor="nutritionGoals">КБЖУ (опционально):</label>
        <input
          id="nutritionGoals"
          type="text"
          value={nutritionGoals}
          onChange={e => setNutritionGoals(e.target.value)}
          style={{ width: '100%', marginBottom: 12 }}
          placeholder="Например: 2000 ккал, 100г белка, 70г жиров, 250г углеводов"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Генерируется...' : 'Сгенерировать план на 1 день'}
        </button>
      </form>
      {submitted && error && <p style={{ color: 'red' }}>{error}</p>}
      {submitted && data && (
        <div style={{ marginTop: 24 }}>
          <h2>Сгенерированный план:</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}; 