import React, { useState, useEffect } from "react";

const API = process.env.REACT_APP_API;

export const Admin = () => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [autor, setAutor] = useState("");
    const [books, setBooks] = useState([]);
    const [editing, setEditing] = useState(false)
    const [id, setId] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!editing) {
            const res = await fetch(`${API}/books`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    autor: autor,
                }),
            });
            await res.json();
        } else {
            const res = await fetch(`${API}/book/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    autor: autor
                })
            })
            await res.json();
            setEditing(false);
            setId('');
        }

        await getUsers();

        setName('')
        setDescription('')
        setAutor('')
    };

    const getUsers = async () => {
        const res = await fetch(`${API}/books`);
        const data = await res.json();
        setBooks(data);
    };

    useEffect(() => {
        getUsers();
    }, []);

    const deleteBook = async (id) => {
        const userResponse = window.confirm('Are you sure you want to delete it?')
        if (userResponse) {
            const res = await fetch(`${API}/book/${id}`, {
                method: 'DELETE'
            });
            await res.json();
            await getUsers();
        }
    };

    const editBook = async (id) => {
        const res = await fetch(`${API}/book/${id}`)
        const data = await res.json();

        setEditing(true);
        setId(id)
        setName(data.name);
        setDescription(data.description);
        setAutor(data.autor);
    };

    return (
        <div className="row">
            <div className="col-md-4">
                <form onSubmit={handleSubmit} className="card card-body">
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setName(e.target.value)}
                            value={name}
                            className="form-control"
                            placeholder="Name"
                            autoFocus
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setDescription(e.target.value)}
                            value={description}
                            className="form-control"
                            placeholder="Description"
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setAutor(e.target.value)}
                            value={autor}
                            className="form-control"
                            placeholder="Autor"
                        />
                    </div>
                    <button className="btn btn-primary btn-block">
                        {editing ? 'Update' : 'Create'}
                    </button>
                </form>
            </div>
            <div className="col-md-8">
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Autor</th>
                            <th>Operation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {books.map((book) => (
                            <tr key={book._id}>
                                <td>{book.name}</td>
                                <td>{book.description}</td>
                                <td>{book.autor}</td>
                                <td>
                                    <button
                                        className="btn btn-secondary btn-sm btn-block"
                                        onClick={(e) => editBook(book._id)}>
                                        Edit
                                    </button>
                                    <button
                                        className="btn btn-danger btn-sm btn-block"
                                        onClick={(e) => deleteBook(book._id)}>
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
