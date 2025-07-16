export interface GenerateMealPlanRequest {
  userId: number;
  period: number;
  text: string;
  budget?: string;
  nutrition_goals?: string;
} 