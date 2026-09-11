import {useState,useEffect} from "react";
function LivroForm({usuario,senha,buscarLivro,livroEditado,setLivroEditado}){
    const[nome,setNome]=useState('')
    const[autor,setAutor]=useState('')
    const [ano,setAno]=useState('')
    const [mensagem,setMensagem]=useState('')
    const[tipomensagem,setTipoMensagem]=useState('')
    useEffect(()=>{
        if(mensagem){
            const timer= setTimeout(()=>{
               setMensagem('')
                setTipoMensagem('')
            },4000)
            return()=> clearTimeout(timer)

        }
    },[mensagem])

    useEffect(()=>{
        if(livroEditado){
            setNome(livroEditado.nome_livro)
            setAutor(livroEditado.autor_livro)
            setAno(livroEditado.ano_livro)
        }
    },[livroEditado])
    function validarForm(){
          if(!nome || !autor || !ano){
            setMensagem('Erro os campos nao podem ser vazios')
              setTipoMensagem('erro')
            return false
        }
        const ano_atual=new Date().getFullYear()
        const ano_maximo=ano_atual + 10
        if(Number(ano)<0 || Number(ano)>ano_maximo ){
            setMensagem(`O ano deve estar entre 0 eo ${ano_maximo}`)
            setTipoMensagem('erro')
            return false
        }

        return true

    }

    function cadastrarLivro(event){
        event.preventDefault()
        if(!validarForm()){return}
        setMensagem('')

        const livro ={
            nome_livro:nome,
            autor_livro:autor,
            ano_livro:Number(ano)
        }
        fetch('http://localhost:8000/adicionar',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                Authorization : `Basic ${btoa(`${usuario}:${senha}`)}`
            },
            body:JSON.stringify(livro)
        })
            .then(async response =>{
               const data= await response.json()
               if(!response.ok){
                   throw new Error(data.detail || 'Erro livro ja cadastrado')
               }
               return data
            })
            .then(data=>{
                console.log(data)
                setMensagem(data.message)
                setTipoMensagem('sucesso')
                setNome('')
                setAno('')
                setAutor('')
                buscarLivro()

            })
            .catch(error=>{
                setMensagem(error.message)
                setTipoMensagem('erro')
            })
    }

    function atualizar_livro(event){
        event.preventDefault()
       if(!validarForm()){return}
       setMensagem('')

        const livro={
            nome_livro:nome,
            autor_livro:autor,
            ano_livro:Number(ano)
        }
        console.log('Livro sendo editado:', livro)
        console.log("ID: ", livroEditado.id)
        fetch(`http://localhost:8000/atualizar/${livroEditado.id}`,{
            method:'PUT',
            headers:{
                'Content-type':'application/json',
                Authorization : `Basic ${btoa(`${usuario}:${senha}`)}`
            },
            body:JSON.stringify(livro)
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
                setMensagem(data.message)
                setTipoMensagem('sucesso')
                buscarLivro()
                cancelar_edicao()
            })
            .catch(error=>{
                setMensagem(error.message)
                setTipoMensagem('erro')
            })
    }
    function limpar_campos(){
        setLivroEditado(null)
        setNome('')
        setAutor('')
        setAno('')


    }
    function cancelar_edicao(){
        limpar_campos()
        setMensagem('')
        setTipoMensagem('')


    }

    return(
       <form className={'livro-form'} onSubmit={livroEditado ?  atualizar_livro : cadastrarLivro} >
           <h1>Cadastro de livros</h1>
           <input type={"text"} placeholder={"Digite o nome do livro "} value={nome} onChange={event => setNome(event.target.value)}/>
           <input type={"text"} placeholder={"Digite o nome do Autor "} value={autor} onChange={event => setAutor(event.target.value)}/>
           <input type={"number"} placeholder={"Digite ano de lançamento do livro "} value={ano} onChange={event => setAno(event.target.value)}/>
           {mensagem &&( <p className={tipomensagem == 'sucesso' ? 'mensagem-sucesso' : 'mensagem-erro'}>{mensagem}</p>)}
           <button className={'btn-principal'} type={"submit"} >{livroEditado ? 'Atualizar' : 'Cadastrar'}</button>
           {livroEditado && (
               <button className={'btn-cancelar'} type={"button"} onClick={cancelar_edicao}>Cancelar Ediçao</button>
           )}

       </form>

    )
}

export default LivroForm