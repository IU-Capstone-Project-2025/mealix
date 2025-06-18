# Frontend

This directory contains the frontend application for Mealix, built using a modern JavaScript framework React and structured according to the **Feature-Sliced Design (FSD)** methodology.

## Feature-Sliced Design (FSD) Architecture

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