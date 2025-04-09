// ********************************
// FROM REACT ELECTRON BOILERPLATE:
import '@testing-library/jest-dom';
import { getByTestId, render } from '@testing-library/react';
import App from '../renderer/App';

 
describe('App', () => {
  it('should render', () => {
    expect(render(<App />)).toBeTruthy();
  });
});
// *********************************






// *********************************
// Work done.
// *********************************

// Could be useful:
// import UI from '../renderer/Components/UI';
// import Pagination from '../renderer/Components/Pagination';
// import Sidebar from '../renderer/Components/Sidebar';
// import CommentThread from '../renderer/Components/CommentThread';

// Tests.
describe('Initial render is correct', () => {
  test('Check sidebar', () => {
    render(<App />)

    expect(getByTestId(document.documentElement, 'sidebar'),).toBeInTheDocument()
    expect(getByTestId(document.documentElement, 'upload-button'),).toBeInTheDocument()
  });

  test('Check generate button panel', () => {
    render(<App />)

    expect(getByTestId(document.documentElement, 'generate-button'),).toBeInTheDocument()
  })
});
