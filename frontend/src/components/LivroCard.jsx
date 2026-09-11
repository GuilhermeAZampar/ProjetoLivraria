import {useState,useEffect} from "react";
function LivroCard({livro,usuario,senha,buscarLivros,setLivroEditado}){
    const [mensagem,setMensagem]=useState('')
    const[modal,setModal]=useState(false)
    useEffect(()=>{
        if(mensagem){
            const timer = setTimeout(()=>{
                setMensagem('')
            },4000)
            return () =>clearTimeout(timer)
        }
    },[mensagem])
    function excluirLivro(){
        fetch(`http://localhost:8000/deletar/${livro.id}`,{
            method:'DELETE',
            headers:{
                Authorization:`Basic ${btoa(`${usuario}:${senha}`)}`
            }
        })
         .then(async response=>{
             const data = await response.json()
             if(!response.ok){
                 throw new Error(data.detail || 'Erro Livro nao encontrado')
             }
             return data
         })
            .then(data=>{
                console.log(data)
                setModal(false)
                buscarLivros()

            })
            .catch(error=>{
                setMensagem(error.message)
            })
    }

    function editarLivro(){
        setLivroEditado(livro)
    }
    return(
        <div className={'livro-card'}>
            <h2>{livro.nome_livro}</h2>
            <p>Autor: {livro.autor_livro}</p>
            <p>Ano: {livro.ano_livro}</p>
            {mensagem &&( <p className={'mensagem-erro'}>{mensagem}</p>)}
            <button className={'btn-excluir'} type={"button"} onClick={()=>setModal(true)} >Excluir</button>
            {modal &&(
                <div className={'modal-overlay'}>
                    <div className={'modal'}>
                        <h3>Confirmar exclusão</h3>
                        <p>Tem certeza que deseja excluir {livro.nome_livro}</p>
                         <div className={'modal-botoes'}>
                        <button type={"button"} className={'btn-cancelar'} onClick={()=>setModal(false)}>Cancelar</button>
                        <button type={"button"} className={'btn-excluir'} onClick={excluirLivro}>Confirmar Exclusão</button>
                    </div>
                    </div>
                </div>
            )}
            <button className={'btn-editar'} type={"button"} onClick={editarLivro}>Editar</button>
        </div>
    )

}

export default LivroCard