import { useState } from 'react'


function MyButton() {
  const [count, setCount] = useState(0)

  function handleClick() {
    setCount(count + 1)
  }

  return (
    <button onClick={handleClick}>
      Кликнули {count} раз
    </button>
  )
}


function App() {
  return (
    <div className="App">
      <div className="wrapper">
        АААААААА, КНОПКА
        <MyButton />
      </div>
    </div>
  );
}

export default App;
