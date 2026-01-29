import { HashRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import './App.css';
import './i18n';

import Vocabulary from './pages/Vocabulary';
import Premium from './pages/Premium';

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="vocabulary" element={<Vocabulary />} />
          <Route path="history" element={<div className="container"><h2>History</h2><p>Coming soon...</p></div>} />
          <Route path="profile" element={<Premium />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}

export default App;
