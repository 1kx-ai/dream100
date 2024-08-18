# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Project Structure

src/
│
├── components/
│   ├── common/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Modal.jsx
│   │   └── ...
│   │
│   ├── layout/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── Sidebar.jsx
│   │   └── ...
│   │
│   ├── influencers/
│   │   ├── InfluencerList.jsx
│   │   ├── InfluencerCard.jsx
│   │   ├── InfluencerForm.jsx
│   │   └── ...
│   │
│   ├── projects/
│   │   ├── ProjectList.jsx
│   │   ├── ProjectCard.jsx
│   │   ├── ProjectForm.jsx
│   │   └── ...
│   │
│   └── webProperties/
│       ├── WebPropertyList.jsx
│       ├── WebPropertyCard.jsx
│       ├── WebPropertyForm.jsx
│       └── ...
│
├── pages/
│   ├── Home.jsx
│   ├── Influencers.jsx
│   ├── Projects.jsx
│   ├── WebProperties.jsx
│   └── ...
│
├── layouts/
│   ├── MainLayout.jsx
│   ├── AuthLayout.jsx
│   └── ...
│
├── hooks/
│   ├── useAuth.js
│   ├── useApi.js
│   └── ...
│
├── utils/
│   ├── api.js
│   ├── helpers.js
│   └── ...
│
├── contexts/
│   ├── AuthContext.jsx
│   └── ...
│
├── styles/
│   ├── global.css
│   └── ...
│
├── App.jsx
└── main.jsx