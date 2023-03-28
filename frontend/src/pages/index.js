import { Container } from '@/components/Container'
import { Book } from '@/components/Book'
import { useEffect, useState } from 'react'
import { headers } from '../../next.config'

const API = process.env.NEXT_PUBLIC_API



export default function Home() {

    const [data, setData] = useState([])

    const getBooks = async () => {
        const token = localStorage.token;
        const headers = token === undefined ? {} : {
            'Authorization': `Bearer ${token}`
        }
        const options = {
            method: 'GET',
            headers: headers
        }
        const response = await fetch(`${API}/books`)
        const data = await response.json()
        setData(data.data);
    }

    useEffect(() => {
        getBooks();
    }, []);

    return (
        <>
        <Container className="container d-flex justify-content-center" title="Books Web">
            <div className="row">
                <div className="col-12">
                    {
                        data.map((book) => (
                            <>
                                <Book key={book.id} name={book.name} author={book.author} description={book.description} className="my-5" /> 
                            </>                  
                    ))
                    }
                </div>
            </div>
        </Container>
        </>
    )
}
