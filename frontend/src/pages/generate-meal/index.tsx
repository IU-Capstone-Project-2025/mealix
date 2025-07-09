import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useGenerateMealPlan } from '@features/generate-meal-plan/model/useGenerateMealPlan';
import { Meal } from '@entities/meal/model/types';
import styles from './IngredientCard.module.css';
import { loadArticleImageMap, ArticleImageMap } from '@shared/lib/utils/articleImageMap';

export const GenerateMealPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const period = Number(searchParams.get('period')) || 1;
  const userIdRaw = localStorage.getItem('user_id');
  const userId = userIdRaw ? Number(userIdRaw) : 0;
  const { generate, loading, data, error } = useGenerateMealPlan();
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [articleImageMap, setArticleImageMap] = useState<ArticleImageMap>({});

  console.log(import.meta.env.VITE_API_URL)
  console.log(articleImageMap[0]);

  useEffect(() => {
    loadArticleImageMap().then(setArticleImageMap);
  }, []);

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    generate({ userId, period, text });
    console.log('кнопка нажата')
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
          {/* Если есть data.days (старый/расширенный формат) */}
          {Array.isArray(data.days) ? (
            data.days.map((day, i) => (
              <div key={i}>
                <h2>День {i + 1}</h2>
                {day.meals.map((meal, j) => (
                  <div key={j} style={{ marginBottom: 16 }}>
                    <h3>{meal.type}: {meal.dish}</h3>
                    <div>
                      <b>Ингредиенты:</b>
                      <div className={styles.ingredientList}>
                        {meal.ingredients.map((ing, k) => {
                          // const imageUrl = articleImageMap[ing.article];
                          return (
                            <div
                              key={k}
                              className={styles.ingredientCard}
                            >
                              {/* {imageUrl && (
                                <img
                                  src={imageUrl}
                                  alt={ing.name}
                                  style={{ width: '100%', borderRadius: 6, marginBottom: 6 }}
                                />
                              )} */}
                              <div className={styles.ingredientName}>{ing.name}</div>
                              <div className={styles.ingredientAmount}>
                                {ing.amount} {ing.unit}
                              </div>
                              <div className={styles.ingredientProduct}>
                                {ing.product_name}
                              </div>
                              <a
                                href={`https://magnit.ru/product/${ing.article}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={styles.ingredientLink}
                              >
                                ссылка для покупки
                              </a>
                            </div>
                          );
                        })}
                      </div>
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
            ))
          ) : null}

          {/* Если есть data.meals (текущий формат) */}
          {Array.isArray((data as any).meals) ? (
            <div>
              <h2>День 1</h2>
              {((data as unknown as { meals: Meal[] }).meals).map((meal: Meal, j: number) => (
                <div key={j} style={{ marginBottom: 16 }}>
                  <h3>{meal.type}: {meal.dish}</h3>
                  <div>
                    <b>Ингредиенты:</b>
                    <div className={styles.ingredientList}>
                      {meal.ingredients.map((ing, k) => {
                        // const imageUrl = articleImageMap[ing.article];
                        return (
                          <div
                            key={k}
                            className={styles.ingredientCard}
                          >
                            {/* {imageUrl && (
                              <img
                                src={imageUrl}
                                alt={ing.name}
                                style={{ width: '100%', borderRadius: 6, marginBottom: 6 }}
                              />
                            )} */}
                            <div className={styles.ingredientName}>{ing.name}</div>
                            <div className={styles.ingredientAmount}>
                              {ing.amount} {ing.unit}
                            </div>
                            <div className={styles.ingredientProduct}>
                              {ing.product_name}
                            </div>
                            <a
                              href={`https://magnit.ru/product/${ing.article}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className={styles.ingredientLink}
                            >
                              ссылка для покупки
                            </a>
                          </div>
                        );
                      })}
                    </div>
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
          ) : null}
        </div>
      )}
    </div>
  );
}; 