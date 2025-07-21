import React, { useState } from 'react';
import { getLocalStorageItem } from '@shared/lib/utils/local-storage';
import { useGenerateMealPlan } from '@features/generate-meal-plan/model/useGenerateMealPlan';
import { Meal } from '@entities/meal/model/types';
import { MealPlanResponse } from '@entities/meal/model/types';
import styles from './HomePage.module.css';
// import { loadArticleImageMap, ArticleImageMap } from '@shared/lib/utils/articleImageMap';

export const HomePage: React.FC = () => {
  const userId = getLocalStorageItem('user_id');
  const { generate, loading, data, error } = useGenerateMealPlan();
  const [text, setText] = useState('');
  const [budget, setBudget] = useState('');
  const [nutritionGoals, setNutritionGoals] = useState('');
  const [submitted, setSubmitted] = useState(false);
  // const [articleImageMap, setArticleImageMap] = useState<ArticleImageMap>({});
  const [openIngredients, setOpenIngredients] = useState<number | null>(null);

  // useEffect(() => {
  //   loadArticleImageMap().then(setArticleImageMap);
  // }, []);

  if (!userId) {
    return (
      <div className={styles.container}>
        <h1>Добро пожаловать в Mealix!</h1>
        <p>Пожалуйста, войдите через Telegram-бота для использования сервиса.</p>
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

  // Helper to get meals array from response (either data.meals or data.days[0].meals)
  const getMeals = (data: MealPlanResponse | null): Meal[] => {
    if (!data) return [];
    if (Array.isArray((data as any).meals)) {
      return (data as any).meals as Meal[];
    }
    if (Array.isArray((data as any).days) && (data as any).days.length > 0) {
      return (data as any).days[0].meals as Meal[];
    }
    return [];
  };

  const meals = getMeals(data as MealPlanResponse);

  return (
    <div className={styles.container}>
      <h1>Сгенерируйте свой план питания</h1>
      <form onSubmit={handleGenerate} className={styles.form}>
        <label htmlFor="prefs">Пожелания (опционально):</label>
        <textarea
          id="prefs"
          value={text}
          onChange={e => setText(e.target.value)}
          rows={3}
          placeholder="Например: Хочу что-то легкое, без мяса, люблю итальянскую кухню..."
        />
        <label htmlFor="budget">Бюджет (опционально):</label>
        <input
          id="budget"
          type="text"
          value={budget}
          onChange={e => setBudget(e.target.value)}
          placeholder="Например: до 1000 рублей на день"
        />
        <label htmlFor="nutritionGoals">КБЖУ (опционально):</label>
        <input
          id="nutritionGoals"
          type="text"
          value={nutritionGoals}
          onChange={e => setNutritionGoals(e.target.value)}
          placeholder="Например: 2000 ккал, 100г белка, 70г жиров, 250г углеводов"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Генерируется...' : 'Сгенерировать план на 1 день'}
        </button>
      </form>
      {submitted && error && <p style={{ color: 'red', marginTop: 10 }}>{error}</p>}
      {submitted && meals.length > 0 && (
        <div className={styles.mealPlan}>
          <h2>План питания</h2>
          {meals.map((meal: Meal, idx: number) => (
            <div className={styles.meal} key={idx}>
              <div className={styles.mealTitle}>{meal.type && meal.type.charAt(0).toUpperCase() + meal.type.slice(1)}: {meal.dish}</div>
              <p
                style={{ marginBottom: 10, display: 'flex', alignItems: 'center', color: '#4CAF50' }}
                onClick={() => setOpenIngredients(openIngredients === idx ? null : idx)}
              >
                {openIngredients === idx ? 'Скрыть ингредиенты' : 'Смотреть ингредиенты'}
                {openIngredients === idx ?
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16" style={{transform: 'rotate(90deg)'}}>
                    <path fill-rule="evenodd" d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5"/>
                  </svg> 
                  :
                  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16" rotate="45" style={{transform: 'rotate(270deg)'}}>
                    <path fill-rule="evenodd" d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5"/>
                  </svg>
                }
              </p>
              {openIngredients === idx && (
                <div>
                  <b>Ингредиенты:</b>
                  <div className={styles.ingredientList}>
                    {meal.ingredients.map((ing, k) => {
                      // const imageUrl = articleImageMap[ing.article];
                      return (
                        <div className={styles.ingredientCard} key={k}>
                          {/* {imageUrl && (
                            <img
                              src={imageUrl}
                              alt={ing.name}
                              className={styles.ingredientImage}
                            />
                          )} */}
                          <div className={styles.ingredientName}>{ing.name}</div>
                          <div className={styles.ingredientAmount}>{ing.amount} {ing.unit}</div>
                          <div className={styles.ingredientProduct}>{ing.product_name}</div>
                          <a
                            href={`https://magnit.ru/product/${ing.article}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={styles.ingredientLink}
                          >
                            купить
                          </a>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
              {meal.steps && meal.steps.length > 0 && (
                <div>
                  <b>Шаги:</b>
                  <ol className={styles.steps}>
                    {meal.steps.map((step: string, sidx: number) => (
                      <li key={sidx}>{step}</li>
                    ))}
                  </ol>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}; 