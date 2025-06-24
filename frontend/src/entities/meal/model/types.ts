export interface Ingredient {
    name: string,
    amount: number,
    unit: string,
    product_name: string,
    article: string
}

export interface Meal {
    type: string,
    dish: string,
    ingredients: Ingredient[],
    steps: string[]
}

export interface Day {
    meals: Meal[]
}

export interface MealPlanResponse {
    days: Day[]
}