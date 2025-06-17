# Frontend

This directory contains the frontend application for Mealix, built using a modern JavaScript framework React and structured according to the **Feature-Sliced Design (FSD)** methodology.

## Feature-Sliced Design (FSD) Architecture

### Core Principles

```ruby
mealix/frontend/src/
├── app/
│   ├── index.tsx         # entering app point
│   ├── App.tsx           # root component
│   ├── router/           # routing settings
│   └── styles/           # global styles
│       └── index.css
│
├── processes/            # user scenarios managing
│   └── user-onboarding/  
│       ├── lib/
│       ├── model/
│       └── ui/
│           └── UserOnboardingWizard.tsx
│
├── pages/                # pages components
│   ├── settings/
│   │   └── index.tsx     
│   ├── meal-plan-generation/
│   │   └── index.tsx     
│   └── saved-menus/
│       └── index.tsx     
│
├── widgets/              # widgets
│   ├── meal-plan-display/
│   │   └── index.tsx     
│   ├── shopping-list/
│   │   └── index.tsx     
│   └── profile-settings-form/
│       └── index.tsx     
│
├── features/             # main logic implementation
│   ├── auth/             
│   │   ├── sign-in/
│   │   └── sign-up/
│   ├── generate-meal-plan/
│   │   └── index.tsx     
│   ├── save-meal-plan/
│   │   └── index.tsx     
│   ├── allergy-selection/
│   │   └── index.tsx     
│   └── cuisine-preference-picker/
│       └── index.tsx     
│
├── entities/             # main logic entities
│   ├── user/
│   │   ├── model/        
│   │   ├── api/          
│   │   └── ui/           
│   │       └── UserAvatar.tsx
│   ├── meal/
│   │   ├── model/
│   │   ├── api/
│   │   └── ui/
│   │       └── MealCard.tsx
│   └── ingredient/
│       ├── model/
│       ├── api/
│       └── ui/
│
└── shared/               # UI
    ├── ui/               
    │   ├── Button/
    │   ├── Input/
    │   └── Icon/
    ├── lib/              
    │   └── utils/
    ├── config/           
    │   └── api.ts
    └── types/            
        └── common.ts
```

### FSD Layers (from top to bottom / most specific to most generic)

1.  **`app`**:
    *   **Purpose:** Application-level logic and global configuration. Contains global styles, routing, and setup for the entire application.
    *   **Contents:** Global providers, root layout, application entry point.
    *   **Dependencies:** Can depend on `processes`, `pages`, `shared`.
    *   **Example for Mealix:** Main `App` component, global CSS, routing configuration.

2.  **`processes`**:
    *   **Purpose:** Manages long-running inter-page scenarios or complex cross-feature interactions.
    *   **Contents:** State management for complex flows, orchestrating multiple features/widgets across different pages.
    *   **Dependencies:** Can depend on `pages`, `widgets`, `features`, `entities`, `shared`.
    *   **Example for Mealix:** A multi-step wizard for initial user profile setup that spans several "pages".

3.  **`pages`**:
    *   **Purpose:** Top-level components representing distinct pages/routes of the application.
    *   **Contents:** Composes `widgets` and `features` to form a complete view.
    *   **Dependencies:** Can depend on `widgets`, `features`, `entities`, `shared`.
    *   **Example for Mealix:** `SettingsPage`, `MealPlanGenerationPage`, `SavedMenusPage`.

4.  **`widgets`**:
    *   **Purpose:** Reusable UI blocks that combine multiple `features` or `entities` to solve a specific UI problem. They often encapsulate some interaction logic.
    *   **Contents:** Complex UI components (e.g., a "User Profile Card" widget which might include "Edit Profile" feature and "Avatar" entity).
    *   **Dependencies:** Can depend on `features`, `entities`, `shared`.
    *   **Example for Mealix:** `MealPlanDisplayWidget`, `ShoppingListWidget`, `ProfileSettingsFormWidget`.

5.  **`features`**:
    *   **Purpose:** Encapsulate a specific business capability or user story, often involving interaction with an API or managing local state related to that capability. They are interactive.
    *   **Contents:** Buttons that trigger actions, forms that submit data, interactive lists.
    *   **Dependencies:** Can depend on `entities`, `shared`.
    *   **Example for Mealix:** `GenerateMealPlanButton`, `SaveMealPlanButton`, `AllergySelectionForm`, `CuisinePreferencePicker`.

6.  **`entities`**:
    *   **Purpose:** Represents core domain concepts and their associated logic and UI. They are the building blocks for `features` and `widgets`. Typically, they don't have business logic, but rather domain logic (e.g., data models, interfaces, basic CRUD operations).
    *   **Contents:** Data models (interfaces/types), API clients for a specific entity, basic display components for that entity.
    *   **Dependencies:** Can depend on `shared`.
    *   **Example for Mealix:** `User` (data model, basic API calls related to user data), `Meal` (data model, basic display component for a meal item), `Ingredient` (data model, display).

7.  **`shared`**:
    *   **Purpose:** Generic, reusable code that is independent of any specific feature or domain.
    *   **Contents:** UI Kit (buttons, inputs, icons), utility functions, constants, global types, API base configuration.
    *   **Dependencies:** No dependencies on other application layers (only external libraries).
    *   **Example for Mealix:** `Button` component, `formatDate` utility, `API_BASE_URL` constant, common TypeScript types.

### Slices within Layers

Each layer (except `app` and `shared`) is further divided into "slices" based on business domain. For example:
`src/
  features/
    auth/
      login/
      signup/
    meal-generation/
    ...
  entities/
    user/
    meal/
    ...
`

### Import Rule

Imports are strictly controlled:
*   **Inside a slice:** Any import is allowed.
*   **Between slices of the same layer:** Imports are forbidden (e.g., `features/auth` cannot import from `features/meal-generation`).
*   **Between different layers:** Only downward imports are allowed (e.g., `features` can import from `entities` or `shared`, but `entities` cannot import from `features`).

### Getting Started

To begin developing, refer to the `src` directory structure and place your code according to the FSD principles outlined above. Each folder within a layer (e.g., `entities/user`) should contain its own `index.ts` file to export its public API, facilitating clean imports.

```typescript
// Example: src/entities/user/index.ts
export * from './model';
export * from './ui';
// ... other exports
```

