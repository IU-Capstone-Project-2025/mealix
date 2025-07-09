import { useState } from 'react';
import { GenerateMealPlanRequest } from './types';
import { MealPlanResponse } from '@entities/meal/model/types';
import { apiPOST } from '@shared/lib/utils/api';

export function useGenerateMealPlan() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<MealPlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generate = async (req: GenerateMealPlanRequest) => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const result = await apiPOST<GenerateMealPlanRequest, MealPlanResponse>('/meals', req);
      console.log(result)
      setData(result);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return { generate, loading, data, error };
} 