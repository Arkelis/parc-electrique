/* @refresh reload */
import './style.css';
import { render } from 'solid-js/web';

import Sidebar from './Sidebar';

const root = document.getElementById('app');

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
  throw new Error(
    'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
  );
}

render(() => <Sidebar />, root!);