import React, { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useGenerateMealPlan } from '@features/generate-meal-plan/model/useGenerateMealPlan';

export const GenerateMealPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const period = Number(searchParams.get('period')) || 1;
  const userId = Number(localStorage.getItem('user_id')) || 0;
  const { generate, loading, data, error } = useGenerateMealPlan();

  useEffect(() => {
    generate({ userId, period, text: '' });
    // eslint-disable-next-line
  }, [userId, period]);

  return (
    <div>
      <h1>Генерация плана на {period} {period === 1 ? 'день' : 'дня'}</h1>
      {loading && <p>Генерируется...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data && (
        <div>
          {data.days.map((day, i) => (
            <div key={i}>
              <h2>День {i + 1}</h2>
              {day.meals.map((meal, j) => (
                <div key={j} style={{ marginBottom: 16 }}>
                  <h3>{meal.type}: {meal.dish}</h3>
                  <div>
                    <b>Ингредиенты:</b>
                    <ul>
                      {meal.ingredients.map((ing, k) => (
                        <li key={k}>
                          {ing.name} — {ing.amount} {ing.unit} ({ing.product_name}, {ing.article})
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <b>Шаги:</b>
                    <ol>
                      {meal.steps.map((step, k) => (
                        <li key={k}>{step}</li>
                      ))}
                    </ol>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}; 