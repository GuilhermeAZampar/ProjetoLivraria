import { useEffect, useState } from "react";
import LivroCard from './components/LivroCard.jsx'
import LivroForm from "./components/LivroForm.jsx";
import './App.css'

function App() {
  const [livros, setLivros] = useState([])
    const[livroEditado,setLivroEditado]=useState(null)
  const usuario = 'admin'
  const senha = 'admin'
  function BuscarLivro() {
  fetch('http://localhost:8000/livros?limit=100', {
    headers: {
      Authorization: `Basic ${btoa(`${usuario}:${senha}`)}`
    }
  })
      .then(async response=>{
          const data = await response.json()
          if(!response.ok){
              throw new Error(data.detail || 'Erro livro nao encontrado')
          }
          return data
      })
      .then(data=>{
          console.log(data)
          setLivros(data.livro ?? [])

      })

      .catch(error=>{
          console.log(error.message)
      })
}

  useEffect(() => {
    BuscarLivro()

  }, [])

  return (
    <>
      <div className={'app'}>
      <h1>Biblioteca Virtual</h1>
      <LivroForm usuario={usuario} senha={senha} buscarLivro={BuscarLivro} livroEditado={livroEditado} setLivroEditado={setLivroEditado} />
        <div className={'livro-grid'}>
      {livros.map((livro) => (
        <LivroCard key={livro.id} livro={livro} usuario={usuario} senha={senha} buscarLivros={BuscarLivro} setLivroEditado={setLivroEditado}/>

      ))}
        </div>
        </div>
    </>
  )
}

export default App