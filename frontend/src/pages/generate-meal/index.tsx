import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useGenerateMealPlan } from '@features/generate-meal-plan/model/useGenerateMealPlan';

export const GenerateMealPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const period = Number(searchParams.get('period')) || 1;
  const userIdRaw = localStorage.getItem('user_id');
  const userId = userIdRaw ? Number(userIdRaw) : 0;
  const { generate, loading, data, error } = useGenerateMealPlan();
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    generate({ userId, period, text });
  };

  return (
    <div>
      <h1>Генерация плана на {period} {period === 1 ? 'день' : 'дня'}</h1>
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
        <button type="submit" disabled={loading || !userId}>
          {loading ? 'Генерируется...' : 'Сгенерировать'}
        </button>
      </form>
      {submitted && error && <p style={{ color: 'red' }}>{error}</p>}
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